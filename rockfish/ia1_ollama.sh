#!/bin/bash
#
#SBATCH --job-name=llama2_70b
#SBATCH --output=out.llama2_70b.log
#SBATCH --error=err.llama_70b.log
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

# Run the Python script
bash="/bin/bash"

python --version
which python

cd turk-instructions/src

ollama run llama2:70b & sleep 10 && python3 4_run_evaluation.py --solver_type text --ollama_model llama2:70b --tasks test_easy --max_instance_count 20 --num_demonstrations 3 --use_relevant_html --headless --do_eval --server > relevant_ollama_llama270b_3.txt