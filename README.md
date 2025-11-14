# RaBbLE -- ReUsable Animated Babbling Language Engine

## Overview

This is a modular, lightweight animated face frontend designed as the visual interface for **RABBLE**, a voice-enabled AI assistant agent optimized for edge system deployment. The face serves as an intuitive, expressive way for RABBLE to communicate through animated visual feedback, complementing voice interactions with emotional expressions and real-time audio visualization. It now includes a pluggable speech-to-text transcription engine, a dynamic, real-time word display system, and an extensible LLM agent integration.

![RABBLE Animated Face Demo](RabbleAnimationV0.2.0.gif)

## Features

- **Modular Component Architecture**: Cleanly separated components (Eyes, Mouth, Face) for easy modification and extension.
- **Dynamic Emotional Expression**: Emotion states are loaded from a `.rabl` configuration file, allowing easy customization and addition of new emotions with specific blink rates, mouth shapes, and animation parameters.
- **Real-Time Audio Visualization**: Mouth animates in response to amplified audio input with standardized waveform shapes and frequencies, ensuring a smoother and more consistent visual experience.
- **Advanced Speech-to-Text Transcription**:
    -   **Model-Agnostic Transcriber**: Easily swap between `openai-whisper` and `faster-whisper` backends via a simple configuration.
    -   **Multi-threaded Audio Processing**: Dedicated threads for audio input and transcription ensure a responsive GUI.
    -   **Configurable Transcription Interval**: Adjust how often transcription occurs for optimal latency.
    -   **Overlapping Audio Buffers**: Prevents missed speech at chunk boundaries for improved accuracy.
    -   **Transcription Logging**: All transcribed text is saved to timestamped log files in the `logs/` directory.
    -   **Transcription Pause/Unpause**: Toggle transcription processing with a keyboard shortcut.
- **Dynamic Word Display**: Transcribed words are displayed in real-time with smooth scrolling animations, managed by the `WordDisplayManager`.
- **Extensible LLM Agent Integration**:
    -   **AbstractLLMAgent Interface**: Defines a clear contract for integrating various LLM agent implementations.
    -   **EchoLLMAgent**: A basic agent that echoes input, useful for testing.
    -   **GoogleADKLLMAgent (Placeholder)**: A placeholder for integrating with Google's Agent Development Kit.
    -   LLM agent responses are displayed on the screen.
- **Hideable Text Input Field**: A text input field can be toggled visible/hidden for direct user input to the LLM agent.
- **Smooth Blinking Animations**: Natural eye blinking with emotion-dependent blink rates.
- **Edge-Optimized**: Lightweight design suitable for deployment on resource-constrained edge devices.
- **Pygame-Based**: Cross-platform rendering using Pygame for broad compatibility.

## Requirements

- Python 3.13+
- pygame
- pyaudio
- numpy
- openai-whisper (for OpenAI Whisper backend)
- faster-whisper (for Faster-Whisper backend)
- pyyaml (for RABL configuration parsing)
- langchain (for LLM agent framework, if used)
- google-adk (for Google Agent Development Kit integration, if used)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your system has audio input capability (microphone).

## Usage

Run the application from the root directory:
```bash
python -m src.main
```

### Keyboard Controls

-   **M**: Cycle through emotions (defined in `emotions.rabl`).
-   **T**: Toggle eyelid positions (swap which eye has top/bottom eyelid).
-   **P**: Toggle transcription pause/unpause.
-   **I**: Toggle visibility of the text input field.

## Project Structure

For detailed information about the code architecture, components, and how to extend the system, see [CODEREVIEW.md](CODEREVIEW.md).

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

## Architecture

The system follows a modular, hierarchical design:

```
src/main.py (Application Orchestration & GUI)
    ├── src/config/config_loader.py (Loads all .rabl config files)
    ├── src/audio/audio_handler.py (Threaded Audio Input, Amplification)
    ├── src/transcription/transcriber.py (Threaded Transcription, Logging)
    │   ↓ (sends words to)
    ├── src/agent/llm_agent.py (AbstractLLMAgent interface, concrete implementations)
    │   ↓ (sends responses to)
    └── src/ui/word_display_manager.py (Manages word display and text input)
        ↓ (drawn by main.py)
    src/animation/face.py (Emotion Manager, dynamically configured)
        ├── src/animation/eye.py (Left & Right - Blinking & Rendering)
        └── src/animation/mouth.py (Audio Visualization, dynamically configured)
```

## The RABL Configuration System

**RABL** (Reusable Animated Babbling Language Engine) configuration is managed through a set of `.rabl` files located in the `config/` directory. The RABL markup language is based on YAML, making it easy to read and modify. This system externalizes all major parameters, allowing for extensive customization without code changes.

### Configuration Structure

The configuration is split into multiple `.rabl` files, which are all loaded and parsed by `src/config/config_loader.py`:

```
config/
├── audio.rabl           # Audio capture and processing configuration
├── display.rabl         # Display settings (resolution, colors)
├── emotions.rabl        # Emotion-specific animation parameters
├── face_layout.rabl     # Face component positioning and sizing
└── transcription.rabl   # Transcription model and word display settings
```

### `audio.rabl` - Audio Configuration

This file contains settings related to audio input, amplification, and processing.

- **`audio_config`**: Settings for audio capture, such as sample rate, chunk size, and gain.

### `display.rabl` - Display Configuration

This file defines the main application window settings and color palette.

- **`display_config`**: Screen resolution (width, height) and caption.
- **`colors`**: Defines the color palette for various UI elements, including eyes, mouth, and background.

### `face_layout.rabl` - Face Layout Configuration

This file controls the size and position of the face components (eyes and mouth) on the screen.

- **`face_config`**: Controls the size and position of the eyes and mouth, including eye radius, eye spacing, mouth width, and mouth height.
- **`waveform_config`**: Base parameters for the mouth's waveform animations, such as default frequency and breathing effect amplitude.

### `emotions.rabl` - Emotion-Specific Configuration

This file defines the unique animation behaviors for each emotional state.

- Each top-level key is an emotion name (e.g., `IDLE`, `HAPPY`).
- **`blink_interval`**: Time in milliseconds between blinks.
- **`mouth_shape`**: The animation style for the mouth (`sine`, `parabolic`, `saw`).
- **`audio_amplitude_multiplier`**: How strongly the audio volume affects the mouth animation (0-100).
- **`cycle_rate`**: The speed of the animation cycle (1.0 is normal).
- **`shape_params`**: Parameters specific to the chosen `mouth_shape`, such as frequency and direction.

### `transcription.rabl` - Transcription and Word Display

This file configures the speech-to-text engine and the appearance of the transcribed text.

- **`backend`**: The transcription model to use (`"openai-whisper"` or `"faster-whisper"`).
- **`model_name`**: The specific Whisper model size (e.g., `"tiny.en"`, `"base.en"`).
- **`device`**: The hardware to run the model on (`"cpu"` or `"cuda"`).
- **`interval_seconds`**: How often the audio buffer is processed for transcription.
- **`overlap_seconds`**: How much audio to overlap between chunks to prevent missed words.
- **`vad_filter`**: (For `faster-whisper`) Enables Voice Activity Detection to filter out silence.
- **`cleanup_strategy`**: Post-processing strategy for transcribed text (e.g., `"simple_deduplication"`).
- **`scroll_speed`**: The speed at which transcribed words scroll across the screen (pixels per second).
- **`word_display_interval_ms`**: The time in milliseconds between displaying each new word.

## Integration with RABBLE

This frontend is designed to work as a standalone UI component that can be integrated into larger RABBLE agent systems. It communicates through:
-   **Emotion State**: Set via `Face.set_emotion(emotion_name)`.
-   **Audio Input**: Receives amplified audio stream through `AudioHandler` for real-time visualization and transcription.
-   **Transcribed Text**: The `Transcriber` sends transcribed text to the `WordDisplayManager` for display and to the active `AbstractLLMAgent` for processing.
-   **LLM Agent Responses**: The active `AbstractLLMAgent` sends its responses back to the `WordDisplayManager` for display.

### Using in Your Project
```python
# In main.py, you would select and instantiate your desired LLM agent:
from src.agent.llm_agent import EchoLLMAgent
from src.agent.google_adk_llm_agent import GoogleADKLLMAgent

# ... inside main() ...
llm_agent_input_queue = queue.Queue()
llm_agent_output_queue = queue.Queue()

USE_GOOGLE_ADK_AGENT = False # Set to True to use GoogleADKLLMAgent

if USE_GOOGLE_ADK_AGENT:
    llm_agent = GoogleADKLLMAgent(llm_agent_input_queue, llm_agent_output_queue)
else:
    llm_agent = EchoLLMAgent(llm_agent_input_queue, llm_agent_output_queue)

# Pass llm_agent_input_queue to Transcriber and both queues to WordDisplayManager
# ...
```

## Troubleshooting

### Configuration Loading Issues
- Ensure all `.rabl` files in the `config/` directory exist.
- Check for YAML syntax errors (proper indentation is crucial).

### ModuleNotFoundError
- If you encounter `ModuleNotFoundError` when running `python src/main.py`, try running the application as a module: `python -m src.main`. The `main.py` file includes a `sys.path` modification to help with module discovery.

### No Audio Input
- Verify your microphone is connected and has the correct permissions.
- Check that `audio_config.sample_rate` in `audio.rabl` matches your system's capabilities.

### Transcription Not Working
- Ensure the selected backend is installed: `pip install faster-whisper` or `pip install openai-whisper`.
- Check that `transcription_config.backend` is set correctly in `transcription.rabl`.
- Check the `logs/` directory for any transcription-related error messages.
- If using `device: "cuda"` and encountering errors, ensure your CUDA and cuDNN setup is correct, or change `device` to `"cpu"` in `transcription.rabl`.

### LLM Agent Not Responding
- Ensure the `OPENAI_API_KEY` environment variable is set if you are using an OpenAI-based LLM (e.g., if you were to re-integrate `ChatOpenAI`).
- Verify that the correct LLM agent is selected in `src/main.py` (e.g., `USE_GOOGLE_ADK_AGENT` flag).
- Check the console output for any errors from the `LLMAgent` thread.

## License

```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              © 2025 Mark McConachie                                ║
║                                                                    ║
║                      All Rights Reserved                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

## Contributing

Contributions are welcome! Please refer to [CODEREVIEW.md](CODEREVIEW.md) for code structure and design patterns before making modifications.
