# RaBbLE -- ReUsable Animated Babbling Language Engine

## Overview

This is a modular, lightweight animated face frontend designed as the visual interface for **RABBLE**, a voice-enabled AI assistant agent optimized for edge system deployment. The face serves as an intuitive, expressive way for RABBLE to communicate through animated visual feedback, complementing voice interactions with emotional expressions and real-time audio visualization. It now includes a pluggable speech-to-text transcription engine and a dynamic, real-time word display system.

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
- **Dynamic Word Display**: Transcribed words are displayed in real-time with smooth scrolling animations, managed by the `WordDisplayManager`.
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

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your system has audio input capability (microphone).

## Usage

Run the application:
```bash
python main.py
```

### Keyboard Controls

-   **M**: Cycle through emotions (defined in `emotions.rabl`).
-   **T**: Toggle eyelid positions (swap which eye has top/bottom eyelid).

## Project Structure

For detailed information about the code architecture, components, and how to extend the system, see [CODEREVIEW.md](CODEREVIEW.md).

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

## Architecture

The system follows a modular, hierarchical design:

```
main.py (Orchestration, GUI)
    ├── rabl_parser.py (Parses all .rabl config files)
    ├── audio_handler.py (Threaded Audio Input, Amplification)
    └── transcriber.py (Threaded Transcription, Logging)
        ↓ (sends words to)
    word_display_manager.py (Manages word display)
        ↓ (drawn by main.py)
    Face (Emotion Manager, dynamically configured)
        ├── Eye (Left & Right - Blinking & Rendering)
        └── Mouth (Audio Visualization, dynamically configured)
```

## The RABL Configuration System

**RABL** (Reusable Animated Babbling Language Engine) configuration is managed through a set of `.rabl` files located in the `config/` directory. The RABL markup language is based on YAML, making it easy to read and modify. This system externalizes all major parameters, allowing for extensive customization without code changes.

### Configuration Structure

The configuration is split into three main files, which are all loaded and parsed by `rabl_parser.py`:

```
config/
├── app.rabl             # Main application settings (display, audio, face positioning)
├── emotions.rabl        # Emotion-specific animation parameters
└── transcription.rabl   # Transcription model and word display settings
```

### `app.rabl` - Main Application Configuration

This file contains global settings for the application window, colors, and the physical layout of the face components.

- **`display_config`**: Screen resolution and colors.
- **`colors`**: Defines the color palette for the eyes and mouth.
- **`face_config`**: Controls the size and position of the eyes and mouth.
- **`audio_config`**: Settings for audio capture, such as sample rate and gain.
- **`waveform_config`**: Base parameters for the mouth's waveform animations.

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
-   **Transcribed Text**: The `Transcriber` now directly manages the display of text via the `WordDisplayManager`. To integrate with an agent, you would modify the `Transcriber` to also send the text to your agent's logic.

### Using in Your Project
```python
# In main.py, you would modify the Transcriber's run loop
# to pass the transcribed text to your agent.

# Example modification in transcriber.py:
class AbstractTranscriber(ABC, threading.Thread):
    def __init__(self, ..., agent_text_queue=None):
        ...
        self.agent_text_queue = agent_text_queue

    def run(self):
        ...
        if text:
            cleaned_text = self._apply_cleanup_strategy(text)
            if cleaned_text:
                self.word_display_manager.add_transcribed_text(cleaned_text)
                if self.agent_text_queue:
                    self.agent_text_queue.put(cleaned_text) # Send to agent
                ...
```

## Troubleshooting

### Configuration Loading Issues
- Ensure `config/app.rabl`, `config/emotions.rabl`, and `config/transcription.rabl` exist.
- Check for YAML syntax errors (proper indentation is crucial).
- The `rabl_parser.py` now automatically resolves file paths, so it should work regardless of the execution directory.

### No Audio Input
- Verify your microphone is connected and has the correct permissions.
- Check that `audio_config.sample_rate` in `app.rabl` matches your system's capabilities.

### Transcription Not Working
- Ensure the selected backend is installed: `pip install faster-whisper` or `pip install openai-whisper`.
- Check that `transcription_config.backend` is set correctly in `transcription.rabl`.
- Check the `logs/` directory for any transcription-related error messages.

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
