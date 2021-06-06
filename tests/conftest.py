import os
import shutil

import pytest
from click.testing import CliRunner


@pytest.fixture(autouse=True, scope="session")
def sml_available():
    assert shutil.which("sml"), "sml executable wasn't found in PATH"


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def sml_test_file(request, tmp_path):
    sml_file = tmp_path / "sample_test.sml"
    os.chdir(tmp_path)
    yield sml_file
    os.chdir(request.config.invocation_dir)
