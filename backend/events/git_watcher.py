import subprocess
import time

def detect_git_change(interval=5):
    last_status = None
    while True:
        try:
            status = subprocess.check_output(["git", "status", "--porcelain"]).decode("utf-8")
            if status != last_status:
                print("[Event] Alterações no Git detectadas.")
                last_status = status
        except:
            pass
        time.sleep(interval)
