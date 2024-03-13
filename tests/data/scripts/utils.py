import os, pathlib

def get_test_file_path(f: str):
    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / 'tests' / 'data' / 'source'
    return os.path.join(path, f)

def get_src_file_path(f: str):
    curr_path = pathlib.Path(".")
    path = curr_path.parent.absolute() / 'src' / 'data' / 'source'
    return os.path.join(path, f)

