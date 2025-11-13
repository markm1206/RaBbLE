# RABBLE Animated Face Frontend - Code Review & Architecture Guide

This document provides a comprehensive overview of the codebase structure, component relationships, and design patterns to help developers quickly understand and extend the system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [New Modules & Features](#new-modules-and-features)
4. [Transcription & Word Management Deep Dive](#transcription--word-management-deep-dive)
5. [File Structure](#file-structure)
6. [Data Flow](#data-flow)
7. [Extending the System](#extending-the-system)
8. [Key Design Patterns](#key-design-patterns)
9. [Performance Considerations](#performance-considerations)
10. [Troubleshooting Guide](#troubleshooting-guide)
11. [Integration Notes](#integration-notes)

---

## Architecture Overview

The RABBLE Animated Face Frontend follows a **modular, hierarchical component model** with enhanced capabilities for audio processing, transcription, and dynamic configuration.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                 main.py                                   │
│                      (Application Orchestration & GUI)                    │
│                                                                           │
│  - Pygame initialization & main loop                                      │
│  - Loads all configurations from `.rabl` files via `rabl_parser.py`       │
│  - Manages `AudioHandler` and `Transcriber` threads                       │
│  - Initializes and updates `WordDisplayManager`                           │
│  - Renders `Face` component and transcribed text                          │
└───────────────────┬───────────────────┬───────────────────┬───────────────┘
                    │                   │                   │
                    ↓                   ↓                   ↓
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│  rabl_parser.py   │ │  audio_handler.py │ │   transcriber.py  │
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
┌───────────────────┐ ┌─────────────────────────────────────────┐
│ word_display_manager.py │ │                  Face                   │
│ (Word Display Logic)    │ │        (Dynamic Emotion Manager)        │
│ - Manages pending/active│ │                                         │
│   word queues           │ │  - Manages emotional state dynamically  │
│ - Timed word release    │ │    from loaded RABL config              │
│ - Scrolling animation   │ │  - Coordinates Eye and Mouth rendering  │
└───────────────────┘ └────────┬────────────────────────┬───────┘
                              │                        │
                              ↓                        ↓
                         ┌──────────────────┐   ┌──────────────────┐
                         │  Eye (x2)        │   │  Mouth           │
                         │  - Blinking      │   │  - Audio Viz     │
                         │  - Eyelids       │   │  - Waveforms     │
                         └──────────────────┘   └──────────────────┘
```

**Design Principles:**
- **Separation of Concerns**: Each component/module has a single, well-defined responsibility.
- **Dynamic Configuration**: Emotion behaviors are externalized into `.rabl` files, allowing runtime modification without code changes.
- **Model Agnosticism**: The transcription system uses an Abstract Base Class, enabling easy swapping or addition of different ASR models.
- **Multithreading**: Dedicated threads for audio input and transcription prevent GUI blocking, ensuring responsiveness.
- **Producer-Consumer Pattern**: `queue.Queue` is used for safe, thread-to-thread data transfer.
- **Color Inheritance**: Colors are passed via constructor, allowing easy theming.
- **State Management**: Components maintain their own state (blink timers, animations).
- **Time-Based Animation**: Uses `pygame.time.get_ticks()` for smooth, frame-rate-independent animations.
- **Data Normalization & Amplification**: Audio is normalized for visualization and optionally amplified for transcription.

---

## Core Components

### 1. `main.py` - Application Orchestration & GUI

**Responsibility**: Initializes Pygame, loads all configurations, sets up and manages threads, handles user input, and orchestrates the main rendering loop.

**Main Functions**:
- `main()`: Core application loop.
  - Initializes Pygame.
  - Loads all configurations from the `config/` directory using `rabl_parser.py`.
  - Sets up `animation_queue`, `transcription_queue`, and `model_loaded_event`.
  - Instantiates and starts `AudioHandler` and `Transcriber`.
  - **Initializes `WordDisplayManager`**, which handles the state and rendering of transcribed text.
  - Creates `Face` component, passing loaded configurations.
  - Handles events (quit, emotion cycling, eyelid toggle).
  - Retrieves audio data from `animation_queue` for `Face` drawing.
  - **Calls `word_display_manager.update()` and `word_display_manager.draw()`** each frame.

---

### 2. `face.py` - Dynamic Emotion Manager

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

### 3. `eye.py` - Eye Component (Blinking & Rendering)

**Responsibility**: Renders individual eyes with realistic blinking animations and asymmetric eyelid positioning. (No significant changes in recent refactoring).

---

### 4. `mouth.py` - Mouth Component (Audio Visualization)

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

### 1. `rabl_parser.py` - RABL Configuration Parser

**Responsibility**: Provides a robust mechanism to parse `.rabl` files, which define emotion configurations.

**Key Features**:
-   Uses the `PyYAML` library for reliable parsing of YAML-like structures.
-   Includes error handling for `FileNotFoundError` and `yaml.YAMLError`.

**Main Function**:
-   `parse_rabl(file_path)`: Reads and parses a `.rabl` file into a Python dictionary.

---

### 2. `audio_handler.py` - Threaded Audio Input

**Responsibility**: Manages microphone audio input in a separate thread to prevent blocking the main GUI. Distributes audio data to different queues for visualization and transcription.

**Key Features**:
-   Runs in a `threading.Thread`.
-   Initializes and manages `PyAudio` stream.
-   **Audio Amplification**: Amplifies raw audio data (e.g., by `1.5`) before sending it to the transcription queue, improving transcription accuracy for quieter speech.
-   Uses two `queue.Queue` instances:
    -   `animation_queue`: For real-time, un-amplified audio data (normalized) for mouth visualization.
    -   `transcription_queue`: For amplified raw audio data for the transcriber.

---

### 3. `transcriber.py` - Model-Agnostic Speech-to-Text Transcriber

**Responsibility**: Provides a flexible, multi-threaded system for speech-to-text transcription. It now sends transcribed text directly to the `WordDisplayManager`.

### 4. `word_display_manager.py` - Real-Time Word Display

**Responsibility**: Manages the state, animation, and rendering of transcribed words.

**Key Features**:
- **Dual Queue System**:
    - `pending_display_words`: A queue for words received from the transcriber, waiting to be displayed.
    - `active_display_words`: A queue for words currently visible on the screen.
- **Timed Word Release**: Words are moved from the pending to the active queue at a regular interval (`word_display_interval_ms`), creating a smooth, paced appearance.
- **Frame-Rate Independent Scrolling**: Uses a `delta_time` calculation in its `update()` method to ensure words scroll at a consistent speed (`scroll_speed`) regardless of the application's frame rate.
- **Dynamic Positioning**: Manages the `x` position of each word, removing them once they scroll off-screen.

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
    -   Instead of putting the text into another queue, it **directly calls `word_display_manager.add_transcribed_text(text)`**, passing the data across the thread boundary.

3.  **`WordDisplayManager` (State Manager)**:
    -   Does not run in a thread. It is owned and managed by the main thread.
    -   Its `add_transcribed_text` method is thread-safe for this specific use case because it only appends to a `deque`, which is an atomic operation in Python.
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
├── main.py                    # Entry point, orchestration, GUI
├── rabl_parser.py             # RABL configuration parser
├── audio_handler.py           # Threaded audio input and amplification
├── transcriber.py             # Model-agnostic speech-to-text transcriber
├── word_display_manager.py    # Manages real-time display of transcribed words
├── face.py                    # Face component (dynamic emotion manager)
├── eye.py                     # Eye component (blinking, rendering)
├── mouth.py                   # Mouth component (audio visualization)
├── config/
│   ├── app.rabl               # Main application configuration
│   ├── emotions.rabl          # Emotion-specific configurations
│   └── transcription.rabl     # Transcription and word display settings
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── CODEREVIEW.md              # Developer guide
└── logs/                      # Directory for transcription log files
```

---

## Data Flow

### Per-Frame Execution Order (Updated)

```
1. main.py: Handle Events
   ├─ Check for quit, emotion change, eyelid toggle

2. main.py: Update State
   └─ face.update()
       ├─ left_eye.update()
       └─ right_eye.update()

3. audio_handler.py (Thread): Read Audio
   ├─ stream.read(CHUNK)
   ├─ put amplified audio into transcription_queue
   └─ put normalized audio into animation_queue

4. transcriber.py (Thread): Process Audio & Transcribe
   ├─ Pulls from transcription_queue into an internal buffer
   ├─ Processes buffer in overlapping chunks
   ├─ Calls `_transcribe_audio` (model-specific)
   └─ Calls `word_display_manager.add_transcribed_text(text)`

5. main.py: Update Word Display
   └─ word_display_manager.update(delta_time)
       ├─ Moves words from pending to active queue
       └─ Updates positions of active words for scrolling

6. main.py: Draw Components
   ├─ Get latest normalized audio from animation_queue
   ├─ face.draw(screen, ...)
   └─ word_display_manager.draw(screen)

7. main.py: Display Update
   └─ pygame.display.flip()
```

### Audio Data Pipeline (Updated)

```
Microphone
    ↓
AudioHandler (Thread)
    ├── Raw Bytes (amplified) → transcription_queue → Transcriber (Thread) → word_display_manager.add_transcribed_text()
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
2.  **Update `main.py`**: The `EMOTIONS` list is now dynamically generated, so no code change is needed here.
3.  **Implement New Mouth Shape (if custom)**: If `mouth_shape` refers to a new shape, implement its rendering logic in `mouth.py`'s `draw()` method.

### Adding a New Mouth Shape

1.  **Implement in `mouth.py` `draw()` method**: Add a new `elif shape == "your_new_shape":` block with the custom rendering logic. Ensure it uses `DEFAULT_WAVEFORM_FREQUENCY` and respects `max_amplitude`.
2.  **Define parameters in `emotions.rabl`**: For any emotion using this new shape, specify `mouth_shape: your_new_shape` and provide any `shape_params` it requires.

### Adding a New Transcriber Backend

1.  **Create a new class**: Create `YourNewTranscriber(AbstractTranscriber)` in `transcriber.py`.
2.  **Implement `_load_model()`**: Load your ASR model within this method.
3.  **Implement `_transcribe_audio(audio_np)`**: Process the `audio_np` (float32 array) and return the transcribed text string.
4.  **Update `main.py` factory**: Add an `elif` condition to the transcriber factory in `main.py` to instantiate `YourNewTranscriber` when `TRANSCRIBER_BACKEND` is set to your new model's identifier.
5.  **Update `requirements.txt`**: Add any new Python dependencies for your transcriber.

---

## Key Design Patterns

1.  **Component-Based Architecture**
2.  **Dynamic Configuration (RABL)**: Externalizes all parameters for flexibility.
3.  **Abstract Factory / Strategy Pattern (Transcriber)**: `AbstractTranscriber` defines a common interface, and the factory in `main.py` selects a concrete strategy (`OpenAIWhisperTranscriber` or `FasterWhisperTranscriber`) at runtime.
4.  **Multithreading**: `AudioHandler` and `Transcriber` run in separate threads to ensure a non-blocking GUI.
5.  **Producer-Consumer (Queues)**: `animation_queue` and `transcription_queue` facilitate safe inter-thread communication.
6.  **Event-Based Signaling (`model_loaded_event`)**: Synchronizes thread initialization.
7.  **State Management**: Components like `Face` and `WordDisplayManager` manage their own internal states.
8.  **Time-Based Animation**: Ensures smooth animations independent of frame rate.

---

## Performance Considerations

-   **Transcriber Model**: `faster-whisper` with `compute_type="int8"` is the recommended backend for CPU-bound devices due to its speed and efficiency.
-   **VAD**: Enabling `vad_filter` in `transcription.rabl` for the `faster-whisper` backend can significantly reduce unnecessary processing during silent periods.
-   **`interval_seconds`**: A smaller interval reduces transcription latency but increases CPU load. `0.5` seconds offers a good balance.
-   **`overlap_seconds`**: Essential for accuracy. `0.1` seconds is a reasonable default that prevents words from being cut off between transcription chunks.

---

## Troubleshooting Guide

-   **RABL Parsing Errors**: Check all `.rabl` files in the `config/` directory for correct YAML syntax.
-   **Transcription Model Not Loading**: Ensure the selected backend (`openai-whisper` or `faster-whisper`) is installed via `requirements.txt`. Check the console for model loading messages.
-   **No Transcription Output**: Verify that the `transcription_queue` is being populated in `audio_handler.py` and that the `Transcriber` is successfully processing it. Check the `logs/` directory for transcription logs and potential errors.
-   **Mouth Animation Issues**: Ensure the `animation_queue` is receiving data.
-   **General Performance**: If performance is slow, consider using a smaller Whisper model (e.g., `"tiny.en"`), enabling VAD, or increasing `interval_seconds` in `transcription.rabl`.

---

## Integration Notes

When integrating into a larger RABBLE agent:

1.  **Emotion Control**: Call `face.set_emotion(emotion_name)` from the agent's logic.
2.  **Transcribed Text**: The recommended approach is to pass a queue to the `Transcriber`'s constructor. The `Transcriber` can then put the final text into this queue for the agent to consume, in addition to sending it to the `WordDisplayManager`.

---

For questions or contributions, refer back to this document and the inline code documentation in each component.
