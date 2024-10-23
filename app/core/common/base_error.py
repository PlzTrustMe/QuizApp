from dataclasses import dataclass


@dataclass(eq=False)
class BaseError(Exception):
    @property
    def message(self):
        return "Application error"
