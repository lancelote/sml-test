import re
import subprocess
from itertools import chain
from pathlib import Path

import click

PASS = re.compile(r"^val test.*= true : bool$")
FAIL = re.compile(r"^val test.*= false : bool$")
ERROR = re.compile(r"^.*\.sml:[.\d\-]* Error: .*$")
EXCEPTION = re.compile(r"^uncaught exception .*$")
USE_FAIL = re.compile(r"^\[use failed: '.+' does not exist or is unreadable]")


class Result:
    def __init__(self, test_file: Path, output: str) -> None:
        self.test_file = test_file
        self.passed_lines: list[str] = []
        self.failed_lines: list[str] = []
        self.error_lines: list[str] = []
        self.raw_output: str = output


def run(test_file: Path) -> Result:
    file_name = test_file.name
    cwd = test_file.parent

    process = subprocess.Popen(
        ["sml", file_name],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    out_bytes, _ = process.communicate()
    out = out_bytes.decode("utf-8")
    result = Result(test_file, out)

    for line in out.split("\n"):
        if re.match(PASS, line):
            result.passed_lines.append(line)
        elif re.match(FAIL, line):
            result.failed_lines.append(line)
        elif re.match(ERROR, line):
            result.error_lines.append(line)
        elif re.match(EXCEPTION, line):
            result.error_lines.append(line)
        elif re.match(USE_FAIL, line):
            result.error_lines.append(line)

    return result


def report(results: list[Result], verbose: bool = False) -> None:
    for result in results:
        if verbose:
            click.echo(result.raw_output)
        elif result.failed_lines or result.error_lines:
            click.echo(result.test_file)
            for line in chain(result.failed_lines, result.error_lines):
                click.echo(f"  {line}")


def main(verbose: bool) -> int:
    working_directory = Path(".")
    click.echo(f"Running in {working_directory.absolute()}")

    passed = 0
    failed = 0
    errors = 0
    results: list[Result] = []

    for test_file in working_directory.glob("**/*test.sml"):
        result = run(test_file)
        results.append(result)

        passed += len(result.passed_lines)
        failed += len(result.failed_lines)
        errors += len(result.error_lines)

    click.echo(f"OK={passed}, FAIL={failed}, ERR={errors}")
    report(results, verbose=verbose)

    return 0 if errors == 0 and failed == 0 else 1
