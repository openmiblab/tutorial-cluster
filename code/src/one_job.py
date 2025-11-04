""" 
Script that runs one job, with a num argument to select which one.

This allows for a batch processing script on the cluster to 
submit multiple jobs in succession.

>> python src/one_job.py --num=1

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
    parser.add_argument("--num", type=int, default=0, help="Job array index")
    args = parser.parse_args()
    run(args.data, args.build, args.num)
