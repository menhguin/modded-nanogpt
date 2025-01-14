import subprocess
import sys
import os
import venv
from pathlib import Path

def run_command(command, description):
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.output}")
        return False

def main():
    # Create project directory
    project_name = "modal_project"
    project_dir = Path(project_name)
    venv_dir = project_dir / "venv"
    
    print(f"\n=== Creating project directory: {project_dir} ===")
    project_dir.mkdir(exist_ok=True)
    
    # Create virtual environment
    print(f"\n=== Creating virtual environment in: {venv_dir} ===")
    venv.create(venv_dir, with_pip=True)
    
    # Determine the activate script path based on OS
    if sys.platform == "win32":
        activate_script = venv_dir / "Scripts" / "activate.bat"
        activate_cmd = str(activate_script)
    else:
        activate_script = venv_dir / "bin" / "activate"
        activate_cmd = f"source {activate_script}"
    
    # Create requirements.txt
    requirements = '''modal
torch
'''
    with open(project_dir / "requirements.txt", "w") as f:
        f.write(requirements)
    
    # Create a setup script
    setup_script = f'''#!/bin/bash
{activate_cmd}
pip install -r requirements.txt
python -m modal setup
'''
    
    setup_script_path = project_dir / ("setup.bat" if sys.platform == "win32" else "setup.sh")
    with open(setup_script_path, "w") as f:
        f.write(setup_script)
    
    # Make setup script executable on Unix-like systems
    if sys.platform != "win32":
        setup_script_path.chmod(0o755)
    
    print("\n=== Setup Complete ===")
    print("\nTo activate the virtual environment and install dependencies:")
    
    if sys.platform == "win32":
        print(f"1. cd {project_name}")
        print(f"2. .\\venv\\Scripts\\activate")
        print("3. pip install -r requirements.txt")
        print("4. python -m modal setup")
    else:
        print(f"1. cd {project_name}")
        print("2. source venv/bin/activate")
        print("3. pip install -r requirements.txt")
        print("4. python -m modal setup")
    
    print("\nOr simply run the setup script:")
    if sys.platform == "win32":
        print(f"cd {project_name} && setup.bat")
    else:
        print(f"cd {project_name} && ./setup.sh")

if __name__ == "__main__":
    main()