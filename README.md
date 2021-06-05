# sml-test

Bare-bones Standard ML test runner written in Python

## Assumptions

> Test layout from "Programming Languages, Part A" Coursera course is used

- A test file has `*test.sml` name
- A test file has `use "impl.sml";` on top
  - Where `impl.sml` is implementation being tested
- A test case is a boolean variable with `test*` name in the test file

### Example Test

Example test file `hw1test.sml`

```sml
use "hw1.sml";

val test1_1 = is_older ((1,2,3),(2,3,4)) = true
```

... where `is_older` is a function from `hw1.sml`.

## Installation

`pip install -U --user sml-test`

> The package will be installed in your user home directory. See `pip`
> documentation about [user installs][1]. You need the installation directory
> to be present in `PATH` to run `clean-docker` from the terminal.

## Usage

```console
$ sml-test --help
Usage: sml-test [OPTIONS]

  Recursively execute all SML tests

Options:
  --version      Show the version and exit.
  -v, --verbose  Print raw SML output
  --help         Show this message and exit.
```

### Example Test Run

```console
$ sml-test
Running in /Users/user/git/prog_lang_a
OK=81, FAIL=1, ERR=5
week1/hw/hw1test.sml
  val test1_3 = false : bool
week0/hw/hw0test.sml
  hw0test.sml:9.14-9.20 Error: unbound variable or constructor: double
  hw0test.sml:11.14-11.20 Error: unbound variable or constructor: double
  hw0test.sml:13.14-13.20 Error: unbound variable or constructor: triple
  hw0test.sml:15.14-15.20 Error: unbound variable or constructor: triple
  hw0test.sml:17.14 Error: unbound variable or constructor: f
```

## Requirements

- Python 3.8+
- You need `sml` executable to be present in `PATH`

## Contributions & Suggestions

Please feel free to contribute a missing functionality or suggest changes,
e.g.

- Support for different tests layouts
- Support for older Python versions
- Support for different OS

[1]: https://pip.pypa.io/en/latest/user_guide/#user-installs
