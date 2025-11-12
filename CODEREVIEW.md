# RABBLE Animated Face Frontend - Code Review & Architecture Guide

This document provides a comprehensive overview of the codebase structure, component relationships, and design patterns to help developers quickly understand and extend the system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Documentation](#component-documentation)
3. [File Structure](#file-structure)
4. [Data Flow](#data-flow)
5. [Extending the System](#extending-the-system)
6. [Key Design Patterns](#key-design-patterns)

---

## Architecture Overview

The RABBLE Animated Face Frontend follows a **modular, hierarchical component model**:

```
┌─────────────────────────────────────────┐
│          main.py                        │
│    (Animation Loop & Audio I/O)         │
│                                         │
│  - Pygame initialization                │
│  - PyAudio stream management            │
│  - Event handling (keyboard input)      │
│  - Main render loop                     │
└────────────────┬────────────────────────┘
                 │ creates & updates
                 ↓
┌─────────────────────────────────────────┐
│          Face                           │
│    (Emotion & Component Manager)        │
│                                         │
│  - Manages emotional state              │
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
- **Separation of Concerns**: Each component has a single, well-defined responsibility
- **Color Inheritance**: Colors are passed via constructor, allowing easy theming
- **State Management**: Components maintain their own state (blink timers, animations)
- **Time-Based Animation**: Uses `pygame.time.get_ticks()` for smooth, frame-rate-independent animations

---

## Component Documentation

### 1. `main.py` - Animation Loop & Audio I/O

**Responsibility**: Orchestrate the application lifecycle, handle user input, and manage audio streaming.

**Key Constants**:
```python
WIDTH, HEIGHT = 800, 600              # Display resolution
BACKGROUND_COLOR = (0, 0, 0)          # Black background
EYE_COLOR = (150, 75, 150)            # Magenta eyes
WAVEFORM_COLOR = EYE_COLOR            # Mouth color (same as eyes)

CHUNK = 1024 * 2                      # Audio buffer size
FORMAT = pyaudio.paInt16              # 16-bit audio format
CHANNELS = 1                          # Mono audio
RATE = 44100                          # Sample rate (44.1 kHz)

EMOTIONS = ["IDLE", "HAPPY", "SAD", "ANGRY"]  # Available emotions
```

**Main Functions**:
- `main()`: Core application loop
  - Initializes Pygame and PyAudio
  - Creates Face component with color parameters
  - Handles events (quit, emotion cycling, eyelid toggle)
  - Reads audio input and passes to Face for rendering
  - Manages display updates

**Event Handling**:
- **QUIT**: Exit application
- **KEY_M**: Cycle through emotions
- **KEY_T**: Toggle eyelid positions

**Audio Processing**:
- Reads audio chunks from microphone via PyAudio
- Converts raw bytes to numpy array
- Normalizes to range [-1, 1]
- Passes normalized data to `Face.draw()` for visualization

---

### 2. `face.py` - Face Component (Emotion Manager)

**Responsibility**: Manage overall emotional state and coordinate rendering of Eye and Mouth components.

**Constructor**:
```python
Face(x, y, eye_color, mouth_color, background_color)
```

**Parameters**:
- `x, y`: Center position of the face on screen
- `eye_color`: RGB tuple for eye color (inherited from constants)
- `mouth_color`: RGB tuple for mouth color (inherited from constants)
- `background_color`: RGB tuple for background (inherited from constants)

**Key Attributes**:
```python
self.emotion                    # Current emotion state
self.left_eye, self.right_eye   # Eye components (with asymmetric eyelid positions)
self.mouth                      # Mouth component
```

**Public Methods**:

| Method | Purpose |
|--------|---------|
| `set_emotion(emotion)` | Set face emotion and update blink intervals |
| `toggle_eyelids()` | Swap eyelid positions (for asymmetrical expressions) |
| `update()` | Update component states (call once per frame) |
| `draw(screen, normalized_data, current_time)` | Render face with emotion-specific mouth shapes |

**Emotion Behaviors**:

| Emotion | Blink Rate | Mouth Shape | Details |
|---------|-----------|-------------|---------|
| IDLE | 1000ms | Sine wave (subtle) | Slight undulating breathing effect |
| HAPPY | 1000ms | Parabolic (upward) | Cheerful, curved mouth shape; amplitude 500 |
| SAD | 2000ms | Parabolic (downward) | Slower blinking; inverted parabola; amplitude 500 |
| ANGRY | 500ms | Sawtooth | Rapid blinking; aggressive jagged pattern; amplitude 800 |

**Color Inheritance Example**:
```python
face = Face(400, 300, (150, 75, 150), (150, 75, 150), (0, 0, 0))
# Colors flow to:
# - left_eye.color = (150, 75, 150)
# - right_eye.color = (150, 75, 150)
# - mouth.color = (150, 75, 150)
```

---

### 3. `eye.py` - Eye Component (Blinking & Rendering)

**Responsibility**: Render individual eye with realistic blinking animation and asymmetric eyelid positioning.

**Constructor**:
```python
Eye(x, y, radius, color, background_color, eyelid_position='top')
```

**Parameters**:
- `x, y`: Center position of eye
- `radius`: Eye circle radius (default: 30px)
- `color`: RGB tuple for eye/eyelid color (inherited)
- `background_color`: RGB tuple for background (for masking)
- `eyelid_position`: 'top' or 'bottom' for asymmetric expressions

**Blink State Machine**:
```
IDLE → CLOSING → PAUSED → OPENING → IDLE
```

**Blink Timing Parameters**:
```python
blink_interval = 1000      # Wait time before next blink (emotion-dependent)
blink_close_duration = 75  # Time to close (75ms = 3 frames at 60fps)
blink_open_duration = 150  # Time to open (150ms = 6 frames at 60fps)
blink_pause_duration = 50  # Time paused closed (50ms)
```

**Rendering Process**:
1. **Draw Eyelid Ellipse**: Moves vertically to cover eye
2. **Draw Eye Circle**: White background + magenta ring
3. **Draw Occlusion Rectangle**: Masks eyelid movement

**Key Methods**:

| Method | Purpose |
|--------|---------|
| `update()` | Update blink state based on timing |
| `draw(screen)` | Render eye with current blink state |
| `set_blink_interval(interval)` | Change blink rate |
| `set_eyelid_position(position)` | Switch eyelid to 'top' or 'bottom' |

**Eyelid Position Logic**:
- **Top Eyelid**: Closes from above, rests above eye
- **Bottom Eyelid**: Closes from below, rests below eye
- Asymmetric positioning allows expressive faces (e.g., winking effect)

---

### 4. `mouth.py` - Mouth Component (Audio Visualization)

**Responsibility**: Render mouth shape based on audio input, with emotion-specific waveform shapes and breathing effects.

**Constructor**:
```python
Mouth(x, y, width, color)
```

**Parameters**:
- `x, y`: Center position of mouth
- `width`: Horizontal width of waveform (default: 300px)
- `color`: RGB tuple for mouth color (inherited)

**Waveform Shapes**:

| Shape | Description | Usage | Effect |
|-------|-------------|-------|--------|
| `"default"` | Raw audio waveform | Neutral/default | Direct audio visualization |
| `"parabolic"` | Curved parabola with audio | HAPPY/SAD | Expressive curve; upward or downward |
| `"sine"` | Smooth sine wave undulation | IDLE | Subtle breathing animation |
| `"saw"` | Sawtooth pattern with motion | ANGRY | Aggressive, jagged appearance |

**Animation Features**:
- **Time-Based Amplitude Factor**: `0.7 + 0.3 * sin(time * 0.002)` creates subtle breathing effect
- **Frequency Modulation**: Different frequencies for different shapes
- **Audio Sync**: Real-time response to audio input with multiplier parameters

**Key Methods**:

| Method | Purpose |
|--------|---------|
| `draw(screen, normalized_data, y_offset, amplitude_multiplier, shape, current_time)` | Render mouth |

**Parameter Details**:
- `normalized_data`: Audio array from [-1, 1]
- `y_offset`: Vertical offset baseline (e.g., -40 for SAD, +40 for HAPPY)
- `amplitude_multiplier`: Scaling factor (e.g., 200-800 depending on emotion)
- `shape`: Waveform type ('default', 'parabolic', 'sine', 'saw')
- `current_time`: Milliseconds for time-based animations

---

## File Structure

```
Animated_Face_FrontEnd/
├── main.py                    # Entry point, animation loop, audio I/O
├── face.py                    # Face component (emotion manager)
├── eye.py                     # Eye component (blinking, rendering)
├── mouth.py                   # Mouth component (audio visualization)
├── requirements.txt           # Python dependencies
├── README.md                  # User-facing documentation
└── CODEREVIEW.md             # This file (developer guide)
```

---

## Data Flow

### Per-Frame Execution Order

```
1. main.py: Handle Events
   ├─ Check for quit
   ├─ Check for emotion change
   └─ Check for eyelid toggle

2. main.py: Update State
   └─ face.update()
       ├─ left_eye.update()   (check blink timing)
       └─ right_eye.update()  (check blink timing)

3. main.py: Read Audio
   ├─ stream.read(CHUNK)      (get raw audio)
   ├─ normalize to [-1, 1]
   └─ pass to face.draw()

4. face.py: Draw Components
   ├─ left_eye.draw(screen)
   ├─ right_eye.draw(screen)
   └─ mouth.draw(screen, ...)  (with emotion-specific params)

5. main.py: Display Update
   └─ pygame.display.flip()
```

### Audio Data Pipeline

```
Microphone
    ↓
PyAudio.stream.read() → raw bytes
    ↓
np.frombuffer() → int16 array
    ↓
Normalize by 2^15 → float array [-1, 1]
    ↓
mouth.draw() processes each sample
    ↓
Display as waveform on screen
```

---

## Extending the System

### Adding a New Emotion

1. **Add to EMOTIONS list** in `main.py`:
```python
EMOTIONS = ["IDLE", "HAPPY", "SAD", "ANGRY", "SURPRISED"]
```

2. **Update `Face.set_emotion()`** in `face.py`:
```python
def set_emotion(self, emotion):
    self.emotion = emotion
    if self.emotion == "SURPRISED":
        self.left_eye.set_blink_interval(300)   # Fast blinking
        self.right_eye.set_blink_interval(300)
    # ... other emotions ...
```

3. **Define rendering** in `Face.draw()`:
```python
elif self.emotion == "SURPRISED":
    self.mouth.draw(screen, normalized_data, 20, 600, "parabolic", current_time)
```

### Adding a New Mouth Shape

1. **Implement in `mouth.py`** `draw()` method:
```python
elif shape == "triangle":
    # Your triangle waveform logic here
    for i, sample in enumerate(normalized_data[start_index:end_index]):
        x = int(self.x - (self.width // 2) + (i / self.width * self.width))
        # Calculate triangle pattern
        y = int(self.y + sample * amplitude_multiplier)
        points.append((x, y))
```

2. **Use in emotion** in `face.py`:
```python
elif self.emotion == "CUSTOM":
    self.mouth.draw(screen, normalized_data, 0, 400, "triangle", current_time)
```

### Changing Colors Dynamically

```python
# Modify constants in main.py or pass new colors to Face:
face2 = Face(400, 300, (0, 255, 0), (0, 255, 0), (255, 255, 255))  # Green on white
```

### Adjusting Blink Speed

```python
# In main.py during setup:
face.left_eye.set_blink_interval(2000)   # 2 seconds between blinks
face.right_eye.set_blink_interval(2000)
```

---

## Key Design Patterns

### 1. **Component-Based Architecture**
- Each component (Eye, Mouth) is self-contained
- Components don't directly interact; Face coordinates them
- Promotes reusability and testability

### 2. **Color Inheritance**
- Colors passed from main.py → Face → Components
- Allows easy theming without modifying component code
- Constants centralized in one location

### 3. **State Machine (Blinking)**
- Explicit states: IDLE, CLOSING, PAUSED, OPENING
- Time-based transitions prevent frame-rate dependency
- Easy to visualize and debug

### 4. **Time-Based Animation**
- Uses `pygame.time.get_ticks()` (milliseconds elapsed)
- Frame-rate independent
- Smooth interpolation between states

### 5. **Data Normalization**
- Audio normalized to [-1, 1] range
- Components work with normalized data
- Easy to scale with amplitude multipliers

### 6. **Modular Shapes**
- Waveform shapes defined as separate branches in `mouth.draw()`
- Easy to add new shapes without affecting existing code
- Each shape can have custom time-based animations

---

## Performance Considerations

- **Audio Buffer Size**: 1024*2 samples provides good balance between responsiveness and CPU usage
- **Draw Calls**: Minimal per frame (2 circles + lines per component)
- **Pygame Rendering**: Hardware-accelerated on most systems
- **Suitable for Edge Devices**: Lightweight enough for Raspberry Pi, Jetson Nano, etc.

---

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| No audio visualization | PyAudio stream closed | Check microphone is connected and permissions granted |
| Eyes appear static | Blink interval very long | Check `set_emotion()` is being called correctly |
| Mouth is distorted | Negative array indexing | Ensure audio buffer size is larger than mouth width |
| Choppy animation | Low framerate | Reduce display resolution or close other apps |
| Colors not applying | Wrong emotion state | Verify emotion is set via keyboard input (press M) |

---

## Integration Notes

When integrating into RABBLE agent:

1. **Emotion Control**: Call `face.set_emotion(emotion_name)` from agent logic
2. **Audio Passthrough**: Route agent's audio output to system microphone or pipe PyAudio input
3. **Headless Mode**: Could be adapted to render to file/network stream instead of display
4. **Message Broadcasting**: Add event system to broadcast face state to other agent components

---

For questions or contributions, refer back to this document and the inline code documentation in each component.
