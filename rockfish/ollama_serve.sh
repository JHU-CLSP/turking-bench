#!/bin/bash
#
#SBATCH --job-name=llava
#SBATCH --output=llava.out.log
#SBATCH --error=llava.err.log
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
#SBATCH --gres=gpu:1
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

conda init
conda activate turk

module list

source .env

# Run the Python script
bash="/bin/bash"

python --version
which python

cd turk-instructions/src
ollama run llava & ./1_ia1_run_website.sh & sleep 10 && python3 4_run_evaluation.py --solver_type text-vision --ollama_model llava --tasks test_easy --max_instance_count 1 --no-headless --no-do_eval --server > text_gpt.txt