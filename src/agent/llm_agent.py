import threading
import queue
import time
from abc import ABC, abstractmethod

class AbstractLLMAgent(ABC, threading.Thread):
    """
    Abstract base class for LLM agent implementations.
    Defines the interface for agents that process text queries.
    """
    def __init__(self, input_queue, output_queue=None):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self._running = False

    @abstractmethod
    def process_query(self, query: str) -> str:
        """
        Processes a single text query and returns a response.
        This method should be implemented by concrete agent classes.
        """
        pass

    def run(self):
        """
        The main loop of the LLM agent thread.
        Continuously pulls queries from the input queue and processes them.
        """
        self._running = True
        print(f"{self.__class__.__name__} started, waiting for queries...")
        while self._running:
            try:
                query = self.input_queue.get(timeout=0.1) # Wait for a short period
                if query:
                    response_text = self.process_query(query)
                    if response_text and self.output_queue:
                        self.output_queue.put(response_text)
            except queue.Empty:
                pass # No query in the queue, continue loop
            except Exception as e:
                print(f"{self.__class__.__name__} error: {e}")
        print(f"{self.__class__.__name__} stopped.")

    def stop(self):
        """
        Signals the agent thread to stop.
        """
        self._running = False
        print(f"{self.__class__.__name__} stopping...")

class EchoLLMAgent(AbstractLLMAgent):
    """
    A concrete LLM agent implementation that simply echoes the received query.
    Used for testing and as a placeholder.
    """
    def __init__(self, input_queue, output_queue=None):
        super().__init__(input_queue, output_queue)
        print("EchoLLMAgent initialized.")

    def process_query(self, query: str) -> str:
        """
        Echoes the input query as the response.
        """
        print(f"EchoLLMAgent received query: '{query}'")
        return f"Echo: {query}"
