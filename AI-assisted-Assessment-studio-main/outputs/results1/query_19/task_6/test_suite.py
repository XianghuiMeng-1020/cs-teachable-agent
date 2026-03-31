import pytest
import os
from solution_program import analyze_asteroid_reports

def setup_module(module):
    reports = {
        "report1.txt": "1234,5000\n5678,3000\n9101,2000\n",
        "report2.txt": "\n",
        "report3.txt": "1100,1000\n2100,3000\n3100,2000\n4100,4000\n",
        "report4.txt": "2020,5000\n",
        "report_invalid.txt": ""
    }
    for filename, content in reports.items():
        with open(filename, 'w') as f:
            f.write(content)


def teardown_module(module):
    files = ["report1.txt", "report2.txt", "report3.txt", "report4.txt", "report_invalid.txt", "output1.txt", "output2.txt", "output3.txt", "output4.txt", "output_invalid.txt", "nonexistent_output.txt"]
    for filename in files:
        if os.path.exists(filename):
            os.remove(filename)


def test_normal_case():
    analyze_asteroid_reports("report1.txt", "output1.txt")
    with open("output1.txt", 'r') as file:
        assert file.read().strip() == "average impact force: 3333.33"


def test_no_asteroids():
    analyze_asteroid_reports("report2.txt", "output2.txt")
    with open("output2.txt", 'r') as file:
        assert file.read().strip() == "No data available"


def test_multiple_asteroids():
    analyze_asteroid_reports("report3.txt", "output3.txt")
    with open("output3.txt", 'r') as file:
        assert file.read().strip() == "average impact force: 2500.00"


def test_single_asteroid():
    analyze_asteroid_reports("report4.txt", "output4.txt")
    with open("output4.txt", 'r') as file:
        assert file.read().strip() == "average impact force: 5000.00"


def test_nonexistent_file():
    analyze_asteroid_reports("report_nonexistent.txt", "nonexistent_output.txt")
    with open("nonexistent_output.txt", 'r') as file:
        assert file.read().strip() == "No data available"
