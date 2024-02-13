#!/bin/bash
#
#SBATCH --job-name=collect_field_stats
#SBATCH --output=field_stats.out.log
#SBATCH --error=field_stats.err.log
#
# Number of tasks needed for this job. Generally, used with MPI jobs
#SBATCH --ntasks=1
#SBATCH --partition=parallel
#
# Time format = HH:MM:SS, DD-HH:MM:SS
#SBATCH --time=72:00:00
#
# Minimum memory required per allocated  CPU  in  MegaBytes.
#SBATCH --mem-per-cpu=48000
#SBATCH --cpus-per-task=1
#SBATCH -A ia1
#SBATCH --partition debug
#SBATCH --qos=normal
#
# Send mail to the email address when the job fails
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=kxu39@jhu.edu

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
Xvfb :99 & ./1_rockfish_run_website.sh & sleep 10 && $python 4_run_evaluation.py --solver_type donothing --tasks all --max_instance_count 40 --headless --no-do_eval
