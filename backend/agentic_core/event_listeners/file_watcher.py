import os
import time

def watch_file_changes(directory="."):
    snapshot = set(os.listdir(directory))
    time.sleep(2)
    new_snapshot = set(os.listdir(directory))
    return new_snapshot - snapshot
