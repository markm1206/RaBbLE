# RaBbLE -- ReUsable Animated Babbling Language Engine

## Overview

This is a modular, lightweight animated face frontend designed as the visual interface for **RABBLE**, a voice-enabled AI assistant agent optimized for edge system deployment. The face serves as an intuitive, expressive way for RABBLE to communicate through animated visual feedback, complementing voice interactions with emotional expressions and real-time audio visualization.

![RABBLE Animated Face Demo](RabbleAnimationV0.1.0.gif)

## Features

- **Modular Component Architecture**: Cleanly separated components (Eyes, Mouth, Face) for easy modification and extension
- **Emotional Expression**: Four distinct emotional states (IDLE, HAPPY, SAD, ANGRY) with emotion-specific animations
- **Real-Time Audio Visualization**: Mouth animates in response to audio input with multiple waveform shapes
- **Smooth Blinking Animations**: Natural eye blinking with emotion-dependent blink rates
- **Edge-Optimized**: Lightweight design suitable for deployment on resource-constrained edge devices
- **Pygame-Based**: Cross-platform rendering using Pygame for broad compatibility

## Requirements

- Python 3.7+
- pygame
- pyaudio
- numpy

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your system has audio input capability (microphone)

## Usage

Run the application:
```bash
python main.py
```

### Keyboard Controls

- **M**: Cycle through emotions (IDLE → HAPPY → SAD → ANGRY)
- **T**: Toggle eyelid positions (swap which eye has top/bottom eyelid)

## Project Structure

For detailed information about the code architecture, components, and how to extend the system, see [CODEREVIEW.md](CODEREVIEW.md).

## Architecture

The system follows a modular, hierarchical design:

```
main.py (Animation Loop & Audio I/O)
    ↓
Face (Emotion Manager)
    ├── Eye (Left & Right - Blinking & Rendering)
    └── Mouth (Audio Visualization)
```

## Configuration

Key constants in `main.py` can be adjusted:

- **WIDTH, HEIGHT**: Display resolution (default: 800x600)
- **EYE_COLOR**: RGB tuple for eye color (default: magenta `(150, 75, 150)`)
- **WAVEFORM_COLOR**: RGB tuple for mouth color (default: same as eye color)
- **BACKGROUND_COLOR**: RGB tuple for background (default: black `(0, 0, 0)`)

## Integration with RABBLE

This frontend is designed to work as a standalone UI component that can be integrated into larger RABBLE agent systems. It communicates through:
- **Emotion State**: Set via `Face.set_emotion(emotion_name)`
- **Audio Input**: Receives audio stream through PyAudio for real-time visualization

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
