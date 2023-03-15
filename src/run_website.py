from git import Repo # import GitPython module
import os 

git_url = "https://github.com/hltcoe/turkle.git" 
repo_dir = "Turkle" 
Repo.clone_from(git_url, repo_dir) 

os.chdir(repo_dir) 
os.system("pip install -r requirements.txt")
os.system("python manage.py migrate")
os.system("python manage.py createsuperuser")
os.system("python manage.py runserver 0.0.0.0:8000")