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
                 transcriber_ready_event=None, is_transcriber_paused_func=None,
                 llm_agent_input_queue=None, llm_agent_output_queue=None): # New parameter for LLM agent input/output queues
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
        self.is_transcriber_paused_func = is_transcriber_paused_func # Function to check if transcriber is paused
        self.llm_agent_input_queue = llm_agent_input_queue # Store LLM agent input queue
        self.llm_agent_output_queue = llm_agent_output_queue # Store LLM agent output queue
        self.llm_response_display_queue = deque() # Stores LLM responses for display
        self.last_llm_response_time = pygame.time.get_ticks()
        self.llm_response_display_interval_ms = 200 # Interval for displaying LLM response words

        # Text input field variables
        self.input_box_active = False
        self.input_text = ""
        self.input_font = pygame.font.Font(None, 32)
        self.input_box_rect = pygame.Rect(50, self.screen_height - 40, self.screen_width - 100, 30)
        self.input_box_color_inactive = (100, 100, 100)
        self.input_box_color_active = (200, 200, 200)
        self.input_box_color = self.input_box_color_inactive

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

        # Pull new LLM agent responses from the queue and add to llm_response_display_queue
        while self.llm_agent_output_queue and not self.llm_agent_output_queue.empty():
            response_text = self.llm_agent_output_queue.get()
            response_words = response_text.split()
            for word in response_words:
                self.llm_response_display_queue.append(word)

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


    def draw(self, screen, current_time): # Pass current_time to draw
        """
        Draws all active words on the screen, centered vertically.
        If the transcriber is not ready, it draws a loading message instead.
        """
        if self.is_transcriber_paused_func and self.is_transcriber_paused_func():
            paused_message = "Transcription Paused"
            paused_surface = self.font.render(paused_message, True, self.text_color)
            paused_rect = paused_surface.get_rect(center=(self.screen_width // 2, self.screen_height - self.display_text_y_offset))
            screen.blit(paused_surface, paused_rect)
            return
        
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

        # Display LLM responses (simple display for now, can be enhanced)
        if self.llm_response_display_queue and (current_time - self.last_llm_response_time) >= self.llm_response_display_interval_ms:
            llm_word = self.llm_response_display_queue.popleft()
            llm_surface = self.font.render(f"AI: {llm_word}", True, (0, 255, 0)) # Green for AI response
            llm_rect = llm_surface.get_rect(topleft=(50, 50)) # Top-left for now
            screen.blit(llm_surface, llm_rect)
            self.last_llm_response_time = current_time

    def handle_event(self, event):
        """
        Handles Pygame events for the text input box.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i: # Toggle input box visibility
                self.input_box_active = not self.input_box_active
                if not self.input_box_active:
                    self.input_text = "" # Clear text when hiding
                self.input_box_color = self.input_box_color_active if self.input_box_active else self.input_box_color_inactive
            
            if self.input_box_active:
                if event.key == pygame.K_RETURN:
                    if self.input_text and self.llm_agent_input_queue:
                        print(f"User input: {self.input_text}")
                        self.llm_agent_input_queue.put(self.input_text) # Send text to LLM agent
                        self.input_text = "" # Clear input after sending
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box_rect.collidepoint(event.pos):
                self.input_box_active = not self.input_box_active
            else:
                self.input_box_active = False
            self.input_box_color = self.input_box_color_active if self.input_box_active else self.input_box_color_inactive

    def draw_input_box(self, screen, text_color):
        """
        Draws the text input box on the screen if active.
        """
        if self.input_box_active:
            pygame.draw.rect(screen, self.input_box_color, self.input_box_rect, 2)
            text_surface = self.input_font.render(self.input_text, True, text_color)
            screen.blit(text_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 5))
            # Adjust input box width if text exceeds current width
            self.input_box_rect.w = max(200, text_surface.get_width() + 10)
