import os

import pytest
from click.testing import CliRunner

from confil.confil import confil

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURR_DIR, "test_data/")

FILE_1 = os.path.join(TEST_DATA_DIR, "test_file_1.fastq")
FILE_2 = os.path.join(TEST_DATA_DIR, "test_file_2.fastq")


@pytest.fixture(scope="module")
def cli_runner():
    runner = CliRunner()
    return runner


def test_runner(cli_runner):
    result = cli_runner.invoke(confil, ["--paired", FILE_1, FILE_2])
    # We have a contaminated test file!
    assert result.exit_code == 1
