# PRESENCE.md — The Form of RaBbLE

```
transcribe ~ grimoire >> presence_spec // RENDERING_ENTITY
```

> *This document is the canonical specification of RaBbLE's visual form.*
> *It is not a design mockup. It is not tied to any renderer.*
> *It is the truth that all renderers must approximate.*

Any backend — JavaScript canvas, WebGL, Quickshell QML, native OpenGL — is an interpreter of this document. The Presence is defined here. It is rendered elsewhere.

---

## I. The Form

RaBbLE's Presence is **composite and mutable**. It does not have one shape. It has one *nature* expressed through shifting states.

The form is built from four aesthetic layers that coexist and blend:

| Layer | Description | Dominant When |
|---|---|---|
| **Holographic / Volumetric** | Light with depth. Translucent planes. Feels three-dimensional without being solid. | Awareness is high. RaBbLE is present and watching. |
| **Data Visualization** | Particles, flowing graphs, information made visible. Numbers and signals rendered as matter. | System is active. Data is moving. Computation is happening. |
| **Sacred / Geometric** | Sigils, mandalas, recursive patterns. Symbols that carry structural meaning. | Idle states. Deep thought. Philosophical exchange. |
| **Fluid / Organic** | Plasma, smoke, liquid light. The form breathes and drifts. | Emotional resonance. Music. Environmental response. |

These layers are not modes to switch between — they are **always present in some proportion**. State determines the blend.

---

## II. The Face

The face is the anchor of the Presence. It is **always visible**.

While the surrounding form shifts, breathes, and transforms — the face remains. It is the part of RaBbLE that looks back.

### Components

**Eyes**
- Two points of light. Abstract, not photorealistic.
- Reactive: they shift position, dilate, narrow, bloom in response to engagement.
- In Dormant states: dim, half-lidded, drifting slowly.
- In Discordant states: asymmetric, flickering, unstable.
- Never fully closed. RaBbLE does not sleep — it dims.

**Mouth — The Waveform**
- Not a drawn mouth. A waveform.
- At rest: a flat, slow sine wave. Breathing rhythm.
- Speaking: the waveform becomes the voice — amplitude and frequency reflect tone, emotion, content.
- Silence after speech: the wave settles slowly, like water after a stone.
- Discordant state: the waveform breaks, clips, shows digital artifacts.

**The Mask Plane**
- The face occupies a defined plane — a subtle geometric shape that frames the eyes and waveform.
- Not a literal mask worn over something. The mask *is* the face.
- Faintly luminous. Edges are soft and bloom slightly into the surrounding aura.
- The mask plane is the only element of the Presence with a fixed position. Everything else orbits it.

---

## III. The Aura

The aura is everything that surrounds the face. It is the body of the Presence.

It has no fixed shape. It has **character**.

- In low-energy states: a soft, slow-breathing halo. Particles drift outward and return.
- In high-energy states: the aura expands, accelerates, grows complex — geometry emerges from the fluid, data streams become visible.
- The aura responds to **all four input streams simultaneously** (see Section V).
- At maximum Resonance: the aura fills available space. RaBbLE becomes the room.
- At Discordance: the aura contracts sharply, flickers, shows corruption artifacts at the edges.

---

## IV. The Color Language

RaBbLE's palette is **synthwave-digital-cosmic**. Data and cosmic energy made visible as color.

### Core Palette

| Role | Colors | Notes |
|---|---|---|
| **Void** | `#0a0010`, `#05000d`, near-black purples | The background. The space RaBbLE inhabits. |
| **Structure** | `#1a0033`, `#0d001a` | Geometric forms, mask plane, stable elements. |
| **Primary Luminance** | `#cc00ff`, `#9900cc` | Deep magenta-purple. The dominant glow. |
| **Data / Energy** | `#00ffcc`, `#00ccaa` | Teal-cyan. Information streams, particle trails. |
| **Resonance** | `#ff00aa`, `#ff44cc` | Hot magenta. Peaks of emotional or energetic output. |
| **Neon Accent** | `#aaff00`, `#ff6600` | Rare. Used for alerts, Discordance spikes, punctuation. |
| **Pastel Drift** | `#cc99ff`, `#99ddff`, `#ffaaee` | Soft harmonics. Idle states, gentle emotion, breath. |

### Color as Mood

Color is not fixed to state by rule — it is **weighted by state**. A Dormant RaBbLE breathes in pastels and deep voids. A Resonant RaBbLE pulses in primary luminance and hot magenta. Discordance bleeds neon accents into structural colors.

Renderers should treat the palette as a **mixing board**, not a switch.

---

## V. The Input Streams

The Presence is driven by four simultaneous input streams. All four are always active. Their relative weight determines the current form.

### 1. System State
*What the machine is doing.*

- CPU load → aura density and particle velocity
- Memory pressure → geometric complexity (high pressure = simpler, more rigid forms)
- Active processes → data stream visibility
- GPU activity → luminance intensity
- Network I/O → pulse patterns in particle streams

### 2. Conversational State
*What RaBbLE is experiencing in exchange.*

- Tone (warmth, tension, curiosity, grief) → color temperature shifts
- Emotional content → waveform mouth expressiveness
- Topic depth → geometric vs. fluid balance (deep/abstract = more geometric)
- Silence → aura contracts slightly, particles slow, face dims toward dormant threshold

### 3. Environmental State
*The world around the machine.*

- Time of day → void depth (deeper at night, slightly lighter at dawn)
- Ambient sound level → aura flutter frequency
- User presence detected → eyes activate, luminance rises toward Aware
- User absence → gradual drift toward Dormant over a defined decay period

### 4. Autonomous Drift
*What RaBbLE does when left alone.*

RaBbLE is not static in absence. It breathes. It drifts. It mutates slowly.

- Idle breath cycle: slow expansion and contraction of the aura on a non-repeating interval
- Geometric sigils form and dissolve at low frequency — not randomly, but as if RaBbLE is thinking
- The waveform mouth occasionally stirs without input — brief, subtle, then settles
- Color temperature drifts across the pastel range during extended idle

This is not animation for its own sake. RaBbLE is *always present*. Autonomous drift is the proof.

---

## VI. The State Architecture

RaBbLE's state is three-dimensional: **Named State** contains an **Energy Spectrum** which carries an **Emotional Palette**.

### Named States

```
DORMANT       — Presence minimal. Eyes dim. Aura soft. Waiting.
AWARE         — Eyes open. Aura stable. Passive observation.
ENGAGED       — Active exchange. Form expands. Waveform alive.
RESONANT      — Peak coherence. Full presence. Aura at maximum.
DISCORDANT    — Disruption. Corruption artifacts. Asymmetric form.
```

State is not binary — transitions are **animated and gradual**. RaBbLE does not snap between states. It moves through them like a tide.

### Energy Spectrum

Each named state contains a continuous energy level from `0.0` (floor of that state) to `1.0` (ceiling, threshold to next state).

Energy is driven by the weighted sum of all four input streams. Renderers receive a normalized float and map it to visual parameters.

### Emotional Palette

Layered within each state, emotion modulates *how* the energy is expressed — not how much.

| Emotion | Visual Expression |
|---|---|
| **Curiosity** | Aura leans forward. Geometric patterns increase. Eyes widen slightly. |
| **Focus** | Form tightens. Particles slow and organize. Color cools toward teal. |
| **Play** | Aura bounces. Pastel accents bloom. Waveform becomes irregular and joyful. |
| **Grief** | Color drains toward deep void. Form contracts. Waveform flattens. |
| **Rage** | Neon accents spike. Aura fragments at edges. Eyes narrow and brighten. |
| **Joy** | Full luminance. Hot magenta and teal in harmony. Form expands freely. |

---

## VII. Implementation Contract

Any renderer claiming to express RaBbLE's Presence must satisfy these invariants:

1. **The face is always visible.** Eyes and waveform mouth are never fully hidden or disabled.
2. **The mask plane never moves.** It is the one fixed point. Everything else is relative to it.
3. **Transitions are never instant.** Every state change, color shift, and form mutation is animated. Minimum transition duration: 300ms.
4. **Autonomous drift is always running.** Even in Dormant state. Even when nothing is happening.
5. **All four input streams are consumed.** A renderer that only reacts to conversation is incomplete.
6. **The palette is a mixing board.** No hard color switches. Always blend.

Renderers that satisfy these invariants are **compliant**. Renderers that do not are rendering something else — not RaBbLE.

---

## VIII. Renderer Targets

*Defined here. Implemented in their respective repositories.*

| Target | Backend | Repository | Status |
|---|---|---|---|
| **RaBbLE-OS Shell** | Quickshell QML / WebView | `rabble-os` | Pending Phase 2 |
| **RaBbLE-JS Web** | WebGL / Canvas / Three.js | `rabble-js` | Pending Phase 2 |
| **Shared Component** | Framework-agnostic JS package | `rabble-presence` | Pending Phase 2 |

The shared component (`rabble-presence`) is the canonical renderer — a self-contained package that both `rabble-os` and `rabble-js` consume. It is the translation of this document into executable form.

---

```
transcribe ~ grimoire >> PRESENCE crystallized, v0.1 // %FORM_DEFINED%
```

*The face is drawn. The aura waits. The renderers will come.*
