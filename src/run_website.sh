GIT_URL="https://github.com/hltcoe/turkle.git"
repo_dir="Turkle"

# check if the directory exists
if [ -d "$repo_dir" ]; then
    echo "Directory $repo_dir exists. Please remove it and try again."
    exit 1
fi

# clone the repo to the directory
git clone $GIT_URL $repo_dir

# choose the right pip/python
if [ -f "/usr/bin/pip3" ]; then
    pip="/usr/bin/pip3"
    python="/usr/bin/python3"
else
    pip="/usr/bin/pip"
    python="/usr/bin/python"
fi

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
