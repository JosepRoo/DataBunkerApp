from dataclasses import dataclass


@dataclass
class BaseError(Exception):
    message: str
