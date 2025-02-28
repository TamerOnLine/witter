import os
import sys
import subprocess


def check_python():
    """Check if Python is installed."""
    if sys.version_info.major < 3:
        print("Python 3 is required to run this program.")
        sys.exit(1)


def install_requirements():
    """Automatically install required dependencies."""
    print(" Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)


def run_app():
    """Run the application."""
    print(" Running the app on http://127.0.0.1:8000/")
    subprocess.run(
        [
            sys.executable, "-m", "uvicorn", "api:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ],
        check=True
    )


if __name__ == "__main__":
    check_python()
    install_requirements()
    run_app()
