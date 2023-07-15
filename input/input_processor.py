from abc import ABC, abstractmethod


class InputProcessor(ABC):
    @classmethod
    def process_line(cls, tokens):
        pass
