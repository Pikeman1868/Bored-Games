import pytest
from dataclasses import dataclass
from boredgames.tictactoe import TicTacToe, Presenter, Move, Cell, Board, Player

class SpyPresenter(Presenter):
    def winner(self, player: str) -> None:
        self.the_winner = player

    def move_made(self, move:Move) -> None:
        self.the_move_made = move

@dataclass
class GameTuple():
    game:TicTacToe
    presenter:SpyPresenter

@pytest.fixture
def game_tuple() -> tuple:
    presenter = SpyPresenter()
    return GameTuple(TicTacToe(presenter=presenter), presenter)


class TestAcceptance():

    def test_tictactoe_game_ends_in_win(self, game_tuple:GameTuple):
        game = game_tuple.game
        presenter = game_tuple.presenter
        winner = game.current_player
        game.move(0,0)
        game.move(2,0)
        game.move(0,1)
        game.move(2,1)
        game.move(0,2)
        assert presenter.the_winner == winner
    
class TestGame:
    
    def test_move_plays_for_current_player(self, game_tuple:GameTuple):
        game = game_tuple.game
        expected = game.current_player
        game.move(0,0)
        actual = game.current_player
        assert actual != expected

    def test_successful_move_notives_presenter_of_move(self, game_tuple:GameTuple):
        presenter = game_tuple.presenter
        game = game_tuple.game
        player = game.current_player
        game.move(0, 0)
        assert presenter.the_move_made.player == player

    def test_move_updates_board(self, game_tuple:GameTuple):
        game = game_tuple.game
        game.move(0,0)
        cell:Cell = game.board.at(0, 0)
        assert cell.is_occupied

class TestBoard:

    @pytest.fixture
    def board(self)->Board:
        return Board()

    def test_board_has_three_rows(self, board:Board):
        assert 3 == board.rows

    def test_board_has_three_cols(self, board:Board):
        assert 3 == board.cols

    def test_created_board_has_empty_cells(self, board:Board):
        for i, row in enumerate(board._cells):
            for j, cell in enumerate(row):
                assert cell.is_occupied == False

class SpyBoard:
    pass

class TestCell:
    @pytest.fixture
    def cell(self) -> Cell:
        return Cell(SpyBoard(), row=0, col=0)

    def test_cell_returns_row(self, cell:Cell):
        assert 0 == cell.row

    def test_cell_returns_col(self, cell:Cell):
        assert 0 == cell.col

    def test_cell_is_empty_at_creation(self, cell:Cell):
        assert cell.is_occupied == False

    def test_cell_is_occupied_after_move(self, cell:Cell):
        move = Move(Player("X"))
        cell.occupy(move)
        assert cell.is_occupied == True


