from abc import ABC, abstractmethod
from numpy import ndarray


class Driver(ABC):
    """An abstract class used to represent the display driver interface"""

    @abstractmethod
    def start(self):
        """Connect to display device and initialize it"""
        pass

    @abstractmethod
    def stop(self):
        """Disconnect from display device and cleanup"""
        pass

    @abstractmethod
    def push_frame(self, frame):
        """
        Send frame to display device for display

        :param frame: The frame
        :type frame: ndarray
        """
        pass
