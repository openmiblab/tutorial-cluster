""" 
Script that runs one job, with a num argument to select which one.

This allows for a batch processing script on the cluster to 
submit multiple jobs in succession.

>> python src/one_job.py --num=1

"""

import argparse

from utils.job import run


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, default=0, help="Job array index")
    args = parser.parse_args()
    run(args.num)
