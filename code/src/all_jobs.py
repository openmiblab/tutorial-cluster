""" 
Script that runs all jobs at once

>> python src/all_jobs.py

"""

import os
import argparse

from utils.job import run


INPUT_PATH = os.path.join(os.getcwd(), 'data')
OUTPUT_PATH = os.path.join(os.getcwd(), 'build')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=INPUT_PATH, help="Data folder")
    parser.add_argument("--build", type=str, default=OUTPUT_PATH, help="Build folder")
    args = parser.parse_args()

    for num in range(11):
        run(args.data, args.build, num)
