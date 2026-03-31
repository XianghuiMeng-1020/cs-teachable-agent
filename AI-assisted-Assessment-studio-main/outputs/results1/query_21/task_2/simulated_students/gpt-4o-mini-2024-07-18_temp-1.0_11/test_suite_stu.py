from solution_program import *
import os
import pytest
from solution_program import Game, Library

@pytest.fixture(scope="module")
def setup_module():
    games_file = 'test_games.txt'
    with open(games_file, 'w') as f:
        f.write("Catan,Settlers,1995,1\n")
        f.write("Pandemic,Leacock,2008,0\n")
        f.write("Chess,Unknown,1475,1\n")
    yield games_file
    os.remove(games_file)

class TestLibrary:
    def test_add_game(self):
        library = Library()
        library.add_game("Monopoly", "Fisher", 1935)
        assert any(game.title == "Monopoly" for game in library.collection)

    def test_borrow_game_success(self):
        library = Library()
        library.add_game("Mysterium", "Oleksandr", 2015)
        result = library.borrow_game("Mysterium")
        assert result is True
        assert any(game.title == "Mysterium" and not game.availability for game in library.collection)

    def test_borrow_game_failure(self):
        library = Library()
        library.add_game("Uno", "Merle", 1971)
        library.borrow_game("Uno")
        result = library.borrow_game("Uno")
        assert result is False

    def test_return_game(self):
        library = Library()
        library.add_game("Risk", "Parker", 1957)
        library.borrow_game("Risk")
        library.return_game("Risk")
        assert any(game.title == "Risk" and game.availability for game in library.collection)

    def test_load_games(self, setup_module):
        library = Library()
        library.load_games(setup_module)
        assert any(game.title == "Catan" and game.availability for game in library.collection)
        assert any(game.title == "Pandemic" and not game.availability for game in library.collection)
        assert len(library.collection) == 3

    def test_save_games(self, tmp_path, setup_module):
        library = Library()
        library.load_games(setup_module)
        temp_file = tmp_path / "output_games.txt"
        library.save_games(str(temp_file))
        with open(temp_file, 'r') as file:
            lines = file.readlines()
        assert "Catan,Settlers,1995,1\n" in lines
        assert "Pandemic,Leacock,2008,0\n" in lines
        assert "Chess,Unknown,1475,1\n" in lines