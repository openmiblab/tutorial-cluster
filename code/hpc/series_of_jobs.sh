#!/bin/bash
# Use the Bash shell to interpret the script

# Requests 16 gigabytes of RAM for this job (total, not per core).
#SBATCH --mem=2G

# Requests 16 CPU cores for this job.
#SBATCH --cpus-per-task=1

# Sets the maximum wall-clock time for this job: 95 hours, 0 minutes, 0 seconds
#SBATCH --time=00:10:00

# The cluster will send an email to this address only if the job fails
#SBATCH --mail-user=s.sourbron@sheffield.ac.uk
#SBATCH --mail-type=FAIL

# Assigns an internal “comment” (or name) to the job in the scheduler
#SBATCH --comment=cluster-template

# Assign a name to the job
#SBATCH --job-name=test

# This is a job array, which means 11 separate jobs will be submitted 
# — one for each value of $SLURM_ARRAY_TASK_ID from 0 to 10.
# This is often used for batch processing, e.g. processing 11 datasets or parameter sets
#SBATCH --array=0-10

# Write logs to the logs folder
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# Unsets the CPU binding policy.
# Some clusters automatically bind threads to cores; unsetting it can 
# prevent performance issues if your code manages threading itself 
# (e.g. OpenMP, NumPy, or PyTorch).
unset SLURM_CPU_BIND

# Ensures that all your environment variables from the submission 
# environment are passed into the job’s environment
export SLURM_EXPORT_ENV=ALL

# Loads the Anaconda module provided by the cluster.
# (On HPC systems, software is usually installed as “modules” to avoid version conflicts.)
module load Anaconda3/2024.02-1

# Initialize Conda for this non-interactive shell
eval "$(conda shell.bash hook)"

# Activates your Conda environment named venv.
# (Older clusters use source activate; newer Conda versions use conda activate venv.)
# We assume that the conda environment 'venv' has already been created
conda activate tutorial-cluster

# Get the current username
USERNAME=$(whoami)

# Define path variables here
BASE_DIR="/mnt/parscratch/users/$USERNAME/tutorial-cluster"
DATA_DIR="$BASE_DIR/data"
BUILD_DIR="$BASE_DIR/build"

# srun runs your program on the allocated compute resources managed by Slurm
# where $SLURM_ARRAY_TASK_ID = the current job’s array index (from 0 to 10).
srun python "$BASE_DIR/code/src/one_job.py" --num $SLURM_ARRAY_TASK_ID --data="$DATA_DIR" --build="$BUILD_DIR"

