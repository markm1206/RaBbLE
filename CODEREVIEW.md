# RABBLE Animated Face Frontend - Code Review & Architecture Guide

This document provides a comprehensive overview of the codebase structure, component relationships, and design patterns to help developers quickly understand and extend the system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [New Modules & Features](#new-modules-and-features)
4. [LLM Agent Integration Deep Dive](#llm-agent-integration-deep-dive)
5. [Transcription & Word Management Deep Dive](#transcription--word-management-deep-dive)
6. [File Structure](#file-structure)
7. [Data Flow](#data-flow)
8. [Extending the System](#extending-the-system)
9. [Key Design Patterns](#key-design-patterns)
10. [Performance Considerations](#performance-considerations)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Integration Notes](#integration-notes)

---

## Architecture Overview

The RABBLE Animated Face Frontend follows a **modular, hierarchical component model** with enhanced capabilities for audio processing, transcription, dynamic configuration, and extensible LLM agent integration.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                               src/main.py                                 │
│                      (Application Orchestration & GUI)                    │
│                                                                           │
│  - Pygame initialization & main loop                                      │
│  - Loads all configurations from `.rabl` files via `src/config/rabl_parser.py` │
│  - Manages `AudioHandler`, `Transcriber`, and `AbstractLLMAgent` threads  │
│  - Initializes and updates `WordDisplayManager`                           │
│  - Renders `Face` component, transcribed text, and LLM agent responses    │
└───────────────────┬───────────────────┬───────────────────┬───────────────┘
                    │                   │                   │
                    ↓                   ↓                   ↓
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│src/config/rabl_parser.py│ │src/audio/audio_handler.py│ │src/transcription/transcriber.py│
│ (RABL Config Parser)│ │ (Threaded Audio Input)│ │ (Model-Agnostic Transcriber)│
│  - Parses `.rabl` files │ │  - Manages PyAudio stream │ │  - Abstract base class    │
│  - Uses `PyYAML` for robust │ │  - Amplifies audio for    │ │  - OpenAIWhisperTranscriber│
│    parsing                │ │    transcription          │ │  - FasterWhisperTranscriber│
│                           │ │  - Provides audio to      │ │  - Threaded transcription │
│                           │ │    queues                 │ │  - Overlapping buffers    │
└───────────────────┘ └───────────────────┘ └───────────────────┘
                    │                   │
                    │ creates & updates │ sends transcribed words
                    ↓                   ↓
┌───────────────────┐ ┌───────────────────┐ ┌─────────────────────────────────────────┐
│src/agent/llm_agent.py│ │src/ui/word_display_manager.py│ │               src/animation/face.py               │
│ (Abstract LLM Agent)│ │ (Word Display Logic)    │ │        (Dynamic Emotion Manager)        │
│ - Interface for LLM │ │ - Manages pending/active│ │                                         │
│   agents            │ │   word queues           │ │  - Manages emotional state dynamically  │
│ - EchoLLMAgent      │ │ - Timed word release    │ │    from loaded RABL config              │
│ - GoogleADKLLMAgent │ │ - Scrolling animation   │ │  - Coordinates Eye and Mouth rendering  │
└───────────────────┘ └───────────────────┘ └────────┬────────────────────────┬───────┘
                    │                   │            │                        │
                    │ sends queries to  │ receives LLM responses from
                    │                   │            ↓                        ↓
                    └───────────────────┼───────────┐
                                        │           │
                                        ↓           ↓
                                   ┌──────────────────┐   ┌──────────────────┐
                                   │src/animation/eye.py│   │src/animation/mouth.py│
                                   │  - Blinking      │   │  - Audio Viz     │
                                   │  - Eyelids       │   │  - Waveforms     │
                                   └──────────────────┘   └──────────────────┘
```

**Design Principles:**
- **Separation of Concerns**: Each component/module has a single, well-defined responsibility.
- **Dynamic Configuration**: Emotion behaviors are externalized into `.rabl` files, allowing runtime modification without code changes.
- **Model Agnosticism**: The transcription system uses an Abstract Base Class, enabling easy swapping or addition of different ASR models. The LLM agent system now also uses an Abstract Base Class for flexible LLM integration.
- **Multithreading**: Dedicated threads for audio input, transcription, and LLM agent processing prevent GUI blocking, ensuring responsiveness.
- **Producer-Consumer Pattern**: `queue.Queue` is used for safe, thread-to-thread data transfer between audio, transcriber, LLM agent, and word display.
- **Color Inheritance**: Colors are passed via constructor, allowing easy theming.
- **State Management**: Components maintain their own state (blink timers, animations, word display, input field).
- **Time-Based Animation**: Uses `pygame.time.get_ticks()` for smooth, frame-rate-independent animations.
- **Data Normalization & Amplification**: Audio is normalized for visualization and optionally amplified for transcription.

---

## Core Components

### 1. `src/main.py` - Application Orchestration & GUI

**Responsibility**: Initializes Pygame, loads all configurations, sets up and manages threads for audio, transcription, and the LLM agent, handles user input (including new keyboard controls for pause and text input), and orchestrates the main rendering loop.

**Main Functions**:
- `main()`: Core application loop.
  - Initializes Pygame.
  - **Adds project root to `sys.path` for module discovery.**
  - Loads all configurations from the `config/` directory using `src/config/config_loader.py`.
  - Sets up `animation_queue`, `transcription_queue`, `llm_agent_input_queue`, `llm_agent_output_queue`, `model_loaded_event`, and `transcriber_ready_event`.
  - Instantiates and starts `AudioHandler`, `Transcriber`, and the selected `AbstractLLMAgent` implementation.
  - Initializes `WordDisplayManager`, which handles the state and rendering of transcribed text, LLM responses, and the text input field.
  - Creates `Face` component, passing loaded configurations.
  - Handles events (quit, emotion cycling, eyelid toggle, **transcription pause/unpause, text input toggle, text input processing**).
  - Retrieves audio data from `animation_queue` for `Face` drawing.
  - Calls `word_display_manager.update()` and `word_display_manager.draw()` each frame, **passing `current_time` for LLM response display timing**.
  - **Calls `word_display_manager.draw_input_box()`** each frame.

---

### 2. `src/animation/face.py` - Dynamic Emotion Manager

**Responsibility**: Manages the overall emotional state of the face and coordinates the rendering of its `Eye` and `Mouth` components based on dynamic configurations.

**Constructor**:
```python
Face(x, y, eye_color, mouth_color, background_color, emotion_config)
```

**Parameters**:
- `x, y`: Center position of the face.
- `eye_color, mouth_color, background_color`: RGB tuples for theming.
- `emotion_config`: Dictionary containing emotion configurations loaded from `emotions.rabl`.

**Key Attributes**:
- `self.emotion`: Current emotion state (e.g., "IDLE", "HAPPY").
- `self.emotion_config`: Stores the loaded emotion parameters.
- `self.left_eye, self.right_eye`: `Eye` components.
- `self.mouth`: `Mouth` component.

**Public Methods**:
- `set_emotion(emotion)`: Sets the face emotion and updates blink intervals based on `emotion_config`.
- `toggle_eyelids()`: Swaps eyelid positions for asymmetric expressions.
- `update()`: Updates component states.
- `draw(screen, normalized_data, current_time)`: Renders the face, dynamically retrieving mouth parameters (`y_offset`, `amplitude_multiplier`, `mouth_shape`, `shape_params`) from `emotion_config`.

---

### 3. `src/animation/eye.py` - Eye Component (Blinking & Rendering)

**Responsibility**: Renders individual eyes with realistic blinking animations and asymmetric eyelid positioning. (No significant changes in recent refactoring).

---

### 4. `src/animation/mouth.py` - Mouth Component (Audio Visualization)

**Responsibility**: Renders mouth shapes based on audio input, with emotion-specific waveform shapes and breathing effects, now with standardized properties.

**Key Constants**:
- `DEFAULT_WAVEFORM_FREQUENCY`: Ensures consistent movement speed across all waveforms.
- `BREATHING_EFFECT_AMPLITUDE`: Controls the subtlety of the time-varied breathing effect.

**Key Methods**:
- `draw(screen, normalized_data, y_offset, amplitude_multiplier, shape, current_time, max_amplitude, shape_params)`:
  -   `y_offset`: Now consistently `0` for all emotions, aligning waveform midpoints.
  -   `amplitude_multiplier`: Standardized across most emotions, with a slightly higher value for "ANGRY".
  -   `shape_params`: Dynamically retrieves shape-specific parameters (e.g., `sine_frequency`, `saw_period_divisor`, `base_amplitude`) from the RABL config.
  -   `max_amplitude`: Clamps the waveform's vertical extent to prevent overlap with eyes.
  -   Waveform generation logic updated to use `DEFAULT_WAVEFORM_FREQUENCY` and reduced `BREATHING_EFFECT_AMPLITUDE`.
  -   Line thickness increased to `5` for a smoother appearance.

---

## New Modules & Features

### 1. `src/config/rabl_parser.py` - RABL Configuration Parser

**Responsibility**: Provides a robust mechanism to parse `.rabl` files, which define emotion configurations.

**Key Features**:
-   Uses the `PyYAML` library for reliable parsing of YAML-like structures.
-   Includes error handling for `FileNotFoundError` and `yaml.YAMLError`.

**Main Function**:
-   `parse_rabl(file_path)`: Reads and parses a `.rabl` file into a Python dictionary.

---

### 2. `src/audio/audio_handler.py` - Threaded Audio Input

**Responsibility**: Manages microphone audio input in a separate thread to prevent blocking the main GUI. Distributes audio data to different queues for visualization and transcription.

**Key Features**:
-   Runs in a `threading.Thread`.
-   Initializes and manages `PyAudio` stream.
-   **Audio Amplification**: Amplifies raw audio data (e.g., by `1.5`) before sending it to the transcription queue, improving transcription accuracy for quieter speech.
-   Uses two `queue.Queue` instances:
    -   `animation_queue`: For real-time, un-amplified audio data (normalized) for mouth visualization.
    -   `transcription_queue`: For amplified raw audio data for the transcriber.

---

### 3. `src/transcription/transcriber.py` - Model-Agnostic Speech-to-Text Transcriber

**Responsibility**: Provides a flexible, multi-threaded system for speech-to-text transcription. It now sends transcribed text to both the `WordDisplayManager` and the active `AbstractLLMAgent`.

**Key Features**:
-   **Transcription Pause/Unpause**: Includes a `paused` flag and `toggle_pause()` method to control transcription processing.

---

### 4. `src/ui/word_display_manager.py` - Real-Time Word Display & Text Input

**Responsibility**: Manages the state, animation, and rendering of transcribed words, LLM agent responses, and the hideable text input field.

**Key Features**:
- **Dual Queue System**:
    - `pending_display_words`: A queue for words received from the transcriber, waiting to be displayed.
    - `active_display_words`: A queue for words currently visible on the screen.
    - **`llm_response_display_queue`**: A queue for LLM agent responses, displayed separately.
- **Timed Word Release**: Words are moved from the pending to the active queue at a regular interval (`word_display_interval_ms`), creating a smooth, paced appearance.
- **Frame-Rate Independent Scrolling**: Uses a `delta_time` calculation in its `update()` method to ensure words scroll at a consistent speed (`scroll_speed`) regardless of the application's frame rate.
- **Dynamic Positioning**: Manages the `x` position of each word, removing them once they scroll off-screen.
- **Hideable Text Input**: Manages the state (`input_box_active`, `input_text`), event handling (`handle_event`), and drawing (`draw_input_box`) for a user-facing text input field.
- **LLM Response Display**: Displays responses from the LLM agent in a distinct area of the screen.

---

## LLM Agent Integration Deep Dive

The system now features a modular LLM agent architecture, allowing for flexible integration with various LLM frameworks.

### Queueing, Threading, and Data Flow

1.  **`Transcriber` (Producer)**:
    -   Sends cleaned transcribed text to the `llm_agent_input_queue`.
2.  **`WordDisplayManager` (Producer)**:
    -   Sends user input from the text field to the `llm_agent_input_queue`.
3.  **`AbstractLLMAgent` (Consumer/Producer)**:
    -   Runs in its own thread.
    -   Consumes text queries from the `llm_agent_input_queue`.
    -   Processes the query using its specific LLM integration.
    -   Produces the LLM's response and puts it into the `llm_agent_output_queue`.
4.  **`WordDisplayManager` (Consumer)**:
    -   Consumes LLM responses from the `llm_agent_output_queue` and displays them on the screen.

### Classes

-   **`src/agent/llm_agent.py`**:
    -   **`AbstractLLMAgent(ABC, threading.Thread)`**:
        -   Abstract base class defining the interface (`process_query`, `stop`) for all LLM agent implementations.
        -   Manages common threading logic and queue handling.
    -   **`EchoLLMAgent(AbstractLLMAgent)`**:
        -   Concrete implementation that simply echoes the input query. Useful for testing and as a generic fallback.
-   **`src/agent/google_adk_llm_agent.py`**:
    -   **`GoogleADKLLMAgent(AbstractLLMAgent)`**:
        -   A placeholder concrete implementation for integrating with Google's Agent Development Kit. It currently simulates interaction by echoing the input with a specific prefix.

---

## Transcription & Word Management Deep Dive

### Queueing, Threading, and Data Flow

The system uses a multi-threaded, producer-consumer architecture to handle audio processing and transcription without freezing the main GUI thread.

1.  **`AudioHandler` (Producer)**:
    -   Runs in its own thread.
    -   Continuously reads raw audio data from the microphone.
    -   It produces data for two separate consumers:
        1.  **For Animation**: It normalizes the raw audio and puts it into the `animation_queue`. This queue is size-limited (`maxsize=2`) to ensure the animation is always based on the most recent audio.
        2.  **For Transcription**: It amplifies the raw audio (to improve model accuracy) and puts it into the unbounded `transcription_queue`.

2.  **`Transcriber` (Consumer/Producer)**:
    -   Runs in its own thread.
    -   Consumes raw audio data from the `transcription_queue`.
    -   Once it transcribes a chunk of audio, it produces the resulting text.
    -   It puts the text into the `transcribed_text_queue` for `WordDisplayManager` and also into the `llm_agent_input_queue` for the active `AbstractLLMAgent`.

3.  **`WordDisplayManager` (State Manager)**:
    -   Does not run in a thread. It is owned and managed by the main thread.
    -   Its `update()` method pulls transcribed text from `transcribed_text_queue` and LLM responses from `llm_agent_output_queue`.
    -   The main loop calls its `update()` and `draw()` methods each frame.

4.  **Synchronization**:
    -   `model_loaded_event`: A `threading.Event` is used to signal when the transcription model has been fully loaded into memory. The `AudioHandler` waits for this event to be set before it starts feeding data into the `transcription_queue`, preventing the transcriber from being overwhelmed at startup.

### Audio Buffering and Timing

To transcribe a continuous stream of audio, the `Transcriber` uses a sophisticated buffering and overlapping strategy.

-   **`audio_buffer`**: A `bytearray` that accumulates incoming raw audio data from the `transcription_queue`.
-   **`interval_seconds`**: This parameter (e.g., `0.5s`) determines the size of the audio chunk that will be sent to the transcription model. The thread waits until the `audio_buffer` contains at least this much data.
-   **`overlap_seconds`**: This is the key to not missing words at the boundaries of chunks. After a chunk is transcribed, it is not entirely discarded. A small portion of it (`overlap_seconds`, e.g., `0.1s`) is kept at the beginning of the `audio_buffer`. This provides the model with context from the previous chunk, greatly improving the accuracy of transcriptions for words that span two chunks.

This process repeats, creating a continuous, sliding window of audio for transcription.

### Transcription Models and Performance

The system is designed to be model-agnostic, with two primary backends configured in `transcription.rabl`.

-   **`openai-whisper`**: The original implementation from OpenAI. It is highly accurate but can be resource-intensive.
-   **`faster-whisper`**: A re-implementation of Whisper that is optimized for speed and lower memory usage, making it ideal for edge devices.
    -   **Inference Speed**: `faster-whisper` can be up to 4 times faster than `openai-whisper`.
    -   **Quantization**: It achieves this performance through optimizations like **INT8 quantization**, which reduces the precision of the model's numerical weights. This significantly speeds up calculations on CPUs at the cost of a minor trade-off in accuracy. The `compute_type` is set automatically based on the selected `device` (`int8` for CPU, `float16` for CUDA).
-   **Voice Activity Detection (VAD)**:
    -   Available only in the `faster-whisper` backend.
    -   VAD is a system that detects human speech in an audio stream. When `vad_filter` is enabled, the transcriber will first analyze the audio for speech. If no speech is detected, it will not send the audio to the model, saving significant computational resources and preventing the model from hallucinating text from background noise.

**Key Constants**:
-   `TRANSCRIPTION_INTERVAL_SECONDS`: Configurable interval (e.g., `0.5` seconds) for processing audio chunks.
-   `OVERLAP_SECONDS`: Configurable overlap (e.g., `0.1` seconds) between chunks to prevent missed speech.

**Classes**:
-   **`AbstractTranscriber(ABC, threading.Thread)`**:
    -   Abstract base class defining the interface (`_load_model`, `_transcribe_audio`) for all transcriber implementations.
    -   Manages common threading logic, audio buffering, logging, and model loading signaling (`model_loaded_event`).
    -   Implements configurable chunking with overlapping buffers.
    -   Logs transcribed text to a timestamped file in the `logs/` directory.
-   **`OpenAIWhisperTranscriber(AbstractTranscriber)`**:
    -   Concrete implementation using the `openai-whisper` library.
    -   Loads the specified Whisper model (e.g., `"tiny.en"`).
    -   Transcribes audio using `self.model.transcribe()`.
-   **`FasterWhisperTranscriber(AbstractTranscriber)`**:
    -   Concrete implementation using the `faster-whisper` library.
    -   Loads the `WhisperModel` with `device="cpu"` and `compute_type="int8"` for optimized CPU performance.
    -   Processes transcription segments from `self.model.transcribe()` iterator.

---

## File Structure

```
Animated_Face_FrontEnd/
├── src/
│   ├── main.py                # Entry point, orchestration, GUI
│   ├── __init__.py
│   ├── animation/
│   │   ├── face.py            # Face component (dynamic emotion manager)
│   │   ├── eye.py             # Eye component (blinking, rendering)
│   │   └── mouth.py           # Mouth component (audio visualization)
│   ├── audio/
│   │   └── audio_handler.py   # Threaded audio input and amplification
│   ├── config/
│   │   ├── config_loader.py   # Loads all .rabl files
│   │   └── rabl_parser.py     # RABL configuration parser
│   ├── transcription/
│   │   └── transcriber.py     # Model-agnostic speech-to-text transcriber
│   ├── ui/
│   │   └── word_display_manager.py # Manages real-time display of transcribed words and text input
│   └── agent/
│       ├── llm_agent.py           # Abstract LLM Agent interface and EchoLLMAgent
│       └── google_adk_llm_agent.py # Google ADK LLM Agent placeholder
├── config/
│   ├── audio.rabl             # Audio capture and processing configuration
│   ├── display.rabl           # Display settings (resolution, colors)
│   ├── emotions.rabl          # Emotion-specific animation parameters
│   ├── face_layout.rabl       # Face component positioning and sizing
│   └── transcription.rabl     # Transcription model and word display settings
├── logs/                      # Directory for transcription log files
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── CODEREVIEW.md              # Developer guide
```

---

## Data Flow

### Per-Frame Execution Order (Updated)

```
1. main.py: Handle Events
   ├─ Check for quit, emotion change, eyelid toggle, transcription pause/unpause, text input toggle
   └─ word_display_manager.handle_event(event) # Handles text input events

2. main.py: Update State
   ├─ face.update()
   │   ├─ left_eye.update()
   │   └─ right_eye.update()
   └─ word_display_manager.update(delta_time) # Moves words, pulls LLM responses

3. audio_handler.py (Thread): Read Audio
   ├─ stream.read(CHUNK)
   ├─ put amplified audio into transcription_queue
   └─ put normalized audio into animation_queue

4. transcriber.py (Thread): Process Audio & Transcribe
   ├─ Pulls from transcription_queue into an internal buffer (if not paused)
   ├─ Processes buffer in overlapping chunks
   ├─ Calls `_transcribe_audio` (model-specific)
   ├─ Puts transcribed text into `transcribed_text_queue` (for display)
   └─ Puts transcribed text into `llm_agent_input_queue` (for LLM agent)

5. AbstractLLMAgent (Thread): Process Queries
   ├─ Pulls queries from `llm_agent_input_queue`
   ├─ Calls `process_query(query)` (concrete agent implementation)
   └─ Puts LLM response into `llm_agent_output_queue`

6. main.py: Draw Components
   ├─ Get latest normalized audio from animation_queue
   ├─ face.draw(screen, ...)
   ├─ word_display_manager.draw(screen, current_time) # Draws transcribed words and LLM responses
   └─ word_display_manager.draw_input_box(screen, TEXT_COLOR) # Draws text input box

7. main.py: Display Update
   └─ pygame.display.flip()
```

### Audio Data Pipeline (Updated)

```
Microphone
    ↓
AudioHandler (Thread)
    ├── Raw Bytes (amplified) → transcription_queue → Transcriber (Thread)
    │                                                   ├── → transcribed_text_queue → WordDisplayManager (Main Thread)
    │                                                   └── → llm_agent_input_queue → AbstractLLMAgent (Thread) → llm_agent_output_queue → WordDisplayManager (Main Thread)
    └── Raw Bytes (normalized) → animation_queue → main.py (Mouth Visualization)
```

---

## Extending the System

### Adding a New Emotion

1.  **Modify `emotions.rabl`**: Add a new top-level key under `emotion_config` with the emotion name and its parameters (e.g., `blink_interval`, `mouth_shape`, `y_offset`, `amplitude_multiplier`, `shape_params`).
    ```rabl
    NEW_EMOTION:
      blink_interval: 750
      mouth_shape: custom_shape
      y_offset: 0
      amplitude_multiplier: 650
      shape_params:
        # ... custom parameters for 'custom_shape' ...
    ```
2.  **Update `src/main.py`**: The `EMOTIONS` list is now dynamically generated, so no code change is needed here.
3.  **Implement New Mouth Shape (if custom)**: If `mouth_shape` refers to a new shape, implement its rendering logic in `src/animation/mouth.py`'s `draw()` method.

### Adding a New Mouth Shape

1.  **Implement in `src/animation/mouth.py` `draw()` method**: Add a new `elif shape == "your_new_shape":` block with the custom rendering logic. Ensure it uses `DEFAULT_WAVEFORM_FREQUENCY` and respects `max_amplitude`.
2.  **Define parameters in `emotions.rabl`**: For any emotion using this new shape, specify `mouth_shape: your_new_shape` and provide any `shape_params` it requires.

### Adding a New Transcriber Backend

1.  **Create a new class**: Create `YourNewTranscriber(AbstractTranscriber)` in `src/transcription/transcriber.py`.
2.  **Implement `_load_model()`**: Load your ASR model within this method.
3.  **Implement `_transcribe_audio(audio_np)`**: Process the `audio_np` (float32 array) and return the transcribed text string.
4.  **Update `src/main.py` factory**: Add an `elif` condition to the transcriber factory in `src/main.py` to instantiate `YourNewTranscriber` when `TRANSCRIBER_BACKEND` is set to your new model's identifier.
5.  **Update `requirements.txt`**: Add any new Python dependencies for your transcriber.

### Adding a New LLM Agent Implementation

1.  **Create a new class**: Create `YourNewLLMAgent(AbstractLLMAgent)` in `src/agent/your_new_llm_agent.py`.
2.  **Implement `process_query(query)`**: This method will contain the logic for interacting with your chosen LLM or agent framework (e.g., Ollama, Google Gemini, a custom agent).
3.  **Update `src/main.py` for selection**:
    -   Import `YourNewLLMAgent`.
    -   Add a condition to the LLM agent selection block in `main()` to instantiate `YourNewLLMAgent` based on a configuration flag (e.g., `USE_YOUR_NEW_AGENT = True`).
4.  **Update `requirements.txt`**: Add any new Python dependencies for your LLM agent.

---

## Key Design Patterns

1.  **Component-Based Architecture**
2.  **Dynamic Configuration (RABL)**: Externalizes all parameters for flexibility.
3.  **Abstract Factory / Strategy Pattern (Transcriber & LLM Agent)**: `AbstractTranscriber` and `AbstractLLMAgent` define common interfaces, and the factory in `main.py` selects concrete strategies at runtime.
4.  **Multithreading**: `AudioHandler`, `Transcriber`, and `AbstractLLMAgent` run in separate threads to ensure a non-blocking GUI.
5.  **Producer-Consumer (Queues)**: `animation_queue`, `transcription_queue`, `llm_agent_input_queue`, and `llm_agent_output_queue` facilitate safe inter-thread communication.
6.  **Event-Based Signaling (`model_loaded_event`)**: Synchronizes thread initialization.
7.  **State Management**: Components like `Face`, `WordDisplayManager`, and `AbstractLLMAgent` manage their own internal states.
8.  **Time-Based Animation**: Ensures smooth animations independent of frame rate.

---

## Performance Considerations

-   **Transcriber Model**: `faster-whisper` with `compute_type="int8"` is the recommended backend for CPU-bound devices due to its speed and efficiency.
-   **VAD**: Enabling `vad_filter` in `transcription.rabl` for the `faster-whisper` backend can significantly reduce unnecessary processing during silent periods.
-   **`interval_seconds`**: A smaller interval reduces transcription latency but increases CPU load. `0.5` seconds offers a good balance.
-   **`overlap_seconds`**: Essential for accuracy. `0.1` seconds is a reasonable default that prevents words from being cut off between transcription chunks.
-   **LLM Agent Performance**: The performance of the LLM agent will heavily depend on the chosen LLM, the complexity of the prompt, and the network latency if using a cloud-based LLM. Consider local LLMs (like Ollama) for edge deployments.

---

## Troubleshooting Guide

-   **RABL Parsing Errors**: Check all `.rabl` files in the `config/` directory for correct YAML syntax.

-   **ModuleNotFoundError**: If you encounter `ModuleNotFoundError` when running `python src/main.py`, try running the application as a module: `python -m src.main`. The `main.py` file includes a `sys.path` modification to help with module discovery.

-   **No Audio Input**:
    -   Verify your microphone is connected and has the correct permissions.
    -   Check that `audio_config.sample_rate` in `audio.rabl` matches your system's capabilities.

-   **Transcription Not Working**:
    -   Ensure the selected backend is installed: `pip install faster-whisper` or `pip install openai-whisper`.
    -   Check that `transcription_config.backend` is set correctly in `transcription.rabl`.
    -   Check the `logs/` directory for any transcription-related error messages.
    -   If using `device: "cuda"` and encountering errors, ensure your CUDA and cuDNN setup is correct, or change `device` to `"cpu"` in `transcription.rabl`.

-   **LLM Agent Not Responding**:
    -   Verify that the correct LLM agent is selected in `src/main.py` (e.g., `USE_GOOGLE_ADK_AGENT` flag).
    -   Check the console output for any errors from the `LLMAgent` thread.
    -   If using a cloud-based LLM, ensure you have the necessary API keys set as environment variables (e.g., `OPENAI_API_KEY` for OpenAI, `GOOGLE_API_KEY` for Google services).
    -   For Google ADK, ensure proper authentication and agent deployment if you move beyond the placeholder.

---

## Integration Notes

When integrating into a larger RABBLE agent:

1.  **Emotion Control**: Call `face.set_emotion(emotion_name)` from the agent's logic.
2.  **Transcribed Text & User Input**: The `Transcriber` and `WordDisplayManager` (for text input) send text to the active `AbstractLLMAgent`'s input queue.
3.  **LLM Agent Responses**: The `AbstractLLMAgent` sends its responses to the `WordDisplayManager`'s output queue for display.

---

For questions or contributions, refer back to this document and the inline code documentation in each component.
