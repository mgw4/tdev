import os
import pytest
import re


from pkgtools.mkpkg import make_package, update_version
from test_pkgtools.utils import (chtmp,
                                 get_version,
                                 get_init_file)


@pytest.mark.order1
def test_make_package(chtmp):
    pkg_name = "test"
    version = "1.0"
    base_path = "./base/abc"

    make_package(pkg_name)
    assert (os.path.isfile("./test/__init__.py"))

    make_package(pkg_name, base_path)

    init_file = os.path.join(base_path, pkg_name, "__init__.py")
    assert (os.path.isfile(init_file))

    pkg_name = "version"
    make_package(pkg_name, base_path, version)
    init_file = os.path.join(base_path, pkg_name, "__init__.py")
    with open(init_file, "r") as fp:
        v = fp.read()
    assert re.match(r"__VERSION__ = \"{}\"".format(version), v)

    # test init file already there
    pkg_name = "init.there"
    os.makedirs("init/there")
    with open("init/there/__init__.py", 'w') as fp:
        fp.write("")

    make_package(pkg_name)  # make sure no exception are raised

    # test pkgpath exists and not dir
    pkg_name = "test_notpath"

    with open(pkg_name, 'w') as fp:
        fp.write("")

    with pytest.raises(Exception):
        make_package(pkg_name)

    # test base_path exists and not dir
    base_path = "base_not_dir"
    with open(base_path, 'w') as fp:
        fp.write("")

    with pytest.raises(Exception):
        make_package(pkg_name, base_path)


def test_update_version(chtmp):
    # update package no version
    pkg_name = "test"
    version = "1.0"
    base_path = "./base/noversion"

    make_package(pkg_name, base_path)
    update_version(pkg_name, version, base_path)
    assert get_version(pkg_name, base_path) == version

    # update with other content in init no version
    with open(get_init_file(pkg_name, base_path), 'w') as fp:
        fp.write("a = [1,2,3]")

    # update with version present
    pkg_name = "test"
    orig_version = "1.0"
    new_version = "2.0"
    base_path = "./base/version"

    make_package(pkg_name, base_path, orig_version)
    update_version(pkg_name, new_version, base_path)
    assert get_version(pkg_name, base_path) == new_version

    # init file is a directory
    pkg_name = "test"
    orig_version = "1.0"
    new_version = "2.0"
    base_path = "./base/init_is_a_dir"

    init_file = get_init_file(pkg_name, base_path)
    os.makedirs(init_file)
    with pytest.raises(Exception) as exc:
        update_version(pkg_name, new_version, base_path)

    assert " is not a valid __init__" in str(exc.value)
