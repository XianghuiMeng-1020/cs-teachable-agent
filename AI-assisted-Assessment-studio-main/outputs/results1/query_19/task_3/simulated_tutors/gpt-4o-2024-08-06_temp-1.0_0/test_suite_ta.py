from program import *
import pytest
import os
from your_solution_module import generate_expedition_summary

def setup_module(module):
    with open('expedition_records.txt', 'w') as f:
        f.write("101,John Doe,2120,25\n")
        f.write("102,Mary Jane,2120,15\n")
        f.write("103,Bob Smith,2121,10\n")
    with open('corrupted_records.txt', 'w') as f:
        f.write("101,John Doe,2120,25\n")
        f.write("invalid_data_here\n")

def teardown_module(module):
    os.remove('expedition_records.txt')
    os.remove('corrupted_records.txt')
    if os.path.exists('summary_report.txt'):
        os.remove('summary_report.txt')


def test_correct_summary_generation():
    generate_expedition_summary('expedition_records.txt', 'summary_report.txt')
    with open('summary_report.txt', 'r') as f:
        data = f.read().strip()
    assert data == "Total Expeditions: 3\nTotal Crew Members: 50\nAverage Crew per Expedition: 16.67\nUnique Years: 2"


def test_file_not_found():
    generate_expedition_summary('non_existing_file.txt', 'summary_report.txt')
    with open('summary_report.txt', 'r') as f:
        data = f.read().strip()
    assert data.startswith("Error:")


def test_corrupted_data():
    generate_expedition_summary('corrupted_records.txt', 'summary_report.txt')
    with open('summary_report.txt', 'r') as f:
        data = f.read().strip()
    assert data.startswith("Error:")


def test_empty_file():
    open('empty_file.txt', 'w').close()
    generate_expedition_summary('empty_file.txt', 'summary_report.txt')
    with open('summary_report.txt', 'r') as f:
        data = f.read().strip()
    assert data == "Total Expeditions: 0\nTotal Crew Members: 0\nAverage Crew per Expedition: 0.00\nUnique Years: 0"
    os.remove('empty_file.txt')


def test_partial_data():
    with open('partial_data.txt', 'w') as f:
        f.write("101,John Doe,2120,25\n")
        f.write("102\n")
        f.write("103,Bob Smith,2121,10\n")
    generate_expedition_summary('partial_data.txt', 'summary_report.txt')
    with open('summary_report.txt', 'r') as f:
        data = f.read().strip()
    assert data.startswith("Error:")
    os.remove('partial_data.txt')
