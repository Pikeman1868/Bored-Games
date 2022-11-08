import pytest
from boredgames import tictactoe

class SpyPresenter(tictactoe.Presenter):

    def __init__(self, winner:str) -> None:
        self.winner = winner

    def winner(self, player:str):
        assert self.winner == player

@pytest.fixture
def game() -> tictactoe:
    return tictactoe(presenter=SpyPresenter(winner="X"))


class TestAcceptance():

    def test_tictactoe_game_ends_in_win(self, game:tictactoe.TicTacToe):
        game.move(0,0)
        game.move(2,0)
        game.move(0,1)
        game.move(2,1)
        game.move(0,2)
    

class TestGame:
    def test_move_plays_for_current_player(self):
        ...