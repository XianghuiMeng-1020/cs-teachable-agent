import pytest
import os
from solution import lottery_game

@dataclass
class CapturedOutput:
    out: str

@pytest.fixture
def capsys(monkeypatch):
    _input = []
    _output = ''

    def mock_input(s=''):
        nonlocal _output
        _output += s
        if _input:
            return _input.pop(0)
        return ''

    def set_input(*inputs):
        nonlocal _input
        _input.extend(inputs)

    monkeypatch.setattr('builtins.input', mock_input)

    def set_output(outputs):
        nonlocal _output
        _output = outputs

    monkeypatch.setattr('builtins.print', lambda s: _output.__add__(s + '\n'))

    def get_output():
        return CapturedOutput(_output.strip())

    yield set_input, get_output

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    with open("lottery_numbers.txt", "w") as f:
        f.write("3,15,27,33,41,57\n")

@pytest.fixture(scope='module', autouse=True)
def teardown_module():
    yield
    os.remove('lottery_numbers.txt')


def test_win(capsys):
    set_input, get_output = capsys
    set_input('3')
    lottery_game()
    assert 'You Win!' == get_output().out


def test_lose(capsys):
    set_input, get_output = capsys
    set_input('1')
    lottery_game()
    assert 'Try Again next time!' == get_output().out


def test_invalid_file_content(monkeypatch):
    os.rename("lottery_numbers.txt", "lottery_numbers_bak.txt")
    with open("lottery_numbers.txt", "w") as f:
        f.write("Invalid content")
    monkeypatch.setattr('builtins.input', lambda _: '33')
    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)
    lottery_game()
    assert captured_output.getvalue().strip() == 'Invalid input or file content'
    os.rename("lottery_numbers_bak.txt", "lottery_numbers.txt")


def test_invalid_input(capsys):
    set_input, get_output = capsys
    set_input('abc')
    lottery_game()
    assert 'Invalid input or file content' == get_output().out


def test_file_not_exists(monkeypatch):
    os.rename("lottery_numbers.txt", "lottery_numbers_bak.txt")
    monkeypatch.setattr('builtins.input', lambda _: '27')
    captured_output = StringIO()
    monkeypatch.setattr('sys.stdout', captured_output)
    lottery_game()
    os.rename("lottery_numbers_bak.txt", "lottery_numbers.txt")
    assert captured_output.getvalue().strip() == 'Invalid input or file content'
