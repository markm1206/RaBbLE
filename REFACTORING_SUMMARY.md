# RABBLE Animated Face Frontend - Refactoring Summary

## Overview

This document summarizes the major refactoring performed on the RABBLE Animated Face Frontend system to consolidate configuration management through the RABL configuration file system and improve waveform rendering consistency.

## Key Refactoring Goals ✓

1. **Centralize Configuration**: Move all hardcoded constants to `emotions.rabl`
2. **Unified Waveform System**: Ensure all waveforms maintain consistent Y-center positioning
3. **Base Frequency System**: Implement a 1.0 base frequency representing one full sine cycle
4. **Improve Code Maintainability**: Reduce hardcoded values throughout the codebase

## Files Modified

### 1. `emotions.rabl` - Configuration Consolidation

**Status**: Completely restructured with new sections

#### New Configuration Sections:

- **`display_config`**: Display resolution and text colors
  - `width`, `height`: Screen dimensions (800x600)
  - `background_color`: RGB tuple for background
  - `text_color`: RGB tuple for transcribed text

- **`colors`**: Color scheme configuration
  - `eye_color`: Eye and eyelid color
  - `waveform_color`: Mouth/waveform color

- **`face_config`**: Face component positioning
  - `eye.radius`: Eye size (30 pixels)
  - `eye.left_x_offset`, `eye.right_x_offset`: Eye horizontal positioning
  - `eye.y_offset`: Eye vertical positioning relative to face
  - `eye.left_eyelid_position`, `eye.right_eyelid_position`: Eyelid starting positions
  - `mouth.y_offset`: Mouth vertical positioning
  - `mouth.width`: Mouth width (300 pixels)
  - `mouth.max_amplitude`: Maximum waveform amplitude clamp (90 pixels)

- **`audio_config`**: Audio input settings
  - `chunk_size`: PyAudio chunk size (2048 samples)
  - `sample_rate`: Recording sample rate (16000 Hz)
  - `channels`: Mono (1 channel)
  - `gain_factor`: Audio amplification for transcription (1.5x)

- **`transcription_config`**: Transcription settings
  - `interval_seconds`: Processing interval (0.5 seconds)
  - `overlap_seconds`: Chunk overlap (0.1 seconds)
  - `backend`: Transcriber backend ("faster-whisper" or "openai")
  - `model_name`: Whisper model name ("tiny.en")

- **`waveform_config`**: Waveform rendering parameters
  - `base_frequency`: 1.0 (one full sine cycle across screen width)
  - `breathing_amplitude`: 0.15 (breathing effect intensity)
  - `line_width`: 5 pixels

#### Enhanced `emotion_config`:

Each emotion now includes `shape_params` with proper configuration:

- **`IDLE`** (Sine wave):
  - `sine_frequency`: 0.015 (relative to base_frequency)
  - `sine_amplitude`: 10 pixels
  
- **`HAPPY`** & **`SAD`** (Parabolic wave):
  - `parabolic_sine_frequency`: 0.05
  - `parabolic_sine_amplitude`: 5
  - `curve_factor_intensity`: 1.0 (controls parabolic curve strength)
  
- **`ANGRY`** (Sawtooth wave):
  - `saw_period_divisor`: 8
  - `base_amplitude`: 20 pixels
  - `saw_frequency`: 0.02

---

### 2. `mouth.py` - Waveform System Refactor

**Status**: Completely rewritten with new logic

#### Major Changes:

1. **Unified Y-Axis Positioning**
   - **Before**: Waveforms had different baseline Y values
   - **After**: All waveforms maintain `self.y` as the center line
   - All audio amplitudes and shape oscillations are added/subtracted from this center

2. **Parabolic Waveform with Curvature**
   ```
   curve_factor = (1 - normalized_position²) * curve_factor_intensity
   ```
   - Uses proper quadratic function: $f(x) = 1 - x^2$ where $x \in [-1, 1]$
   - Creates inverted parabola (peak at center)
   - Multiplied by `curve_factor_intensity` for control
   - Provides 20-pixel base lift from center

3. **Base Frequency System (1.0)**
   - **Before**: Arbitrary frequency values spread across code
   - **After**: Single `base_frequency` = 1.0 represents one full sine cycle
   - All frequency parameters are relative multiples
   - Example: sine_frequency=0.015 means 0.015 cycles per screen width

4. **Sine Wave Implementation**
   ```python
   sine_offset = sine_amplitude * (1 + np.sin(i * sine_frequency * 2π / width + ...))
   ```
   - Proper sine function with $2\pi$ scaling
   - Adds 1 to keep positive (oscillates between 0 and 2×amplitude)
   - All points oscillate around the center Y

5. **Sawtooth Wave Implementation**
   - Triangle wave that goes up then down symmetrically
   - Starts and ends at center Y
   - Oscillates around center with control points at top and bottom
   - Time-based phase shift for animation

6. **Method Signature Update**
   ```python
   def draw(self, screen, normalized_data, y_offset, amplitude_multiplier, shape="default", 
            current_time=0, max_amplitude=None, shape_params=None, waveform_config=None)
   ```
   - New `waveform_config` parameter for base_frequency and breathing_amplitude
   - Provides defaults if not supplied

#### Breathing Effect
- Reduced `breathing_amplitude` default: 0.15 (was mixed in code)
- Now configurable via `waveform_config`
- Formula: `time_amplitude_factor = 0.7 + breathing_amplitude * sin(current_time * 0.004)`

---

### 3. `face.py` - Configuration-Driven Initialization

**Status**: Refactored to load configuration

#### Constructor Changes:
```python
def __init__(self, x, y, eye_color, mouth_color, background_color, 
             emotion_config, face_config=None, waveform_config=None)
```

#### New Logic:
1. **Load eye configuration from `face_config`**:
   - Eye radius, positions, eyelid starting positions
   - Dynamic initialization based on RABL settings

2. **Load mouth configuration from `face_config`**:
   - Mouth width, Y offset, max amplitude
   - All positioning now data-driven

3. **Store configurations**:
   - `self.emotion_config`: Emotion-specific parameters
   - `self.face_config`: Component positioning
   - `self.waveform_config`: Waveform rendering parameters

#### Draw Method Update:
- Now passes `self.waveform_config` to `mouth.draw()`
- Uses `self.max_amplitude` loaded from config

---

### 4. `main.py` - Full Configuration Loading

**Status**: Refactored to load all settings from RABL

#### Configuration Loading:
```python
config_data = parse_rabl("Animated_Face_FrontEnd/emotions.rabl")

# Extract all sections
display_config = config_data.get('display_config', {})
colors_config = config_data.get('colors', {})
face_config = config_data.get('face_config', {})
audio_config = config_data.get('audio_config', {})
transcription_config = config_data.get('transcription_config', {})
waveform_config = config_data.get('waveform_config', {})
emotion_config_data = config_data.get('emotion_config', {})
```

#### Dynamic Constant Initialization:
- All constants now pulled from RABL configuration
- `WIDTH`, `HEIGHT`: from display_config
- `BACKGROUND_COLOR`, `TEXT_COLOR`: from display_config
- `EYE_COLOR`, `WAVEFORM_COLOR`: from colors
- `EMOTIONS`: dynamically generated from emotion_config keys

#### Audio Configuration:
- `audio_chunk_size`: passed to AudioHandler
- `audio_rate`: passed to AudioHandler
- `audio_channels`: passed to AudioHandler
- `audio_gain_factor`: passed to AudioHandler

#### Transcription Configuration:
- `TRANSCRIBER_BACKEND`: selects "openai" or "faster-whisper"
- `TRANSCRIBER_MODEL`: passes model name to transcriber

#### Component Instantiation:
```python
face = Face(WIDTH // 2, HEIGHT // 2, EYE_COLOR, WAVEFORM_COLOR, BACKGROUND_COLOR, 
           emotion_config_data, face_config, waveform_config)
```

---

### 5. `audio_handler.py` - Parameterized Gain Factor

**Status**: Updated to accept configurable gain

#### Constructor Change:
```python
def __init__(self, ..., gain_factor=1.5)
```

#### Implementation:
- Stores `self.gain_factor` for use in audio processing
- Amplifies audio for transcription: `amplified_data = (data * self.gain_factor).astype(np.int16)`
- Provides consistent, configurable audio amplification

---

## Waveform Mathematics

### Base Frequency System

**Concept**: `base_frequency = 1.0` represents one complete sine cycle across the screen width

$$\text{effective\_frequency} = \text{shape\_frequency} \times \text{base\_frequency}$$

### Sine Waveform
$$y = y_{center} + y_{offset} + A \cdot \sin\left(\frac{2\pi \cdot x \cdot f}{\text{width}} + \phi\right)$$

Where:
- $y_{center}$ = mouth center Y position
- $y_{offset}$ = emotion-specific offset (usually 0)
- $A$ = audio amplitude
- $f$ = frequency parameter (0.015 for IDLE)
- $\phi$ = phase (time-based for animation)

### Parabolic Waveform
$$y = y_{center} + y_{offset} + A \cdot \sin(...) + C \cdot (1 - x_{norm}^2)$$

Where:
- $x_{norm} \in [-1, 1]$ normalized position across width
- $C$ = `curve_factor_intensity` (usually 1.0) × 20 pixels
- Creates a smile/frown shape with sine undulation

### Sawtooth Waveform
$$y = y_{center} + y_{offset} + A \cdot \text{triangle}(\text{phase}) + S \cdot \text{amplitude\_factor}$$

Where:
- Triangle function creates up-then-down motion
- `saw_period_divisor` controls wavelength
- Oscillates around center Y

---

## Configuration Flow Diagram

```
emotions.rabl
    ├── display_config ──────────────→ main.py → Pygame display
    ├── colors ──────────────────────→ main.py → RGB tuples
    ├── face_config ─────────────────→ Face.__init__()
    │   ├── eye config ───────────────→ Eye.__init__() × 2
    │   └── mouth config ────────────→ Mouth.__init__()
    ├── audio_config ────────────────→ AudioHandler.__init__()
    ├── transcription_config ────────→ main.py → Transcriber selection
    ├── waveform_config ────────────→ Face.draw() → Mouth.draw()
    └── emotion_config ─────────────→ Face.set_emotion()
        └── shape_params ───────────→ Mouth.draw() for waveform rendering
```

---

## Benefits of This Refactoring

### 1. **Centralized Configuration Management**
   - Single source of truth: `emotions.rabl`
   - No need to modify Python code for most customizations
   - Runtime configuration changes possible

### 2. **Improved Code Maintainability**
   - Separation of concerns: configuration vs. logic
   - Reduced coupling between components
   - Easier to understand parameter flow

### 3. **Consistent Waveform Behavior**
   - All shapes maintain same Y-center positioning
   - Unified frequency system prevents confusion
   - Predictable animation behavior

### 4. **Enhanced Extensibility**
   - Easy to add new emotions with just RABL entries
   - New mouth shapes can use consistent parameters
   - Audio settings adjustable without code changes

### 5. **Better Performance Tuning**
   - Audio gain, chunk size, sample rate all tunable
   - Transcription interval/overlap configurable
   - Waveform rendering parameters adjustable

---

## Usage Examples

### Adjust Display Resolution
```yaml
display_config:
  width: 1024
  height: 768
```

### Change Audio Amplification
```yaml
audio_config:
  gain_factor: 2.0  # Boost audio input by 2x
```

### Customize Waveform
```yaml
waveform_config:
  base_frequency: 0.5  # Half sine cycle across screen
  breathing_amplitude: 0.25  # More pronounced breathing
```

### Add New Emotion
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

---

## Testing Recommendations

1. **Verify waveform centering**: All waveforms should hover around mouth center
2. **Test frequency scaling**: Change `base_frequency` and confirm animation speed
3. **Check parabolic curvature**: Adjust `curve_factor_intensity` and verify smile shape
4. **Audio levels**: Adjust `gain_factor` and confirm transcription accuracy
5. **Component positioning**: Change `face_config` values and verify visual layout

---

## Migration Notes

If integrating this into existing RABBLE agent systems:

1. **Configuration Loading**: Update integration code to load `emotions.rabl`
2. **Component Creation**: Pass loaded config sections to Face, AudioHandler, etc.
3. **Emotion Control**: Use emotion names from dynamically-generated `EMOTIONS` list
4. **Customization**: All tuning now happens in RABL, not Python code

---

## Future Enhancement Opportunities

1. **Runtime Configuration Reloading**: Reload `emotions.rabl` without restart
2. **Configuration Validation**: Schema validation for RABL files
3. **Preset Packs**: Multiple RABL files for different animation styles
4. **Keyframe Animation**: Time-based configuration transitions
5. **Configuration Export**: Save current settings to new RABL file

---

## Commit Information

- **Commit Hash**: `0ec5781`
- **Branch**: `Speech_to_text_integration`
- **Files Changed**: 6 (emotions.rabl, mouth.py, face.py, main.py, audio_handler.py, uv.lock)
- **Additions**: ~500 lines of configuration and improved code
- **Deletions**: ~60 lines of hardcoded constants

---

For questions or further improvements, refer to the inline documentation in each component and the CODEREVIEW.md file.
