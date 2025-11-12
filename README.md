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

-   **Transcription Backend**: In `config/app.rabl`, set `transcription_config.backend` to `"openai"` or `"faster-whisper"`.
-   **Emotion Definitions**: Modify `config/emotions.rabl` to customize existing emotions or add new ones.
-   **Display & Audio Settings**: Configure `config/app.rabl` for display, audio, and transcription parameters.

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

All configuration is managed through files in the `config/` directory, organized into application settings and emotion-specific configurations:

### Configuration Structure

```
config/
├── app.rabl        # Main application configuration (display, audio, positioning, waveform)
└── emotions.rabl   # Emotion-specific configurations (cycle_rate, frequencies, expressions)
```

### app.rabl - Main Application Configuration

#### Display Configuration
- **width**: Screen resolution width (default: 800)
- **height**: Screen resolution height (default: 600)
- **background_color**: RGB tuple for background (default: `[0, 0, 0]` - black)
- **text_color**: RGB tuple for transcribed text (default: `[255, 255, 255]` - white)

#### Color Scheme
- **eye_color**: RGB tuple for eyes and eyelids (default: `[150, 75, 150]` - magenta)
- **waveform_color**: RGB tuple for mouth/waveform visualization (default: same as eye_color)

#### Face Component Positioning
- **eye.radius**: Eye size in pixels (default: 30)
- **eye.left_x_offset**: Left eye horizontal offset from face center (default: -60)
- **eye.right_x_offset**: Right eye horizontal offset from face center (default: 60)
- **eye.y_offset**: Eye vertical offset from face center (default: -40)
- **eye.left_eyelid_position**: Starting eyelid position for left eye (default: "bottom")
- **eye.right_eyelid_position**: Starting eyelid position for right eye (default: "top")
- **mouth.y_offset**: Mouth vertical offset from face center (default: 80)
- **mouth.width**: Width of mouth animation (default: 300)
- **mouth.max_amplitude**: Maximum waveform amplitude clamp (default: 90)

#### Audio Configuration
- **chunk_size**: PyAudio chunk size in samples (default: 2048)
- **sample_rate**: Recording sample rate in Hz (default: 16000)
- **channels**: Number of audio channels (default: 1 - mono)
- **gain_factor**: Audio amplification multiplier for transcription (default: 1.5)

#### Transcription Configuration
- **interval_seconds**: How often to process audio chunks (default: 0.5 seconds)
- **overlap_seconds**: Overlap between transcription chunks (default: 0.1 seconds)
- **backend**: Transcriber backend - "openai" or "faster-whisper" (default: "faster-whisper")
- **model_name**: Whisper model name (default: "tiny.en")

#### Waveform Base Parameters
- **base_frequency**: Base frequency for animations (default: 1.0)
- **breathing_amplitude**: Amplitude of breathing effect (0-1, default: 0.15)
- **line_width**: Thickness of waveform line in pixels (default: 5)

### emotions.rabl - Emotion-Specific Configuration

Each emotion has its own configuration with animation parameters. Frequencies are specified **in terms of π** (e.g., `2` means 2π radians).

#### Emotion Parameters
- **blink_interval**: Blink frequency in milliseconds
- **mouth_shape**: Animation shape - "sine", "parabolic", "saw", or "default"
- **y_offset**: Vertical offset for mouth shape
- **audio_amplitude_multiplier**: Controls audio waveform amplitude (0-100 scale)
  - 0 = straight line (no audio effect)
  - 50 = half audio modulation
  - 100 = full audio range
- **cycle_rate**: Animation speed multiplier (1.0 = normal, 2.0 = double speed, 0.5 = half speed)
- **shape_params**: Shape-specific parameters:
  - **sine_frequency**: Frequency in terms of π for sine waves
  - **saw_frequency**: Frequency in terms of π for sawtooth waves
  - **parabolic_sine_frequency**: Frequency in terms of π for parabolic waves
  - **curve_direction**: For parabolic shapes (1.0 = smile/convex, -1.0 = frown/concave)

#### Available Emotions (Default)
- **IDLE**: Subtle sine wave with normal speed (cycle_rate: 1.0)
- **NEUTRAL**: Sawtooth wave with slightly faster speed (cycle_rate: 1.5)
- **HAPPY**: Parabolic smile with steady motion (cycle_rate: 0.8)
- **SCARED**: Parabolic open-mouth with nervous rapid motion (cycle_rate: 2.0)
- **SAD**: Parabolic frown with slow, melancholic motion (cycle_rate: 0.6)
- **ANGRY**: Sawtooth aggressive animation with very fast motion (cycle_rate: 2.5)

#### Example Emotion Configuration

```yaml
emotion_config:
  IDLE:
    blink_interval: 1000
    mouth_shape: sine
    y_offset: 0
    audio_amplitude_multiplier: 60
    cycle_rate: 1.0
    shape_params:
      sine_frequency: 2                 # 2π radians = one full cycle
```

## Recent Updates

### Configuration System Restructuring (Phase 5)
- **Modular Config Structure**: Reorganized into `config/app.rabl` and `config/emotions.rabl`
- **Per-Emotion Cycle Rate**: Each emotion now has its own `cycle_rate` for independent animation speed control
- **π-Based Frequency Specification**: Frequencies now specified in terms of π (e.g., 2 = 2π radians) for improved clarity
- **Clearer Parameter Naming**: 
  - `amplitude_multiplier` → `audio_amplitude_multiplier` (makes purpose clear)
  - `curve_factor_intensity` → `curve_direction` (more intuitive)
- **Removed Legacy Parameters**: Cleaned up unused configuration parameters for simplicity
- **Enhanced RABL Parser**: Now handles file references, loading emotions from separate file automatically

### Waveform System Refinement (Phase 4)
- **Unified Sinusoidal Effects**: All waveforms (sine, parabolic, sawtooth) now exhibit consistent amplitude and frequency effects
- **Consistent Amplitudes**: All shapes use ±30 pixels sinusoidal motion for predictable behavior
- **Simplified Configuration**: Removed unused parameters (saw_period_divisor, sine_amplitude, parabolic_sine_amplitude, etc.)

### Configuration System Refactoring (Phase 1-3)
- **Centralized Configuration**: All system parameters managed through `.rabl` config files
- **Unified Waveform System**: Consistent Y-center positioning across all shapes
- **Base Frequency Normalization**: 1.0 = one full cycle across screen width
- **Robust Path Resolution**: Configuration loads correctly from any working directory

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

1. Open `config/emotions.rabl` and add a new emotion entry:
```yaml
emotion_config:
  CONFUSED:
    blink_interval: 1500
    mouth_shape: sine
    y_offset: 0
    audio_amplitude_multiplier: 55
    cycle_rate: 1.2
    shape_params:
      sine_frequency: 1.5              # In terms of π
```

2. Run the application - the new emotion will be automatically available via the M key

### Modifying Animation Speed Per Emotion

Adjust `cycle_rate` to control animation speed independently for each emotion:

```yaml
emotion_config:
  EXCITED:
    cycle_rate: 3.0                    # Very fast animation
  SLEEPY:
    cycle_rate: 0.3                    # Very slow animation
```

### Modifying Waveform Frequency

Frequencies are specified in terms of π in `config/emotions.rabl`:

```yaml
shape_params:
  sine_frequency: 1.0                  # 1π radians
  sine_frequency: 2.0                  # 2π radians (one full cycle)
  sine_frequency: 0.5                  # 0.5π radians (half cycle)
```

### Modifying Base Waveform Parameters

Edit `config/app.rabl` waveform_config section:
```yaml
waveform_config:
  base_frequency: 1.0                  # Animation base frequency
  breathing_amplitude: 0.25            # More pronounced breathing effect
  line_width: 6                        # Thicker waveform line
```

### Adjusting Audio Settings

```yaml
audio_config:
  gain_factor: 2.0                     # Boost audio for better transcription
  sample_rate: 44100                   # Higher sample rate for quality
  chunk_size: 4096                     # Larger chunks for better quality
```

### Customizing Colors

```yaml
colors:
  eye_color: [255, 100, 50]            # Orange eyes
  waveform_color: [0, 255, 255]        # Cyan mouth
```

## Troubleshooting

### Configuration Loading Issues
- Ensure `config/app.rabl` and `config/emotions.rabl` exist in the `config/` directory
- Check for YAML syntax errors (proper indentation required)
- Run with debug output to see where configuration is being loaded from
- Verify the `emotions_file` reference in `app.rabl` points to the correct path

### No Audio Input
- Verify microphone is connected and permissions granted
- Check `audio_config.sample_rate` matches your system
- Try adjusting `audio_config.chunk_size`

### Transcription Not Working
- Ensure transcription backend is installed: `pip install faster-whisper` or `pip install openai-whisper`
- Check `transcription_config.backend` is set correctly in `config/app.rabl`
- Verify internet connection (for OpenAI backend)
- Check `logs/` directory for transcription errors

### Animation Not Responsive Enough
- Increase `audio_amplitude_multiplier` in the emotion (0-100 scale)
- Reduce `cycle_rate` to slow down waveform oscillation
- Increase `waveform_config.base_frequency`

### Animation Too Jerky or Inconsistent
- Try adjusting the frequency in terms of π (higher = more oscillations per screen width)
- Increase `waveform_config.line_width` for smoother visual appearance
- Ensure `cycle_rate` is between 0.5 and 3.0 for smooth motion

### Poor Animation Performance
- Reduce display resolution in `display_config`
- Decrease `waveform_config.line_width`
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
