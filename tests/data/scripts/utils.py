import os, pathlib

def get_file_path(dir: str, f: str):
    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / dir / "data" / "source"
    return os.path.join(path, f)