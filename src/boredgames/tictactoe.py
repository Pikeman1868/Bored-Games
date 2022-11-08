from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass
from itertools import cycle
from abc import ABC, abstractmethod

class Presenter(Protocol):
    def winner(self, player:str) -> None:
        ...

    def move_made(self, move:Move) -> None:
        ...

class TicTacToe:
    def __init__(self, presenter:Presenter):
        self._presenter = presenter
        self._board = Board()

        players = (Player('X'), Player('O'))
        self.players = cycle(players)
        self._next_player()

    @property
    def current_player(self) -> Player:
        return self._current_player

    @current_player.setter
    def current_player(self, player:Player) -> None:
        self._current_player = player

    @property
    def board(self) -> Board:
        return self._board

    def move(self, row:int, col:int):
        move = Move(self.current_player)
        self.board.at(row, col).occupy(move)
        self._presenter.move_made(move)
        self._next_player()

    def _next_player(self):
        self.current_player = next(self.players)
        

@dataclass
class Move:
    player:Player

@dataclass
class Player:
    marker:str

class Cell:
    class CellState(ABC):
        @abstractmethod
        def is_occupied(self) -> bool:
            pass
        @abstractmethod
        def occupy(self, context:Cell, move:Move)->None:
            pass
    
    class EmptyState(CellState):
        def is_occupied(self) -> bool:
            return False
        def occupy(self, context: Cell, move: Move) -> None:
            context._player = move.player
            context._current_state = Cell.OCCUPIED
        
    class OccupiedState(CellState):
        def is_occupied(self) -> bool:
            return True
        def occupy(self, context: Cell, move: Move) -> None:
            pass

    EMPTY = EmptyState()
    OCCUPIED = OccupiedState()

    def __init__(self, board:Board, row:int, col:int):
        self.board:Board = board
        self._row:int = row
        self._col:int = col
        self._current_state:Cell.CellState = self.EMPTY
        self._player = None

    @property
    def is_occupied(self) -> bool:
        return self._current_state.is_occupied()

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    def occupy(self, move:Move) -> None:
        self._current_state.occupy(self, move)

class Board:
    def __init__(self) -> None:
        self._cells = list()
        for i in range(self.rows):
            row = list()
            for j in range(self.cols):
                row.append(Cell(self, i, j))
            self._cells.append(row)

    @property
    def rows(self) -> int:
        return 3

    @property
    def cols(self) -> int:
        return 3

    def at(self, row:int, col:int) -> Cell:
        return self._cells[row][col]