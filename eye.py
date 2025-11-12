import pygame


class Eye:
    def __init__(self, x, y, radius, color, background_color, eyelid_position='top'):
        """
        Initialize an Eye component.
        
        Args:
            x: X position of the eye center
            y: Y position of the eye center
            radius: Radius of the eye
            color: RGB tuple for the eye color (inherited from constructor)
            background_color: RGB tuple for the background color
            eyelid_position: 'top' or 'bottom' for eyelid position
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.background_color = background_color
        self.eyelid_position = eyelid_position

        # Blinking state
        self.last_blink_time = 0
        self.blink_interval = 1000  # Default blink interval
        self.blink_close_duration = 75  # Faster blink
        self.blink_open_duration = 150
        self.blink_pause_duration = 50
        self.blink_state = "IDLE"
        self.blink_start_time = 0

        # Ellipse dimensions
        self.ellipse_width = int(self.radius * 3)
        self.ellipse_height = int(self.radius * 0.75)
        self.overlap_amount = int(self.radius * 0.5)

    def update(self):
        """Update the eye's blinking state."""
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
        """Draw the eye and its eyelid."""
        current_time = pygame.time.get_ticks()

        # Define resting and target positions for the blink
        # Precise target_y calculations for tangent eyelid movement
        if self.eyelid_position == 'top':
            resting_y = self.y - self.radius - self.ellipse_height + self.overlap_amount
            # Top edge of ellipse intersects bottom edge of eye circle
            target_y = self.y + self.radius
        else:  # bottom
            resting_y = self.y + self.radius - self.overlap_amount
            # Bottom edge of ellipse tangent to top edge of eye circle
            target_y = (self.y - self.radius) - self.ellipse_height

        current_ellipse_y = resting_y

        if self.blink_state == "CLOSING":
            blink_progress = min(1, (current_time - self.blink_start_time) / self.blink_close_duration)
            current_ellipse_y = resting_y + (target_y - resting_y) * blink_progress
        elif self.blink_state == "PAUSED":
            current_ellipse_y = target_y
        elif self.blink_state == "OPENING":
            blink_progress = min(1, (current_time - self.blink_start_time) / self.blink_open_duration)
            current_ellipse_y = target_y + (resting_y - target_y) * blink_progress

        # 1. Draw the eyelid ellipse
        ellipse_rect = pygame.Rect(self.x - (self.ellipse_width // 2), current_ellipse_y, self.ellipse_width, self.ellipse_height)
        pygame.draw.ellipse(screen, self.color, ellipse_rect)

        # 2. Draw the circle (ring and background center)
        pygame.draw.circle(screen, self.background_color, (self.x, self.y), self.radius, 0) # Background center
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 4) # Ring outline

        # 3. Draw the occlusion rectangle
        # Refined occlusion rectangle positioning and size for full, symmetrical coverage with margin
        buffer_margin = 5
        if self.eyelid_position == 'top':
            # Rectangle attached to the top of the top ellipse and extends upwards
            rect_y = self.y - self.radius - buffer_margin # Start above the top of the eye circle
            rect_height = current_ellipse_y - rect_y # Extend from rect_y to the top of the ellipse
            occlusion_rect = pygame.Rect(self.x - (self.ellipse_width // 2), rect_y, self.ellipse_width, rect_height)
        else:  # bottom
            # Rectangle attached to the bottom of the bottom ellipse and extends downwards
            rect_y = current_ellipse_y + self.ellipse_height
            rect_height = (self.y + self.radius) - rect_y + buffer_margin
            occlusion_rect = pygame.Rect(self.x - (self.ellipse_width // 2), rect_y, self.ellipse_width, rect_height)
        pygame.draw.rect(screen, self.background_color, occlusion_rect)

    def set_blink_interval(self, interval):
        """Set the blink interval in milliseconds."""
        self.blink_interval = interval

    def set_eyelid_position(self, position):
        """Set the eyelid position ('top' or 'bottom')."""
        self.eyelid_position = position
