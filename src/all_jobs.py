""" 
Script that runs all jobs at once

>> python src/all_jobs.py

"""

from job import run


if __name__ == "__main__":

    for num in range(11):
        run(num)
