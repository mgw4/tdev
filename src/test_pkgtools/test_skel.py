import os
import functools

from pkgtools.mkskel import make_skel
from test_pkgtools.utils import chtmp


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


def test_make_skel(chtmp):
    project_name = "test_project"
    project_path = "test_path"
    version = "1.1"

    make_skel(project_name, project_path, version)
    path_dict = get_directory_structure(project_path)
    ex_dict = {
        'test_path': {
            '.gitignore': None,
            'src': {
                'requirements.txt': None,
                'MANIFEST.in': None,
                'setup.py': None,
                'test_project': {
                    '__init__.py': None
                }
            },
            'README.rst': None
        }
    }

    assert path_dict == ex_dict
