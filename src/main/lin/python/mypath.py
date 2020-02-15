import os


def my_cd(file_path, n=1):
    for i in range(n):
        file_path = os.path.dirname(file_path)
    return file_path


def get_path(which='dir_path'):
    """
    Function that detects if the script is run externally or within an IDE console.
    The paths change depending on the environment.
    Args:
        which (str): file_path, dir_path, root_path or data_path
    Returns:
        path (str): required path
    """
    if [x for x in os.environ if 'SPY' in x]:
        # Spyder - paths for testing in Spyder environment
        file_path = globals()['__file__']
        root_path = my_cd(file_path, 5)
        dir_path = my_cd(file_path, 1)
        data_path = my_cd(file_path, 1) + "/data"
    elif [x for x in os.environ if 'PYCHARM' in x]:
        if 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ:
            # PyCharm - paths for testing locally within PyCharm Python console
            root_path = os.getcwd()
            dir_path = root_path + '\\src\\main\\lin\\python'
            file_path = dir_path + '\\tinderbot.py'
            data_path = root_path + '\\src\\main\\lin\\data'
        else:
            # PyCharm - paths for testing in PyCharm run/debug
            file_path = os.path.abspath(__file__)
            root_path = my_cd(file_path, 5)
            dir_path = my_cd(file_path, 1)
            data_path = my_cd(file_path, 1) + "/data"
    if which == 'file_path':
        return file_path
    elif which == 'dir_path':
        return dir_path
    elif which == 'data_path':
        return data_path
    elif which == 'root_path':
        return root_path


# def make_editorconfig(dir_path):
#     """Create .editorconfig file in given directory and return filepath."""
#     path = Path(dir_path, '.editorconfig')
#     if not path.exists():
#         path.parent.mkdir(exist_ok=True, parent=True)
#         path.touch()
#     return path
