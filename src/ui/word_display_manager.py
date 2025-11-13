import pygame
from collections import deque
import queue # Import queue for thread-safe communication
import threading # Import threading for Event

class WordDisplayManager:
    """
    Manages the display of transcribed words, including scrolling,
    appearing at a uniform rate, and disappearing at screen margins.
    The display is anchored to the center, with new words added to the front
    and existing words moving back.
    """
    def __init__(self, font, text_color, screen_width, screen_height,
                 scroll_speed=70, word_display_interval_ms=150, display_text_y_offset=50,
                 transcribed_text_queue=None, text_start_offset=50,
                 transcriber_ready_event=None): # New parameter for transcriber ready event
        self.font = font
        self.text_color = text_color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed = scroll_speed # pixels per second
        self.word_display_interval_ms = word_display_interval_ms
        self.display_text_y_offset = display_text_y_offset
        self.line_height = self.font.get_linesize() # Get line height for vertical positioning

        self.active_display_words = deque() # Stores {'text': 'word', 'x': x_pos, 'width': word_width}
        self.pending_display_words = deque() # Stores words waiting to be displayed
        self.last_word_display_time = pygame.time.get_ticks()
        self.current_line_width = 0 # Track width of words on the current line
        self.word_spacing = 10 # Pixels between words
        self.transcribed_text_queue = transcribed_text_queue # Store the queue
        self.text_start_offset = text_start_offset # Offset from center for new words
        self.transcriber_ready_event = transcriber_ready_event # Store the event

    def update(self, delta_time):
        """
        Updates the position of active words and moves new words from pending to active.
        Also pulls new transcribed text from the queue.
        delta_time is in milliseconds.
        """
        # Only process transcribed words if the transcriber is ready
        if not self.transcriber_ready_event.is_set():
            return # Do not update words if transcriber is not ready

        # Pull new transcribed text from the queue and add to pending_display_words
        while not self.transcribed_text_queue.empty():
            text = self.transcribed_text_queue.get()
            words = text.split()
            for word in words:
                self.pending_display_words.append(word)

        # Add new words from pending to active at a uniform rate
        current_time = pygame.time.get_ticks()
        if self.pending_display_words and (current_time - self.last_word_display_time) >= self.word_display_interval_ms:
            new_word_text = self.pending_display_words.popleft()
            word_surface = self.font.render(new_word_text, True, self.text_color)
            word_width = word_surface.get_width()

            # Add new word to the right of the last word, or at the center + offset if it's the first word
            if not self.active_display_words:
                new_word_x = self.screen_width / 2 + self.text_start_offset
            else:
                last_word = self.active_display_words[-1]
                new_word_x = last_word['x'] + last_word['width'] + self.word_spacing
            
            self.active_display_words.append({
                'text': new_word_text,
                'x': new_word_x,
                'width': word_width
            })
            self.last_word_display_time = current_time

        # Update positions of active words (scroll left)
        scroll_amount = (self.scroll_speed * delta_time) / 1000.0 # pixels per millisecond
        for word_data in self.active_display_words:
            word_data['x'] -= scroll_amount

        # Remove words that have scrolled off the left margin
        while self.active_display_words and (self.active_display_words[0]['x'] + self.active_display_words[0]['width']) < 0:
            self.active_display_words.popleft()

        # Remove words that have scrolled off the right margin (if they were added far right)
        while self.active_display_words and self.active_display_words[-1]['x'] > self.screen_width:
            self.active_display_words.pop()


    def draw(self, screen):
        """
        Draws all active words on the screen, centered vertically.
        If the transcriber is not ready, it draws a loading message instead.
        """
        if not self.transcriber_ready_event.is_set():
            loading_message = "Initializing Transcription..."
            loading_surface = self.font.render(loading_message, True, self.text_color)
            loading_rect = loading_surface.get_rect(center=(self.screen_width // 2, self.screen_height - self.display_text_y_offset))
            screen.blit(loading_surface, loading_rect)
            return

        # Calculate the total width of all active words to center them
        total_words_width = sum(word['width'] for word in self.active_display_words) + \
                            max(0, len(self.active_display_words) - 1) * self.word_spacing
        
        # The y position is fixed at the bottom of the screen
        text_y = self.screen_height - self.display_text_y_offset - self.line_height / 2 # Center vertically on the line

        for word_data in self.active_display_words:
            word_surface = self.font.render(word_data['text'], True, self.text_color)
            screen.blit(word_surface, (int(word_data['x']), int(text_y)))
