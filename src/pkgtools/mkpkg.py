import argparse
import logging
import os

logger = logging.getLogger(__name__)


def _mkpkg(pkgar, base_path="./", version=None):
    assert isinstance(pkgar, list)

    tmp_dir = os.getcwd()
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        elif not os.path.isdir(base_path):
            raise ("{} not a directory".format(base_path))

        os.chdir(base_path)

        pkg = os.path.join(*pkgar)

        if not os.path.exists(pkg):
            os.mkdir(pkg)
        else:
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


def main():

    p = argparse.ArgumentParser()
    p.add_argument("package_name", help="package name ie: pkgtools.test")
    p.add_argument("-base_path",
                   help="folder in which to create the package",
                   default="./")
    p.add_argument("-version", help="version number for the package",
                   default=None)

    args = p.parse_args()
    make_package(args.package_name, args.base_path, args.version)


if __name__ == "__main__":
    main()
