from textwrap import dedent

from sml_test.cli import cli


def assert_result(result, ok=0, fail=0, err=0, exit_code=0):
    assert f"OK={ok}, FAIL={fail}, ERR={err}" in result.output
    assert result.exit_code == exit_code


def test_ok_and_err(sml_test_file, cli_runner):
    sml_test_file.write_text(
        dedent(
            """
                val test_1 = 1 = 1
                val test_2 = 1 = 2
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result, ok=1, fail=1, exit_code=1)


def test_err(sml_test_file, cli_runner):
    sml_test_file.write_text(
        dedent(
            """
                test_1 = 2 = 2
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result, err=1, exit_code=1)


def test_ok(sml_test_file, cli_runner):
    sml_test_file.write_text(
        dedent(
            """
                val test_1 = 1 = 1
                val test_2 = 2 = 2
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result, ok=2)


def test_no_tests(sml_test_file, cli_runner):
    sml_test_file.write_text(
        dedent(
            """
                val foo = 2 = 2
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result)


def test_verbose(sml_test_file, cli_runner):
    sml_test_file.write_text(
        dedent(
            """
                val test_1 = 1 = 1
            """
        )
    )
    result = cli_runner.invoke(cli, ["-v"])
    assert "val test_1 = true : bool" in result.output
    assert result.exit_code == 0
