GIT_URL="https://github.com/klxu03/turkle.git"
repo_dir="Turkle"

# check if the directory exists
if [ -d "$repo_dir" ]; then
    echo "Directory $repo_dir exists, running pre-existing server"
    cd $repo_dir
    python3 manage.py runserver 0.0.0.0:8000
    exit 0
fi