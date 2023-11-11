import subprocess
import sys
import os

# what conda env am I in (e.g., where is my Python process from)?
ENVBIN = sys.exec_prefix

# what binaries am I looking for that are installed in this env?
PYTHON = os.path.join(ENVBIN, "bin", "python")

# let's make sure they exist, no typos.
for bin in (PYTHON):
    assert os.path.exists(bin), "missing binary {} in env {}".format(bin, ENVBIN)

def run_web_server():
    subprocess.Popen([PYTHON, "Turkle/manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    assert os.path.exists("Turkle/manage.py"), f"Turkle must be installed in the Turkle directory before running this script to start the web server"
    run_web_server()