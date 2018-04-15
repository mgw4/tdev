import os
import pytest
import pytest

from pkgtools.mksetup import (make_readme,
                              make_requirements,
                              make_manifest,
                              make_gitignore,
                              make_setup)
from test_pkgtools.utils import chtmp


@pytest.fixture
def project_path(chtmp):
    project_name = "test_project"
    os.makedirs(project_name)
    return project_name


@pytest.fixture
def src_path(project_path):
    src_path = os.path.join(project_path, "src")
    os.makedirs(src_path)
    return src_path


def test_make_readme(project_path):
    project_name = "test_readme"
    make_readme(project_path, project_name)
    assert os.path.isfile(os.path.join(project_path, "README.rst"))

    with open(os.path.join(project_path, "README.rst")) as fp:
        readme = fp.read()

    assert project_name in readme


def test_make_requirements(src_path):
    make_requirements(src_path)
    requires_file = os.path.join(src_path, 'requirements.txt')
    assert os.path.isfile(requires_file)


def test_make_manifest(src_path):
    make_manifest(src_path)
    manifest_file = os.path.join(src_path, 'MANIFEST.in')
    assert os.path.isfile(manifest_file)


def test_make_gitignire(project_path):
    make_gitignore(project_path)
    gitignore_file = os.path.join(project_path, '.gitignore')
    assert os.path.isfile(gitignore_file)
    with open(gitignore_file, 'r') as fp:
        gi = fp.read()

    assert "venv" in gi


def test_maske_setup(src_path):
    project_name = "test_proj"
    make_setup(project_name, src_path)

    setup_file = os.path.join(src_path, "setup.py")
    assert os.path.isfile(setup_file)

    with open(setup_file, 'r') as fp:
        setup = fp.read()

    assert project_name in setup

    # setup file already exists
    make_setup(project_name, src_path)
    assert os.path.isfile(setup_file)
    assert os.path.isfile(setup_file+".bak")

    # setup back already there make sure no exceptions raised
    make_setup(project_name, src_path)
    assert os.path.isfile(setup_file+".bak")
