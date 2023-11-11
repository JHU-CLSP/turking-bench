import subprocess
import os

def run_web_server():
    subprocess.Popen("conda run -n turk python Turkle/manage.py runserver 0.0.0.0:8000".split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    assert os.path.exists("Turkle/manage.py"), f"Turkle must be installed in the Turkle directory before running this script to start the web server"
    run_web_server()