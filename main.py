import pygame
import sys
import pyaudio
import numpy as np

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

class Eye:
    def __init__(self, x, y, radius, color, background_color, eyelid_position='top'):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.background_color = background_color
        self.eyelid_position = eyelid_position

        # Blinking state
        self.last_blink_time = 0
        self.blink_interval = 1000  # Default blink interval
        self.blink_close_duration = 150
        self.blink_open_duration = 150
        self.blink_pause_duration = 50
        self.blink_state = "IDLE"
        self.blink_start_time = 0

        # Ellipse dimensions
        self.ellipse_width = int(self.radius * 3)
        self.ellipse_height = int(self.radius * 0.75)
        self.overlap_amount = int(self.radius * 0.5)

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.blink_state == "IDLE":
            if current_time - self.last_blink_time > self.blink_interval:
                self.blink_state = "CLOSING"
                self.blink_start_time = current_time
        elif self.blink_state == "CLOSING":
            if current_time - self.blink_start_time > self.blink_close_duration:
                self.blink_state = "PAUSED"
                self.blink_start_time = current_time
        elif self.blink_state == "PAUSED":
            if current_time - self.blink_start_time > self.blink_pause_duration:
                self.blink_state = "OPENING"
                self.blink_start_time = current_time
        elif self.blink_state == "OPENING":
            if current_time - self.blink_start_time > self.blink_open_duration:
                self.blink_state = "IDLE"
                self.last_blink_time = current_time

    def draw(self, screen):
        current_time = pygame.time.get_ticks()

        # Define resting and target positions for the blink
        if self.eyelid_position == 'top':
            resting_y = self.y - self.radius - self.ellipse_height + self.overlap_amount
            target_y = self.y + self.radius - self.ellipse_height
        else: # bottom
            resting_y = self.y + self.radius - self.overlap_amount
            target_y = self.y - self.radius

        current_ellipse_y = resting_y

        if self.blink_state == "CLOSING":
            blink_progress = min(1, (current_time - self.blink_start_time) / self.blink_close_duration)
            current_ellipse_y = resting_y + (target_y - resting_y) * blink_progress
        elif self.blink_state == "PAUSED":
            current_ellipse_y = target_y
        elif self.blink_state == "OPENING":
            blink_progress = min(1, (current_time - self.blink_start_time) / self.blink_open_duration)
            current_ellipse_y = target_y + (resting_y - target_y) * blink_progress

        # Draw the eyelid and its mask
        ellipse_rect = pygame.Rect(self.x - (self.ellipse_width // 2), current_ellipse_y, self.ellipse_width, self.ellipse_height)
        pygame.draw.ellipse(screen, self.color, ellipse_rect)
        
        # Draw the eye on top
        pygame.draw.circle(screen, self.background_color, (self.x, self.y), self.radius, 0)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 4)

class Mouth:
    def __init__(self, x, y, width, color):
        self.x = x
        self.y = y
        self.width = width
        self.color = color

    def draw(self, screen, normalized_data, y_offset, amplitude_multiplier, shape="default"):
        points = []
        start_index = len(normalized_data) // 2 - (self.width // 2)
        end_index = len(normalized_data) // 2 + (self.width // 2)
        
        if shape == "parabolic":
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                curve_factor = 1 - (abs(i - (self.width // 2)) / (self.width // 2))**2
                y = int(self.y + y_offset * curve_factor + sample * amplitude_multiplier)
                points.append((x, y))
        elif shape == "saw":
            saw_period = self.width // 4
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                pos_in_cycle = i % saw_period
                if pos_in_cycle < saw_period / 2:
                    saw_offset = (pos_in_cycle / (saw_period / 2)) * 40
                else:
                    saw_offset = (1 - ((pos_in_cycle - (saw_period / 2)) / (saw_period / 2))) * 40
                y = int(self.y - saw_offset + sample * amplitude_multiplier)
                points.append((x, y))
        else: # Default
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                y = int(self.y + sample * amplitude_multiplier)
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, self.color, False, points, 4)

class Face:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.emotion = "HAPPY"
        
        eye_radius = 30
        self.left_eye = Eye(x - 60, y - 40, eye_radius, EYE_COLOR, BACKGROUND_COLOR, 'bottom')
        self.right_eye = Eye(x + 60, y - 40, eye_radius, EYE_COLOR, BACKGROUND_COLOR, 'top')
        self.mouth = Mouth(x, y + 80, 300, WAVEFORM_COLOR)

    def set_emotion(self, emotion):
        self.emotion = emotion
        if self.emotion == "ANGRY":
            self.left_eye.blink_interval = 500
            self.right_eye.blink_interval = 500
        elif self.emotion == "SAD":
            self.left_eye.blink_interval = 2000
            self.right_eye.blink_interval = 2000
        else: # HAPPY
            self.left_eye.blink_interval = 1000
            self.right_eye.blink_interval = 1000

    def toggle_eyelids(self):
        if self.left_eye.eyelid_position == 'bottom':
            self.left_eye.eyelid_position = 'top'
            self.right_eye.eyelid_position = 'bottom'
        else:
            self.left_eye.eyelid_position = 'bottom'
            self.right_eye.eyelid_position = 'top'

    def update(self):
        self.left_eye.update()
        self.right_eye.update()

    def draw(self, screen, normalized_data):
        self.left_eye.draw(screen)
        self.right_eye.draw(screen)

        if self.emotion == "SAD":
            self.mouth.draw(screen, normalized_data, -40, 500, "parabolic")
        elif self.emotion == "HAPPY":
            self.mouth.draw(screen, normalized_data, 40, 500, "parabolic")
        elif self.emotion == "ANGRY":
            self.mouth.draw(screen, normalized_data, 0, 800, "saw")
        else:
            self.mouth.draw(screen, normalized_data, 0, 500)

# --- Main Application ---
def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Animated Face with Audio Waveform")

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    face = Face(WIDTH // 2, HEIGHT // 2)
    
    EMOTIONS = ["HAPPY", "SAD", "ANGRY"]
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
