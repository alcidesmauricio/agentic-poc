import os

def list_project_files(root_dir="."):
    files = []
    for root, dirs, filenames in os.walk(root_dir):
        for name in filenames:
            files.append(os.path.join(root, name))
    return files
