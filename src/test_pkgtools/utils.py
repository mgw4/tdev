import os
import pytest
import re


@pytest.fixture
def chtmp(tmpdir):
    tmp = tmpdir.chdir()
    yield
    tmp.chdir()


def get_init_file(pkg_name, base_path):
    pkg_path = pkg_name.split(".")
    return os.path.join(base_path, *pkg_path, "__init__.py")


def get_version(pkg_name, base_path):
    init_file = get_init_file(pkg_name, base_path)
    with open(init_file, 'r') as fp:
        init = fp.read()

    mg = re.search("__VERSION__ = \"(.+)\"", init)
    if not mg:
        return None
    version = mg.group(1)
    return version
