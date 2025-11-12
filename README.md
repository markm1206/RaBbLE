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

All configuration is managed through the `config.rabl` file, which is organized into 7 configuration sections:

### Display Configuration
- **width**: Screen resolution width (default: 800)
- **height**: Screen resolution height (default: 600)
- **background_color**: RGB tuple for background (default: `[0, 0, 0]` - black)
- **text_color**: RGB tuple for transcribed text (default: `[255, 255, 255]` - white)

### Color Scheme
- **eye_color**: RGB tuple for eyes and eyelids (default: `[150, 75, 150]` - magenta)
- **waveform_color**: RGB tuple for mouth/waveform visualization (default: same as eye_color)

### Face Component Positioning
- **eye.radius**: Eye size in pixels (default: 30)
- **eye.left_x_offset**: Left eye horizontal offset from face center (default: -60)
- **eye.right_x_offset**: Right eye horizontal offset from face center (default: 60)
- **eye.y_offset**: Eye vertical offset from face center (default: -40)
- **eye.left_eyelid_position**: Starting eyelid position for left eye (default: "bottom")
- **eye.right_eyelid_position**: Starting eyelid position for right eye (default: "top")
- **mouth.y_offset**: Mouth vertical offset from face center (default: 80)
- **mouth.width**: Width of mouth animation (default: 300)
- **mouth.max_amplitude**: Maximum waveform amplitude clamp (default: 90)

### Audio Configuration
- **chunk_size**: PyAudio chunk size in samples (default: 2048)
- **sample_rate**: Recording sample rate in Hz (default: 16000)
- **channels**: Number of audio channels (default: 1 - mono)
- **gain_factor**: Audio amplification multiplier for transcription (default: 1.5)

### Transcription Configuration
- **interval_seconds**: How often to process audio chunks (default: 0.5 seconds)
- **overlap_seconds**: Overlap between transcription chunks (default: 0.1 seconds)
- **backend**: Transcriber backend - "openai" or "faster-whisper" (default: "faster-whisper")
- **model_name**: Whisper model name (default: "tiny.en")

### Waveform Configuration
- **base_frequency**: Base frequency for sine wave (1.0 = one full cycle across screen width)
- **breathing_amplitude**: Amplitude of breathing effect (0-1, default: 0.15)
- **line_width**: Thickness of waveform line in pixels (default: 5)

### Emotion Configuration
Each emotion can be customized with:
- **blink_interval**: Blink frequency in milliseconds
- **mouth_shape**: Animation shape - "sine", "parabolic", "saw", or "default"
- **y_offset**: Vertical offset for mouth shape (usually 0)
- **amplitude_multiplier**: Multiplier for audio amplitude
- **shape_params**: Shape-specific parameters (frequency, amplitude, curve intensity, etc.)

**Available Emotions**:
- **IDLE**: Subtle sine wave with slow breathing (blink_interval: 1000ms)
- **HAPPY**: Parabolic smile with sine undulation (blink_interval: 1000ms)
- **SAD**: Parabolic frown with sine undulation (blink_interval: 2000ms)
- **ANGRY**: Sawtooth aggressive animation (blink_interval: 500ms)

## Recent Updates

### Configuration System Refactoring
The system has been refactored to use a centralized configuration approach:

- **Centralized Configuration**: All system parameters are now managed in `config.rabl`, eliminating hardcoded constants throughout the codebase
- **Unified Waveform System**: All waveform shapes (sine, parabolic, sawtooth) now maintain consistent Y-center positioning
- **Base Frequency Normalization**: Implemented 1.0 base frequency representing one full sine cycle across the screen width
- **Robust Path Resolution**: Configuration file is loaded correctly regardless of working directory

### Waveform Improvements
- **Sine Waveforms**: Proper mathematical implementation using sin(x) with 2π scaling
- **Parabolic Waveforms**: Proper quadratic curve implementation (smile/frown shapes) with configurable intensity
- **Sawtooth Waveforms**: Symmetric triangle waves oscillating around center Y position
- **Consistent Center Y**: All waveforms maintain the same Y-axis center point for predictable animation

## Integration with RABBLE

This frontend is designed to work as a standalone UI component that can be integrated into larger RABBLE agent systems. It communicates through:
-   **Emotion State**: Set via `Face.set_emotion(emotion_name)`.
-   **Audio Input**: Receives amplified audio stream through `AudioHandler` for real-time visualization and transcription.
-   **Transcribed Text**: Provides real-time speech-to-text output.

### Using in Your Project
```python
from face import Face
from audio_handler import AudioHandler
from transcriber import FasterWhisperTranscriber
import pygame

# Initialize components
face = Face(400, 300, eye_color, waveform_color, background_color, 
           emotion_config, face_config, waveform_config)

# Control emotions
face.set_emotion("HAPPY")

# Listen for transcribed text
text = text_queue.get_nowait()  # Get latest transcription
```

## Customization

### Adding a New Emotion

1. Open `config.rabl` and add a new emotion entry:
```yaml
emotion_config:
  CONFUSED:
    blink_interval: 1500
    mouth_shape: sine
    y_offset: 0
    amplitude_multiplier: 550
    shape_params:
      sine_frequency: 0.02
      sine_amplitude: 12
```

2. Run the application - the new emotion will be automatically available

### Modifying Waveform Animation

1. Adjust `waveform_config` in `config.rabl`:
```yaml
waveform_config:
  base_frequency: 0.5      # Slower animation (half cycle)
  breathing_amplitude: 0.25 # More pronounced breathing
  line_width: 6            # Thicker waveform line
```

2. Changes take effect on next run

### Adjusting Audio Settings

```yaml
audio_config:
  gain_factor: 2.0  # Boost audio for better transcription
  sample_rate: 44100 # Higher sample rate for quality
```

### Customizing Colors

```yaml
colors:
  eye_color: [255, 100, 50]      # Orange eyes
  waveform_color: [0, 255, 255]  # Cyan mouth
```

## Troubleshooting

### Configuration Loading Issues
- Ensure `config.rabl` is in the same directory as `main.py`
- Check for YAML syntax errors (proper indentation required)
- Run with debug output to see where it's looking for the file

### No Audio Input
- Verify microphone is connected and permissions granted
- Check `audio_config.sample_rate` matches your system
- Try adjusting `audio_config.chunk_size`

### Transcription Not Working
- Ensure transcription backend is installed: `pip install faster-whisper` or `pip install openai-whisper`
- Check `transcription_config.backend` is set correctly
- Verify internet connection (for OpenAI backend)
- Check `logs/` directory for transcription errors

### Poor Animation Performance
- Reduce display resolution in `display_config`
- Increase `waveform_config.base_frequency` for simpler waveforms
- Close other applications to free up resources
- Try CPU-optimized transcription backend (faster-whisper)

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
