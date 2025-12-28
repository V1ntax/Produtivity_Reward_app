import os
import subprocess
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Run the main program
subprocess.run([sys.executable, os.path.join(script_dir, "interface.py")])