GIT_URL="https://github.com/klxu03/turkle.git"
repo_dir="Turkle"

# check poetry/pip
if command -v poetry >/dev/null 2>&1; then
    installer="poetry"
else
    if [ -f "/usr/bin/pip3" ]; then
        installer="pip3"
    else
        installer="pip"
    fi
fi

# pick the right version of python
if [ -f "~/miniconda3/envs/turk/bin/python" ]; then
    # Rockfish specified conda python
    conda activate turk
    python --version
    python="/home/kxu39/miniconda3/envs/turk/bin/python"
elif [ -f "/Users/${USER}/.tea/tea.xyz/v*/bin/tea" ]; then
    python="tea python"
elif [ -f "/usr/bin/pip3" ]; then
    python="python3"
else
    python="python"
fi

echo "Using $installer and $python"

# check if the directory exists
if [ -d "$repo_dir" ]; then
    echo "Directory $repo_dir exists, running pre-existing server"
    cd $repo_dir
    $python manage.py runserver 0.0.0.0:8000
    exit 0
fi

# clone the repo to the directory
git clone $GIT_URL $repo_dir

cd $repo_dir

# Dummy username/password for the superuser
export DJANGO_SUPERUSER_EMAIL=abcd@efg.com
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=123

if [ "$installer" != "poetry" ]; then
    $installer install -r requirements.txt
fi

$python manage.py migrate
$python manage.py createsuperuser --noinput
$python manage.py runserver 0.0.0.0:8000
