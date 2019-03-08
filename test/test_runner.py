import os

import pytest
from click.testing import CliRunner

from confil.confil import confil

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(CURR_DIR, "test_data/")
TEST_REPORT = os.path.join(TEST_DATA_DIR, "test_file.tab")
FILE_1 = os.path.join(TEST_DATA_DIR, "test_file_1.fastq")
FILE_2 = os.path.join(TEST_DATA_DIR, "test_file_2.fastq")


@pytest.fixture(scope="module")
def cli_runner():
    runner = CliRunner()
    return runner


@pytest.mark.skip(reason="No way of currently testing this. It's KRAKEN!")
def test_runner(cli_runner):
    result = cli_runner.invoke(confil, ["--paired", FILE_1, FILE_2])
    assert result.exit_code == 0
