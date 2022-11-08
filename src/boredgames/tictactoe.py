from __future__ import annotations
from typing import Protocol

class Presenter(Protocol):
    def winner(self, player:str) -> None:
        ...

class TicTacToe:
    def __init__(self, presenter):
        self._presenter = presenter

    def move(self, row:int, col:int):
        ...