import argparse
import os
import shutil
from itertools import zip_longest


display_compare = False


def compare_expected_output_to_program_output(expected_results_dir, input_file_dir):
    results = {}
    to_be_compare_results = set()
    compared_results = set()
    os.mkdir("results")
    for program in os.listdir(input_file_dir):
        output_file_name = os.getcwd() + "/results/" + \
            program.split('.')[0] + "_res.txt"
        if display_compare:
            print(f"Compiling {program}")
        os.system(
            f'python katana/katana.py --program "{input_file_dir}/{program}" --run >> {output_file_name}')

        with open(output_file_name, "r") as program_results:
            results[program.split(".")[0]] = program_results.readlines()
            to_be_compare_results.add(program.split(".")[0])

    for program in os.listdir(expected_results_dir):
        output_file_name = os.getcwd() + "/expected_outputs/" + program
        with open(output_file_name, "r") as expected_results:
            key = program.split(".")[0].replace("_expected_output", "")
            expected_lines = expected_results.readlines()
            compared_results.add(key)
            # Don't want to print the massive rule_110 results right now.
            if display_compare and key != "rule_110":
                build_output_table_row(
                    output_file_name.split("/")[-1], program.replace("_expected_output", "_res"), expected_lines, results[key])
            assert results[key] == expected_lines, f"Output not the same as expected for {key} | Results = {results[key]} | Expected = {expected_results.readlines()}"

    if missing_compares := to_be_compare_results - compared_results:
        raise Exception(
            f"Missing compares for {missing_compares}. Generate expected results for these tests.")


def build_output_table_row(expected_file_name, results_file_name, expected_values, results_values):
    max_length = 70
    header_row = ""

    print(142*'_')

    if len(expected_file_name) < max_length:
        header_row += f"|{expected_file_name}" + \
            ((max_length - len(expected_file_name)) * '-')
    else:
        header_row += f"|{expected_file_name[:37]}..."

    header_row += "|"

    if len(results_file_name) < max_length:
        header_row += f"{results_file_name}" + \
            ((max_length - len(results_file_name)) * '-')
    else:
        header_row += f"|{results_file_name[:37]}..."

    header_row += "|"
    print(header_row)

    print(142*'=')

    for expected_line, result_line in zip_longest(expected_values, results_values):
        line_info = ""
        expected_line = expected_line.strip()
        result_line = result_line.strip()
        if len(expected_line) < max_length:
            line_info += f"|{expected_line}" + \
                ((max_length - len(expected_line)) * '-')
        else:
            line_info += f"|{expected_line[:37]}..."
        if len(result_line) < max_length:
            line_info += f"|{result_line}" + \
                ((max_length - len(result_line)) * '-')
        else:
            line_info += f"|{result_line[:37]}..."
        line_info += "|"
        print(line_info)


def clean_previous_outputs(sample_program_dir):
    for program in os.listdir(sample_program_dir):
        output_file_name = os.getcwd() + sample_program_dir.replace(".", "") + \
            "/" + program
        os.remove(output_file_name)


def build_expected_outputs(sample_program_dir):
    for program in os.listdir(sample_program_dir):
        output_file_name = os.getcwd() + "/expected_outputs/" + \
            program.split('.')[0] + "_expected_output.txt"
        os.system(
            f'python katana/katana.py --program "{sample_program_dir}/{program}" --run >> {output_file_name}')


def build_new_only(expected_results_dir, sample_program_dir):
    # Build list of results that already exist
    # breakpoint()
    expected_results_file_list = set()
    for program in os.listdir(expected_results_dir):
        expected_results_file_list.add(program.split(
            ".")[0].replace("_expected_output", ""))

    # breakpoint()
    # Build list of all files in the sample file dir.
    sample_file_list = set()
    for program in os.listdir(sample_program_dir):
        sample_file_list.add(program.split(".")[0])

    # breakpoint()
    if results_to_make := sample_file_list - expected_results_file_list:
        for program in results_to_make:
            output_file_name = os.getcwd() + "/expected_outputs/" + \
                program + "_expected_output.txt"
            os.system(
                f'python katana/katana.py --program "{sample_program_dir}/{program}.ktna" --run >> {output_file_name}')


def clean_up_test():
    shutil.rmtree("results")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--display-compare", action="store_true",
                            help="Switch to display the results as they compared.")
    arg_parser.add_argument("--recreate-all", action="store_true",
                            help="Switch to recreate all the expected outputs.")
    arg_parser.add_argument("--create-new-only", action="store_true",
                            help="Switch to only the results for newly added or missing tests.")
    args = arg_parser.parse_args()

    new_only = args.create_new_only
    recreate_expected_outputs = args.recreate_all
    display_compare = args.display_compare

    try:
        if recreate_expected_outputs:
            clean_previous_outputs("./expected_outputs")
            build_expected_outputs("./sample_programs")
        if new_only:
            build_new_only("./expected_outputs", "./sample_programs")
        compare_expected_output_to_program_output(
            "./expected_outputs", "./sample_programs")
        print("Passed")
    except Exception as ex:
        print(ex)
    finally:
        clean_up_test()
