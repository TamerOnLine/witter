import os
import sys
import subprocess

def activate_virtual_env():
    """تفعيل البيئة الافتراضية بغض النظر عن نظام التشغيل."""
    venv_path = os.path.join(os.getcwd(), "venv")

    if not os.path.exists(venv_path):
        print("⚠️ البيئة الافتراضية غير موجودة! يرجى إنشاؤها باستخدام: python -m venv venv")
        sys.exit(1)

    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")

    return activate_script

def run_api():
    """تشغيل Uvicorn لتشغيل FastAPI."""
    activate_script = activate_virtual_env()

    if sys.platform == "win32":
        command = f"cmd /c \"{activate_script} & uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload\""
    else:
        command = f"bash -c 'source {activate_script} && uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload'"

    subprocess.run(command, shell=True)

if __name__ == "__main__":
    run_api()
