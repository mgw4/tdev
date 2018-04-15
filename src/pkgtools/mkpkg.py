import argparse
import logging
import os
import re

logger = logging.getLogger(__name__)


def _mkpkg(pkgar, base_path="./", version=None):
    assert isinstance(pkgar, list)

    tmp_dir = os.getcwd()
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        elif not os.path.isdir(base_path):
            raise Exception("{} not a directory".format(base_path))

        os.chdir(base_path)

        pkg = os.path.join(*pkgar)

        if not os.path.exists(pkg):
            os.mkdir(pkg)
        else:
            if not os.path.isdir(pkg):
                raise Exception("package path {} is not a directoy".format(pkg))
            logger.info("path already exists")

        init_file = os.path.join(pkg, "__init__.py")

        if not os.path.isfile(init_file):
            with open(init_file, 'w') as fp:
                if version:
                    fp.write("__VERSION__ = \"{}\"".format(version))

        else:
            logger.info("init file already there")
    finally:
        os.chdir(tmp_dir)


def make_package(package_name, base_path="./", version=None):
    path_list = []

    for i in package_name.split("."):
        if len(i) != 0:
            path_list.append(i)
            _mkpkg(path_list, base_path, version)


def update_version(package_name, version, base_path="./"):

    pkg_list = package_name.split(".")
    init_file = os.path.join(base_path, *pkg_list, "__init__.py")

    if not os.path.isfile(init_file):
        raise Exception("{} is not a valid __init__.py file".format(init_file))

    with open(init_file, 'r') as fp:
        orig_init = fp.read()

    new_init, count = re.subn("__VERSION__ = \"(.+)\"",
                              "__VERSION__ = \"{}\"".format(version),
                              orig_init)
    if count == 0:
        new_init = "__VERSION__ = \"{}\"\n".format(version) + new_init

    with open(init_file, 'w') as fp:
        fp.write(new_init)


def main_update():  # pragma: nocover
    p = argparse.ArgumentParser()
    p.add_argument("package_name", help="package name ie: pkgtools.test")
    p.add_argument("version", help="version number for the package",
                   default=None)
    p.add_argument("-base_path",
                   help="folder in which to create the package",
                   default="./")
    args = p.parse_args()

    update_version(args.package_name, args.version, args.base_path)


def main():  # pragma: nocover

    p = argparse.ArgumentParser()
    p.add_argument("package_name", help="package name ie: pkgtools.test")
    p.add_argument("-base_path",
                   help="folder in which to create the package",
                   default="./")
    p.add_argument("-version", help="version number for the package",
                   default=None)

    args = p.parse_args()
    make_package(args.package_name, args.base_path, args.version)


if __name__ == "__main__":  # pargma: nocover
    main()  # pragma: nocover
