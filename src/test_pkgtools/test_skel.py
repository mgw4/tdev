import functools
import os
import pytest
import shlex
import subprocess

from pkgtools.mkskel import make_skel, make_pipenv, pipenv_install
from test_pkgtools.utils import chtmp  # NOQA


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


@pytest.mark.parametrize("python_version",
                         [2.7,
                          3.5,
                          3.6,
                          None,
                          pytest.param("not_a_version", marks=pytest.mark.xfail)])
def test_make_pipenv(chtmp, python_version):  # NOQA
    project_path = "test_path_{}".format(python_version)
    os.makedirs(project_path)

    make_pipenv(project_path, python_version=python_version)
    pipfile = os.path.join(project_path, "Pipfile")

    assert os.path.isfile(pipfile)
    assert os.path.isfile(pipfile + ".lock")
    python_version = "3.5" if not python_version else python_version
    subprocess.check_call(shlex.split(
        "grep -q {} {}".format(python_version, pipfile)))


@pytest.mark.parametrize(["package", "devel"],
                         [("ipython", True),
                          (["requests", "flake8"], False),
                          pytest.param("not_a_package", True, marks=pytest.mark.xfail)])
def test_pipenv_install(chtmp, package, devel):
    project_path = "test_path"
    os.makedirs(project_path)

    make_pipenv(project_path)
    pipenv_install(project_path, package, develop=devel)


def test_make_skel(chtmp):  # NOQA
    project_name = "test_project"
    project_path = "test_path"

    make_skel(project_name, project_path)
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
