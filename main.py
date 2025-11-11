import pygame
import sys
import pyaudio
import numpy as np
from face import Face

# --- Constants ---
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)  # Black
EYE_COLOR = (150, 75, 150)     # Less saturated magenta
WAVEFORM_COLOR = EYE_COLOR  # Mouth color same as eyes

# --- Audio Settings ---
CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

EMOTIONS = ["HAPPY", "SAD", "ANGRY"]


def main():
    """Main animation loop."""
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Animated Face with Audio Waveform")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Create face with inherited colors from constants
    face = Face(WIDTH // 2, HEIGHT // 2, EYE_COLOR, WAVEFORM_COLOR, BACKGROUND_COLOR)
    
    current_emotion_index = 0
    face.set_emotion(EMOTIONS[current_emotion_index])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    current_emotion_index = (current_emotion_index + 1) % len(EMOTIONS)
                    face.set_emotion(EMOTIONS[current_emotion_index])
                    print(f"Emotion changed to: {face.emotion}")
                elif event.key == pygame.K_t:
                    face.toggle_eyelids()

        face.update()

        screen.fill(BACKGROUND_COLOR)

        try:
            raw_data = stream.read(CHUNK)
            data = np.frombuffer(raw_data, dtype=np.int16)
            normalized_data = data / (2.**15)
            face.draw(screen, normalized_data)
        except IOError as e:
            print(e)

        pygame.display.flip()

    stream.stop_stream()
    stream.close()
    p.terminate()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
