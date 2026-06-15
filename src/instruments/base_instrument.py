"""Base class for mock (and future real) lab instruments."""

from abc import ABC, abstractmethod


class BaseInstrument(ABC):
    def __init__(self):
        self.connection_status = "OFF"

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    def is_connected(self) -> bool:
        return self.connection_status == "ON"
