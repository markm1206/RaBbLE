# RABBLE Animated Face Frontend - Code Review & Architecture Guide

This document provides a comprehensive overview of the codebase structure, component relationships, and design patterns to help developers quickly understand and extend the system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [New Modules & Features](#new-modules-and-features)
4. [File Structure](#file-structure)
5. [Data Flow](#data-flow)
6. [Extending the System](#extending-the-system)
7. [Key Design Patterns](#key-design-patterns)
8. [Performance Considerations](#performance-considerations)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Integration Notes](#integration-notes)

---

## Architecture Overview

The RABBLE Animated Face Frontend follows a **modular, hierarchical component model** with enhanced capabilities for audio processing and dynamic configuration.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                 main.py                                   │
│           (Application Orchestration, GUI, Emotion Configuration)         │
│                                                                           │
│  - Pygame initialization & main loop                                      │
│  - Loads emotion configurations from `emotions.rabl` via `rabl_parser.py` │
│  - Manages `AudioHandler` and `Transcriber` threads                       │
│  - Handles user input (keyboard)                                          │
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
│                           │ │    animation & transcription │ │  - Configurable interval  │
│                           │ │    queues                 │ │  - Overlapping buffers    │
│                           │ │                           │ │  - Logs output to file    │
└───────────────────┘ └───────────────────┘ └───────────────────┘
                    │
                    │ creates & updates
                    ↓
┌─────────────────────────────────────────┐
│                  Face                   │
│        (Dynamic Emotion Manager)        │
│                                         │
│  - Manages emotional state dynamically  │
│    from loaded RABL config              │
│  - Coordinates Eye and Mouth rendering  │
│  - Maps emotions to animations          │
└────────┬────────────────────────┬───────┘
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
- **Color Inheritance**: Colors are passed via constructor, allowing easy theming.
- **State Management**: Components maintain their own state (blink timers, animations).
- **Time-Based Animation**: Uses `pygame.time.get_ticks()` for smooth, frame-rate-independent animations.
- **Data Normalization & Amplification**: Audio is normalized for visualization and optionally amplified for transcription.

---

## Core Components

### 1. `main.py` - Application Orchestration & GUI

**Responsibility**: Initializes Pygame, loads configurations, sets up and manages threads for audio and transcription, handles user input, and orchestrates the main rendering loop.

**Key Constants**:
- `TRANSCRIBER_BACKEND`: Selects between `"openai"` and `"faster-whisper"`.
- `WIDTH, HEIGHT`: Display resolution.
- `BACKGROUND_COLOR, EYE_COLOR, WAVEFORM_COLOR, TEXT_COLOR`: RGB tuples for theming.

**Main Functions**:
- `main()`: Core application loop.
  - Initializes Pygame.
  - Loads emotion configurations from `emotions.rabl` using `rabl_parser.py`.
  - Sets up `animation_queue`, `transcription_queue`, `text_queue`, and `model_loaded_event`.
  - Instantiates and starts `AudioHandler` and `Transcriber` (via factory logic).
  - Creates `Face` component, passing loaded emotion configurations.
  - Handles events (quit, emotion cycling, eyelid toggle).
  - Retrieves audio data from `animation_queue` for `Face` drawing.
  - Retrieves transcribed text from `text_queue` and renders it.
  - Manages display updates.

**Event Handling**:
- **QUIT**: Exits application.
- **KEY_M**: Cycles through emotions defined in `emotions.rabl`.
- **KEY_T**: Toggles eyelid positions.

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

**Responsibility**: Provides a flexible, multi-threaded system for speech-to-text transcription, allowing easy swapping of different Whisper model implementations.

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
├── main.py                    # Entry point, orchestration, GUI, emotion loading
├── rabl_parser.py             # RABL configuration parser (uses PyYAML)
├── emotions.rabl              # Emotion configuration file
├── audio_handler.py           # Threaded audio input and amplification
├── transcriber.py             # Model-agnostic speech-to-text transcriber (abstract + concrete impls)
├── face.py                    # Face component (dynamic emotion manager)
├── eye.py                     # Eye component (blinking, rendering)
├── mouth.py                   # Mouth component (audio visualization, standardized)
├── requirements.txt           # Python dependencies (now includes openai-whisper, faster-whisper, pyyaml)
├── README.md                  # User-facing documentation
└── CODEREVIEW.md             # This file (developer guide)
└── logs/                      # Directory for transcription log files
    └── transcription_YYYY-MM-DD_HH-MM-SS.log
```

---

## Data Flow

### Per-Frame Execution Order (Updated)

```
1. main.py: Handle Events
   ├─ Check for quit
   ├─ Check for emotion change (updates Face from RABL config)
   └─ Check for eyelid toggle

2. main.py: Update State
   └─ face.update()
       ├─ left_eye.update()   (check blink timing from RABL config)
       └─ right_eye.update()  (check blink timing from RABL config)

3. audio_handler.py (Thread): Read Audio
   ├─ stream.read(CHUNK)      (get raw audio)
   ├─ amplify raw audio for transcription_queue
   ├─ normalize raw audio for animation_queue
   └─ put data into respective queues

4. transcriber.py (Thread): Process Audio & Transcribe
   ├─ Continuously pulls amplified raw audio from transcription_queue
   ├─ Buffers audio, processes in `TRANSCRIPTION_INTERVAL_SECONDS` chunks with `OVERLAP_SECONDS`
   ├─ Calls `_transcribe_audio` (model-specific)
   └─ Puts transcribed text into text_queue and logs to file

5. main.py: Draw Components
   ├─ Get latest normalized audio from animation_queue (non-blocking)
   ├─ Get latest transcribed text from text_queue (non-blocking)
   ├─ left_eye.draw(screen)
   ├─ right_eye.draw(screen)
   └─ mouth.draw(screen, ...)  (with dynamic params from RABL config, clamped amplitude)

6. main.py: Display Update
   └─ pygame.display.flip()
```

### Audio Data Pipeline (Updated)

```
Microphone
    ↓
AudioHandler (Thread)
    ├── Raw Bytes (amplified) → Transcription Queue → Transcriber (Thread) → Transcribed Text Queue → main.py (Display & Log)
    └── Raw Bytes (normalized) → Animation Queue → main.py (Mouth Visualization)
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

1.  **Component-Based Architecture**: (As before)
2.  **Dynamic Configuration (RABL)**: Externalizes emotion parameters, promoting flexibility and ease of customization.
3.  **Abstract Factory / Strategy Pattern (Transcriber)**:
    -   `AbstractTranscriber` defines a common interface.
    -   `OpenAIWhisperTranscriber` and `FasterWhisperTranscriber` are concrete strategies.
    -   The factory logic in `main.py` selects and instantiates the appropriate strategy at runtime.
4.  **Multithreading**: `AudioHandler` and `Transcriber` run in separate threads, improving responsiveness.
5.  **Producer-Consumer (Queues)**: `animation_queue`, `transcription_queue`, `text_queue` facilitate safe inter-thread communication.
6.  **Event-Based Signaling**: `model_loaded_event` synchronizes model initialization with the main thread.
7.  **Color Inheritance**: (As before)
8.  **State Machine (Blinking)**: (As before)
9.  **Time-Based Animation**: (As before)
10. **Data Normalization & Amplification**: Standardizes audio input for consistent processing.
11. **Modular Shapes**: (As before)

---

## Performance Considerations

-   **Transcriber Model**: `faster-whisper` with `compute_type="int8"` is recommended for CPU-bound edge devices.
-   **`TRANSCRIPTION_INTERVAL_SECONDS`**: A smaller interval reduces latency but increases CPU load. `0.5` seconds is a good balance.
-   **`OVERLAP_SECONDS`**: Essential for transcription accuracy at chunk boundaries; `0.1` seconds is a reasonable default.
-   **Audio Buffer Size**: `CHUNK` in `audio_handler.py` affects responsiveness and CPU usage.
-   **Draw Calls**: Minimal per frame for efficient Pygame rendering.

---

## Troubleshooting Guide

-   **RABL Parsing Errors**: Check `emotions.rabl` for correct YAML-like syntax and indentation. The `rabl_parser.py` now uses `PyYAML` for more robust parsing.
-   **Transcription Model Not Loading**: Ensure `openai-whisper` or `faster-whisper` (and `torch` if using `openai-whisper`) are installed. Check console for "Whisper model not loaded" messages.
-   **No Transcription Output**: Verify `transcription_queue` and `text_queue` are being populated. Check `transcriber.py` logs for errors.
-   **Mouth Animation Issues**: Ensure `animation_queue` is receiving data. Check `face.py` and `mouth.py` for correct parameter passing from `emotion_config`.
-   **General Performance**: Reduce display resolution, close other applications, or try a smaller Whisper model (`tiny.en`).

---

## Integration Notes

When integrating into RABBLE agent:

1.  **Emotion Control**: Call `face.set_emotion(emotion_name)` from agent logic, using emotion names defined in `emotions.rabl`.
2.  **Audio Passthrough**: Route agent's audio output to system microphone or pipe `AudioHandler` input.
3.  **Transcribed Text**: Consume transcribed text from the `text_queue` in `main.py` for further agent processing.
4.  **Headless Mode**: Could be adapted to render to file/network stream instead of display.
5.  **Message Broadcasting**: Add event system to broadcast face state or transcribed text to other agent components.

---

For questions or contributions, refer back to this document and the inline code documentation in each component.
