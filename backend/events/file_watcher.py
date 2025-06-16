import os
import time

def watch_project_files(callback, root_path="."):
    last_state = {}
    while True:
        current_state = {}
        for dirpath, _, filenames in os.walk(root_path):
            for f in filenames:
                path = os.path.join(dirpath, f)
                if not path.startswith("./.git") and os.path.isfile(path):
                    current_state[path] = os.path.getmtime(path)

        if current_state != last_state:
            callback(current_state)
            last_state = current_state
        time.sleep(5)
