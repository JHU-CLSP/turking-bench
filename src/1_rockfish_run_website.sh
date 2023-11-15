GIT_URL="https://github.com/klxu03/turkle.git"
repo_dir="Turkle"

# Rockfish specified conda python
python=~/miniconda3/envs/turk/bin/python

echo "Using Rockfish python $python"

# check if the directory exists
if [ -d "$repo_dir" ]; then
    echo "Directory $repo_dir exists, running pre-existing server"
    cd $repo_dir
    $python manage.py runserver 0.0.0.0:8000
    exit 0
fi