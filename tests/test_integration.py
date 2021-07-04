from textwrap import dedent

from sml_test.cli import cli


def assert_result(result, ok=0, fail=0, err=0, exit_code=0, contains=""):
    assert f"OK={ok}, FAIL={fail}, ERR={err}" in result.output
    assert result.exit_code == exit_code
    assert contains in result.output


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
    # Two errors: mismatch type and unbound variable
    assert_result(result, err=2, exit_code=1)


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
    error_message = "val test_1 = true : bool"
    result = cli_runner.invoke(cli, ["-v"])
    assert_result(result, ok=1, exit_code=0, contains=error_message)


def test_unknown_symbol_in_impl(sml_test_file, sml_impl_file, cli_runner):
    sml_impl_file.write_text(
        dedent(
            """
                fun sum_pair_list(xs : (int * int) list) =
                    sum_list(firsts xs) + sum_list(seconds xs)
            """
        )
    )
    sml_test_file.write_text(
        dedent(
            """
                use "sample.sml";
                val test_1 = sum_pair_list([(1, 2), (3, 4)]) = 10
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result, err=4, exit_code=1)


def test_type_mismatch_in_impl(sml_test_file, sml_impl_file, cli_runner):
    sml_impl_file.write_text(
        dedent(
            """
                fun list_product(xs : int list) =
                  if null xs
                  then 1
                  else hd xs * list_product(tl xs)

                fun countdown(x : int) =
                  if x = 0
                  then []
                  else x :: countdown(x - 1)

                fun factorial(x : int) =
                    list_product countdown x
            """
        )
    )
    sml_test_file.write_text(
        dedent(
            """
                use "sample.sml";
                val test9_2 = factorial 4 = 24
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result, err=1, exit_code=1)


def test_runtime_exception(sml_test_file, sml_impl_file, cli_runner):
    sml_impl_file.write_text(
        dedent(
            """
                fun max1(xs : int list) =
                  if null xs
                  then NONE
                  else
                    let val tl_ans = max1(tl xs)
                    in if isSome tl_ans andalso valOf tl_ans > hd xs
                       then tl_ans
                       else SOME (hd xs)
                    end
            """
        )
    )
    sml_test_file.write_text(
        dedent(
            """
                use "sample.sml";
                val test3 = valOf(max1 []);
            """
        )
    )
    result = cli_runner.invoke(cli)
    assert_result(result, err=1, exit_code=1)


def test_usage_fail(sml_test_file, cli_runner):
    sml_test_file.write_text('use "foo_bar.sml";')
    error_message = "use failed: 'foo_bar.sml'"
    result = cli_runner.invoke(cli)
    assert_result(result, err=1, exit_code=1, contains=error_message)
