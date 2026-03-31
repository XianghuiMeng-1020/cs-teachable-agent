import pytest
import os
from solution import lottery_stub_generator

input_file_content = """Alice,23,20\nBob,11,10\nEve,7,18\n"""
expected_output_content = """Alice,23,20,LOSE\nBob,11,10,WIN\nEve,7,18,WIN\n"""

new_input_file_content = """John,25,5\nMarry,8,24\nPaul,50,50\n"""
new_expected_output_content = """John,25,5,WIN\nMarry,8,24,LOSE\nPaul,50,50,WIN\n"""

input_filepath = "test_input.txt"
output_filepath = "test_output.txt"

new_input_filepath = "new_test_input.txt"
new_output_filepath = "new_test_output.txt"


def setup_module(module):
    with open(input_filepath, 'w') as file:
        file.write(input_file_content)

    with open(new_input_filepath, 'w') as file:
        file.write(new_input_file_content)


def teardown_module(module):
    if os.path.exists(input_filepath):
        os.remove(input_filepath)
    if os.path.exists(output_filepath):
        os.remove(output_filepath)
    if os.path.exists(new_input_filepath):
        os.remove(new_input_filepath)
    if os.path.exists(new_output_filepath):
        os.remove(new_output_filepath)


def test_lottery_stub_generator_output():
    lottery_stub_generator(input_filepath, output_filepath)
    with open(output_filepath, 'r') as result_file:
        content = result_file.read()
    assert content == expected_output_content


def test_new_input_conditions():
    lottery_stub_generator(new_input_filepath, new_output_filepath)
    with open(new_output_filepath, 'r') as result_file:
        content = result_file.read()
    assert content == new_expected_output_content


def test_empty_file_output():
    empty_input_path = 'empty_test_input.txt'
    empty_output_path = 'empty_test_output.txt'
    with open(empty_input_path, 'w') as file:
        file.write("")
    try:
        lottery_stub_generator(empty_input_path, empty_output_path)
        with open(empty_output_path, 'r') as result_file:
            content = result_file.read()
            assert content == ""
    finally:
        if os.path.exists(empty_input_path):
            os.remove(empty_input_path)
        if os.path.exists(empty_output_path):
            os.remove(empty_output_path)


def test_single_entry():
    single_input_path = 'single_test_input.txt'
    single_output_path = 'single_test_output.txt'
    with open(single_input_path, 'w') as file:
        file.write("Dave,20,5\n")
    try:
        lottery_stub_generator(single_input_path, single_output_path)
        with open(single_output_path, 'r') as result_file:
            content = result_file.read()
            assert content == "Dave,20,5,WIN\n"
    finally:
        if os.path.exists(single_input_path):
            os.remove(single_input_path)
        if os.path.exists(single_output_path):
            os.remove(single_output_path)


def test_invalid_format():
    invalid_input_path = 'invalid_test_input.txt'
    invalid_output_path = 'invalid_test_output.txt'
    with open(invalid_input_path, 'w') as file:
        file.write("Dan,30\n")  # Invalid line, missing age
    try:
        lottery_stub_generator(invalid_input_path, invalid_output_path)
        with open(invalid_output_path, 'r') as result_file:
            content = result_file.read()
            assert content == ""
    finally:
        if os.path.exists(invalid_input_path):
            os.remove(invalid_input_path)
        if os.path.exists(invalid_output_path):
            os.remove(invalid_output_path)
