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
def tmp_work_dir(request, tmp_path):
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(request.config.invocation_dir)


@pytest.fixture
def sml_test_file(tmp_work_dir):
    sml_file = tmp_work_dir / "sample_test.sml"
    yield sml_file


@pytest.fixture
def sml_impl_file(tmp_work_dir):
    sml_file = tmp_work_dir / "sample.sml"
    yield sml_file
