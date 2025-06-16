import os

def list_project_files(root_path: str = "."):
    files = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if not full_path.startswith("./.git"):
                files.append(full_path)
    return files
