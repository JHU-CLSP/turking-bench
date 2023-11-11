import subprocess
import os

def run_web_server():
    subprocess.run('bash -c "source activate root; python -V"', shell=True)
    subprocess.Popen(["python", "Turkle/manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    assert os.path.exists("Turkle/manage.py"), f"Turkle must be installed in the Turkle directory before running this script to start the web server"
    run_web_server()