# sml-test

Most basic Standard ML test runner

## Assumptions

> Test layout from "Programming Languages, Part A" Coursera course is used

- A test file has `*test.sml` name
- A test file has `use "impl.sml";` on top
  - Where `impl.sml` is implementation being tested
- A test case is a boolean variable `test*` in test file

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
...
```

### Example Test Run

```console
$ sml-test
...
```

## Requirements

- Python 3.8+
- You need `sml` executable to be present in `PATH`

## Contributions & Suggestions

Please feel free to contribute a missing functionality or suggest features,
e.g.

- Different tests layout
- Support for older Python versions
- Support for different OS

[1]: https://pip.pypa.io/en/latest/user_guide/#user-installs
