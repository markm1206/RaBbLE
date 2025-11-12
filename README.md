# RaBbLE -- ReUsable Animated Babbling Language Engine

# RaBbLE -- ReUsable Animated Babbling Language Engine

## Overview

This is a modular, lightweight animated face frontend designed as the visual interface for **RABBLE**, a voice-enabled AI assistant agent optimized for edge system deployment. The face serves as an intuitive, expressive way for RABBLE to communicate through animated visual feedback, complementing voice interactions with emotional expressions and real-time audio visualization. It now includes a pluggable speech-to-text transcription engine.

![RABBLE Animated Face Demo](RabbleAnimationV0.1.0.gif)

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
- **Smooth Blinking Animations**: Natural eye blinking with emotion-dependent blink rates.
- **Edge-Optimized**: Lightweight design suitable for deployment on resource-constrained edge devices.
- **Pygame-Based**: Cross-platform rendering using Pygame for broad compatibility.

## Requirements

- Python 3.7+
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

### Configuration

-   **Transcription Backend**: In `main.py`, set `TRANSCRIBER_BACKEND` to `"openai"` or `"faster-whisper"`.
-   **Emotion Definitions**: Modify `emotions.rabl` to customize existing emotions or add new ones.
-   **Transcription Parameters**: In `transcriber.py`, adjust `TRANSCRIPTION_INTERVAL_SECONDS` and `OVERLAP_SECONDS`.

### Keyboard Controls

-   **M**: Cycle through emotions (defined in `emotions.rabl`).
-   **T**: Toggle eyelid positions (swap which eye has top/bottom eyelid).

## Project Structure

For detailed information about the code architecture, components, and how to extend the system, see [CODEREVIEW.md](CODEREVIEW.md).

## Architecture

The system follows a modular, hierarchical design:

```
main.py (Orchestration, GUI, Emotion Loading)
    ├── rabl_parser.py (Parses .rabl emotion config)
    ├── audio_handler.py (Threaded Audio Input, Amplification)
    └── transcriber.py (Abstract Transcriber, OpenAI/FasterWhisper Implementations, Threaded Transcription, Logging)
        ↓
    Face (Emotion Manager, dynamically configured)
        ├── Eye (Left & Right - Blinking & Rendering)
        └── Mouth (Audio Visualization, dynamically configured, clamped amplitude)
```

## Configuration

Emotion-specific configurations are now managed in `emotions.rabl`. Key constants in `main.py` can still be adjusted:

-   **TRANSCRIBER_BACKEND**: Selects the transcription engine (`"openai"` or `"faster-whisper"`).
-   **WIDTH, HEIGHT**: Display resolution (default: 800x600).
-   **EYE_COLOR**: RGB tuple for eye color (default: magenta `(150, 75, 150)`).
-   **WAVEFORM_COLOR**: RGB tuple for mouth color (default: same as eye color).
-   **BACKGROUND_COLOR**: RGB tuple for background (default: black `(0, 0, 0)`).
-   **TEXT_COLOR**: RGB tuple for transcribed text (default: white `(255, 255, 255)`).

## Integration with RABBLE

This frontend is designed to work as a standalone UI component that can be integrated into larger RABBLE agent systems. It communicates through:
-   **Emotion State**: Set via `Face.set_emotion(emotion_name)`.
-   **Audio Input**: Receives amplified audio stream through `AudioHandler` for real-time visualization and transcription.
-   **Transcribed Text**: Provides real-time speech-to-text output.

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
