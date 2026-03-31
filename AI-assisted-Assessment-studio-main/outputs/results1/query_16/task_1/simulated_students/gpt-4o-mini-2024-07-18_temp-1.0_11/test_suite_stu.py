from solution_program import *
import pytest
from solution_program import CommsHandler

@pytest.fixture(scope="module")
def setup_module():
    comm = CommsHandler(2)
    return comm

@pytest.fixture(scope="module")
def teardown_module(request):
    request.addfinalizer(cleanup)

def cleanup():
    pass

# Test the sending of a valid message
@pytest.mark.parametrize("message, result", [
    ("Hello", "Hello#1048"),
    ("SF", "SF#410"),
    ("Mars", "Mars#920"),
    ("Galaxy", "Galaxy#1450")
])
def test_send_message(setup_module, message, result):
    assert setup_module.send_message(message) == result

# Test successful receiving of a message
@pytest.mark.parametrize("message_with_code, expected_message", [
    ("Hello#1048", "Hello"),
    ("SF#410", "SF"),
    ("Mars#920", "Mars"),
    ("Galaxy#1450", "Galaxy")
])
def test_receive_message_success(setup_module, message_with_code, expected_message):
    assert setup_module.receive_message(message_with_code) == expected_message

# Test receiving of a message with mismatched code
@pytest.mark.parametrize("message_with_code", [
    "Hello#999",
    "SF#123",
    "Mars#456",
    "Galaxy#321"
])
def test_receive_message_failure(setup_module, message_with_code):
    with pytest.raises(ValueError) as excinfo:
        setup_module.receive_message(message_with_code)
    assert str(excinfo.value) == "Transmit code mismatch"