#!/bin/bash
#
#SBATCH --job-name=dump
#SBATCH --output=dump.out.log
#SBATCH --error=dump.err.log
#
# Number of tasks needed for this job. Generally, used with MPI jobs
#SBATCH --ntasks=1
#SBATCH --partition=defq
#
# Time format = HH:MM:SS, DD-HH:MM:SS
#SBATCH --time=72:00:00
#
# Minimum memory required per allocated  CPU  in  MegaBytes.
#SBATCH --mem-per-cpu=48000
#SBATCH --cpus-per-task=1
#SBATCH -A danielk
#
# Send mail to the email address when the job fails
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=kxu39@jhu.edu
#
# Create a job array of all the parttions
#SBATCH --array=1-1

# Load necessary modules
module load anaconda

source ~/.bashrc

conda activate turk

module list

source .env

# Run the Python script
python=~/miniconda3/envs/turk/bin/python
bash="/bin/bash"

$python --version
which $python


cd turk-instructions/src
./1_run_website.sh & sleep 10 && $python dump_partition.py dmp$SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_MAX
