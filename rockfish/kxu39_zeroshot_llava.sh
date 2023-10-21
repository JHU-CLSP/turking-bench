#!/bin/bash
#
#SBATCH --job-name=llava_serve
#SBATCH --output=llava_serve.out.log
#SBATCH --error=llava_serve.err.log
#
# Number of tasks needed for this job. Generally, used with MPI jobs
#SBATCH --ntasks=1
#SBATCH --partition=ica100
#
# Time format = HH:MM:SS, DD-HH:MM:SS
#SBATCH --time=72:00:00
#
# Minimum memory required per allocated  CPU  in  MegaBytes.
#SBATCH --mem-per-cpu=48000
#SBATCH --gres=gpu:1
#SBATCH -A danielk80_gpu
#
# Send mail to the email address when the job fails
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=kxu39@jhu.edu

# Load necessary modules
module load anaconda
module load cuda/11.8

source ~/.bashrc

conda activate llava-1.5

module list

python --version
which python

source .env

export TRANSFORMERS_CACHE="/scratch4/danielk/kxu39/huggingface_cache/transformers"
export BNB_CUDA_VERSION=118

# Run the Python script
echo "Can you please describe what this place looks like and if you would recommend me going to vacation here?\nWhat are things I should be cautious about visiting this place?" | ~/miniconda3/envs/llava-1.5/bin/python -m llava.serve.cli \
    --model-path liuhaotian/llava-v1.5-7b \
    --image-file "https://llava-vl.github.io/static/images/view.jpg" \
    --load-4bit