from __future__ import annotations
from dataclasses import dataclass
from itertools import cycle
from abc import ABC, abstractmethod

class GameError(Exception):
    pass

class AlreadyOccupiedError(GameError):
    pass

class GameOverError(GameError):
    pass

class Presenter(ABC):
    def winner(self, player:str) -> None:
        raise NotImplementedError()

    def move_made(self, move:Move) -> None:
        raise NotImplementedError()
    
    def error(self, error:str) -> None:
        raise NotImplementedError()

    def game_over(self) -> None:
        raise NotImplementedError()

class TicTacToe:
    class GameState(ABC):
        @abstractmethod
        def move(self, context:TicTacToe, move:Move) -> None:
            raise NotImplementedError()
        @abstractmethod
        def state(self) -> str:
            raise NotImplementedError()

    class GameOverState(GameState):
        def move(self, context: TicTacToe, move: Move) -> None:
            raise GameOverError("Game is over.")

        def state(self) -> str:
            return "Game Over!"

    class GameInProgressState(GameState):
        def move(self, context: TicTacToe, move: Move) -> None:
            context.board.make_move(move)

        def state(self) -> str:
            return "In Progress!"

    GAME_OVER = GameOverState()
    GAME_IN_PROGRESS = GameInProgressState()

    def __init__(self, presenter:Presenter):
        self._presenter:Presenter = presenter
        self._board:Board = Board()
        self._state:TicTacToe.GameState = self.GAME_IN_PROGRESS

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

    @property
    def state(self) -> str:
        return self._state.state()

    def move(self, row:int, col:int):
        move = Move(self.current_player, row, col)
        try:
            self._state.move(self, move)
            self._presenter.move_made(move)
            self._next_player()
        except GameError as e:
            self._presenter.error(e)

    def end_game(self) -> None:
        self._state = self.GAME_OVER
        self._presenter.game_over()

    def _next_player(self):
        self.current_player = next(self.players)

@dataclass
class Move:
    player:Player
    row:int
    col:int

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
            raise AlreadyOccupiedError(f"{context.__str__()} already occupied!")

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

    @property
    def marker(self) -> str:
        return 'X'

    def occupy(self, move:Move) -> None:
        self._current_state.occupy(self, move)

    def __str__(self) -> str:
        return f"Cell({self.row},{self.col})"

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

    def make_move(self, move:Move) -> None:
        self.at(move.row, move.col).occupy(move)