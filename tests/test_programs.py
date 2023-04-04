import argparse
import os
import shutil


def compare_expected_output_to_program_output(expected_results_dir, input_file_dir):
    results = {}
    os.mkdir("results")
    for program in os.listdir(input_file_dir):
        output_file_name = os.getcwd() + "/results/" + \
            program.split('.')[0] + "_res.txt"
        os.system(
            f'python katana/katana.py --program "{input_file_dir}/{program}" --run >> {output_file_name}')

        with open(output_file_name, "r") as program_results:
            results[program.split(".")[0]] = program_results.readlines()

    for program in os.listdir(expected_results_dir):
        output_file_name = os.getcwd() + "/expected_outputs/" + program
        with open(output_file_name, "r") as expected_results:
            key = program.split(".")[0].replace("_expected_output", "")
            assert results[key] == expected_results.readlines(
            ), f"Output not the same as expected for {key} | Results = {results[key]} | Expected = {expected_results.readlines()}"


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


def clean_up_test():
    shutil.rmtree("results")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--create-expected", action="store_true",
                            help="Switch to recreate the expected outputs.")
    args = arg_parser.parse_args()

    create_expected_outputs = args.create_expected

    try:
        if create_expected_outputs:
            clean_previous_outputs("./expected_outputs")
            build_expected_outputs("./sample_programs")
        compare_expected_output_to_program_output(
            "./expected_outputs", "./sample_programs")
        print("Passed")
    except Exception as ex:
        print(ex)
    finally:
        clean_up_test()
