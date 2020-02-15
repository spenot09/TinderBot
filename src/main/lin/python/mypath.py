import os


def get_path():
    """
    Function that detects if the script is run externally or within an IDE. The paths change depending on both situations.
    """
    if [x for x in os.environ if 'SPY' in x]:
        # Spyder - paths for testing in Spyder environment
        file_path = globals()['__file__']
        dir_path = my_cd(file_path, 4)
        data_path = my_cd(file_path, 1) + "/data"
    elif [x for x in os.environ if 'PYCHARM' in x]:
        if 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ:
            # PyCharm - paths for testing locally within PyCharm Python console
            file_path = os.getcwd() + '\\Kubrick Timetable\\Timetable.py'
            dir_path = my_cd(file_path, 2)
            data_path = dir_path + "/Data"
        else:
            # PyCharm - paths for testing in PyCharm run/debug
            file_path = os.path.abspath(__file__)
            dir_path = my_cd(file_path, 2)
            data_path = dir_path + "/Data"
    else:
        # Final path variables for production - DO NOT CHANGE
        file_path = os.path.abspath(__file__)
        dir_path = my_cd(file_path, 4)
        data_path = dir_path + "/Data"
    return file_path, dir_path, data_path
    return cwd


def my_cd(file_path, n=1):
    for i in range(n):
        file_path = os.path.dirname(file_path)
    return file_path


# def make_editorconfig(dir_path):
#     """Create .editorconfig file in given directory and return filepath."""
#     path = Path(dir_path, '.editorconfig')
#     if not path.exists():
#         path.parent.mkdir(exist_ok=True, parent=True)
#         path.touch()
#     return path
