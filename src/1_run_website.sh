GIT_URL="https://github.com/klxu03/turkle.git"
repo_dir="Turkle"

# choose the right pip/python
if [ -f "/Users/${USER}/.tea/tea.xyz/v*/bin/tea" ]; then
    pip="tea pip"
    python="tea python"
elif [ -f "/usr/bin/pip3" ]; then
    pip="pip3"
    python="python3"
else
    pip="pip"
    python="python"
fi

echo "Using $pip and $python"

# check if the directory exists
if [ -d "$repo_dir" ]; then
    echo "Directory $repo_dir exists, running pre-existing server"
    cd $repo_dir
    $python manage.py runserver 0.0.0.0:8000
    exit 0
#    exit 1
fi

# clone the repo to the directory
git clone $GIT_URL $repo_dir

cd $repo_dir

# Dummy username/password for the superuser
export DJANGO_SUPERUSER_EMAIL=abcd@efg.com
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=123

$pip install -r requirements.txt
$python manage.py migrate
$python manage.py createsuperuser --noinput
$python manage.py runserver 0.0.0.0:8000
