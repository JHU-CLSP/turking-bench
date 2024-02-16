#!/bin/bash
#
#SBATCH --job-name=llama2_runs
#SBATCH --output=out.llama2_runs.log
#SBATCH --error=err.llama2_runs.log
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

run_command_group() {
    ollama_model=$1

    # Start ollama run in the background and get its PID
    ollama run "$ollama_model" &
    ollama_pid=$!

    # Start the website script in the background and get its PID
    ./1_ia1_run_website.sh &
    website_pid=$!

    # Sleep for some time
    sleep 10

    # Run the evaluation script
    if python3 4_run_evaluation.py --solver_type text --ollama_model "$ollama_model" --tasks test_easy --max_instance_count 1 --num_demonstrations 3 --use_relevant_html --headless --do_eval --server; then
        echo "Evaluation for $ollama_model completed successfully 3 relevant_html demos."
    else
        echo "Evaluation for $ollama_model failed 3 relevant_html demos."
    fi

    if python3 4_run_evaluation.py --solver_type text --ollama_model "$ollama_model" --tasks test_easy --max_instance_count 1 --num_demonstrations 0 --no-use_relevant_html --headless --do_eval --server; then
        echo "Evaluation for $ollama_model completed successfully 0 full_html demos."
    else
        echo "Evaluation for $ollama_model failed 0 full_html demos."
    fi

    # Kill the ollama run and website processes
    kill $ollama_pid
    kill $website_pid
}

# Run command groups sequentially, continuing even if one fails
run_command_group "llama2:7b"
run_command_group "llama2:7b-chat"
run_command_group "llama2:13b-chat"