import pygame
import sys
import pyaudio
import numpy as np

# --- Constants ---
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)  # Black
EYE_COLOR = (150, 75, 150)     # Less saturated magenta
MOUTH_COLOR = (0, 0, 0)       # Black (no longer used for mouth)
WAVEFORM_COLOR = EYE_COLOR  # Mouth color same as eyes

# --- Audio Settings ---
CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# --- Main Application ---
def main():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Animated Face with Audio Waveform")

    # --- Audio Stream ---
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Main loop
    running = True
    last_blink_time = 0
    blink_interval = 1000  # Time between blinks (in ms), very fast
    blink_close_duration = 75  # How long the blink closing lasts (in ms)
    blink_open_duration = 75 # How long the blink opening lasts (in ms)
    blink_pause_duration = 50 # How long eyes stay closed (in ms)

    blink_state = "IDLE" # IDLE, CLOSING, PAUSED, OPENING
    blink_start_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Blinking Logic ---
        current_time = pygame.time.get_ticks()

        if blink_state == "IDLE":
            if current_time - last_blink_time > blink_interval:
                blink_state = "CLOSING"
                blink_start_time = current_time
        elif blink_state == "CLOSING":
            if current_time - blink_start_time > blink_close_duration:
                blink_state = "PAUSED"
                blink_start_time = current_time
        elif blink_state == "PAUSED":
            if current_time - blink_start_time > blink_pause_duration:
                blink_state = "OPENING"
                blink_start_time = current_time
        elif blink_state == "OPENING":
            if current_time - blink_start_time > blink_open_duration:
                blink_state = "IDLE"
                last_blink_time = current_time # Reset for next blink

        # --- Drawing ---
        # Background
        screen.fill(BACKGROUND_COLOR)

        # Eyes
        eye_radius = 30 # Increased eye size
        face_x = WIDTH // 2 # Keep face_x for eye positioning
        face_y = HEIGHT // 2 # Centered face vertically
        left_eye_x = face_x - 60 # Adjusted eye separation
        right_eye_x = face_x + 60 # Adjusted eye separation
        eye_y = face_y - 40 # Adjusted eye vertical position
        
        # Ellipse dimensions (defined here for use in animation)
        ellipse_width = int(eye_radius * 3)
        ellipse_height = int(eye_radius * 0.75)
        overlap_amount = int(eye_radius * 0.5)

        # Calculate initial ellipse positions (idle state)
        initial_right_ellipse_y = eye_y - eye_radius - ellipse_height + overlap_amount
        initial_left_ellipse_y = eye_y + eye_radius - overlap_amount

        # Calculate target ellipse positions (closed state)
        closed_right_ellipse_y = eye_y + eye_radius - ellipse_height # Target to fully cover the eye
        closed_left_ellipse_y = eye_y - eye_radius # Target to fully cover the eye

        current_right_ellipse_y = initial_right_ellipse_y
        current_left_ellipse_y = initial_left_ellipse_y

        blink_progress = 0.0
        if blink_state == "CLOSING":
            blink_progress = min(1, (current_time - blink_start_time) / blink_close_duration)
            current_right_ellipse_y = initial_right_ellipse_y + (closed_right_ellipse_y - initial_right_ellipse_y) * blink_progress
            current_left_ellipse_y = initial_left_ellipse_y + (closed_left_ellipse_y - initial_left_ellipse_y) * blink_progress
        elif blink_state == "OPENING":
            blink_progress = min(1, (current_time - blink_start_time) / blink_open_duration)
            # Reverse animation: interpolate from closed position back to initial
            current_right_ellipse_y = closed_right_ellipse_y + (initial_right_ellipse_y - closed_right_ellipse_y) * blink_progress
            current_left_ellipse_y = closed_left_ellipse_y + (initial_left_ellipse_y - closed_left_ellipse_y) * blink_progress
        elif blink_state == "PAUSED":
            current_right_ellipse_y = closed_right_ellipse_y
            current_left_ellipse_y = closed_left_ellipse_y

        # --- Drawing Order based on blink_state ---
        if blink_state == "IDLE" or blink_state == "OPENING":
            # Draw ellipses first (static or animating back to idle)
            right_eye_ellipse_rect = pygame.Rect(right_eye_x - (ellipse_width // 2), current_right_ellipse_y, ellipse_width, ellipse_height)
            pygame.draw.ellipse(screen, EYE_COLOR, right_eye_ellipse_rect)
            left_eye_ellipse_rect = pygame.Rect(left_eye_x - (ellipse_width // 2), current_left_ellipse_y, ellipse_width, ellipse_height)
            pygame.draw.ellipse(screen, EYE_COLOR, left_eye_ellipse_rect)

            # Then draw eyes on top, with black fill to slightly overlap
            pygame.draw.circle(screen, BACKGROUND_COLOR, (left_eye_x, eye_y), eye_radius, 0) # Filled black circle
            pygame.draw.circle(screen, BACKGROUND_COLOR, (right_eye_x, eye_y), eye_radius, 0) # Filled black circle
            pygame.draw.circle(screen, EYE_COLOR, (left_eye_x, eye_y), eye_radius, 4) # Outline
            pygame.draw.circle(screen, EYE_COLOR, (right_eye_x, eye_y), eye_radius, 4) # Outline
        else: # CLOSING or PAUSED
            # Draw eyes first (static)
            pygame.draw.circle(screen, BACKGROUND_COLOR, (left_eye_x, eye_y), eye_radius, 0) # Filled black circle
            pygame.draw.circle(screen, BACKGROUND_COLOR, (right_eye_x, eye_y), eye_radius, 0) # Filled black circle
            pygame.draw.circle(screen, EYE_COLOR, (left_eye_x, eye_y), eye_radius, 4) # Outline
            pygame.draw.circle(screen, EYE_COLOR, (right_eye_x, eye_y), eye_radius, 4) # Outline

            # Then draw ellipses on top (animating to cover eyes or paused covering eyes)
            # Clear the area where the ellipses will move to prevent ghosting
            # This needs to be done before drawing the ellipses to ensure proper animation
            clear_right_rect_y = min(initial_right_ellipse_y, closed_right_ellipse_y)
            clear_right_rect_height = ellipse_height + abs(closed_right_ellipse_y - initial_right_ellipse_y)
            pygame.draw.rect(screen, BACKGROUND_COLOR, (right_eye_x - (ellipse_width // 2), clear_right_rect_y, ellipse_width, clear_right_rect_height))
            
            clear_left_rect_y = min(initial_left_ellipse_y, closed_left_ellipse_y)
            clear_left_rect_height = ellipse_height + abs(closed_left_ellipse_y - initial_left_ellipse_y)
            pygame.draw.rect(screen, BACKGROUND_COLOR, (left_eye_x - (ellipse_width // 2), clear_left_rect_y, ellipse_width, clear_left_rect_height))

            right_eye_ellipse_rect = pygame.Rect(right_eye_x - (ellipse_width // 2), current_right_ellipse_y, ellipse_width, ellipse_height)
            pygame.draw.ellipse(screen, EYE_COLOR, right_eye_ellipse_rect)
            left_eye_ellipse_rect = pygame.Rect(left_eye_x - (ellipse_width // 2), current_left_ellipse_y, ellipse_width, ellipse_height)
            pygame.draw.ellipse(screen, EYE_COLOR, left_eye_ellipse_rect)

        # --- Audio Processing ---

        # --- Audio Processing ---
        try:
            raw_data = stream.read(CHUNK)
            data = np.frombuffer(raw_data, dtype=np.int16)
            
            # Normalize data for waveform and mouth animation
            normalized_data = data / (2.**15)
            
            # --- Drawing ---
            # (already done: background, eyes)

            # Waveform as Mouth
            # Position the waveform where the mouth used to be
            mouth_waveform_y_center = face_y + 80 # Center of the mouth area, adjusted for centered face
            
            points = []
            # Scale the waveform more for a larger amplitude
            # Use a subset of data to fit the mouth width
            mouth_width = 300 # Increased mouth width to make it longer
            start_index = len(normalized_data) // 2 - (mouth_width // 2)
            end_index = len(normalized_data) // 2 + (mouth_width // 2)
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(face_x - (mouth_width // 2) + (i / mouth_width * mouth_width))
                y = int(mouth_waveform_y_center + sample * 200) # Increased scaling for amplitude
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(screen, WAVEFORM_COLOR, False, points, 4) # Thicker line for mouth, increased definition

        except IOError as e:
            print(e)


        # Update the display
        pygame.display.flip()

    # --- Cleanup ---
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
