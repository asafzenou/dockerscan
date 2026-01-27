from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all analysis agents."""

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
