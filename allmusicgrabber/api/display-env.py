import os
import sys
import subprocess

def get_venv_info():
    # Check if a virtual environment is active
    venv_path = os.getenv('VIRTUAL_ENV')
    
    if venv_path:
        print(f"Virtual Environment: {venv_path}")
    else:
        print("No virtual environment active.")
        return
    
    # Display Python version information
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}\n")
    
    # List installed packages
    print("Installed packages:")
    
    # Using pip list to get the list of installed packages
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"An error occurred while listing packages: {e}")

if __name__ == "__main__":
    get_venv_info()


