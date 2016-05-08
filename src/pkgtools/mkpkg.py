import os
import argparse
import logging

logger = logging.getLogger(__name__)


def mkpkg(pkgar):

    pkg = os.path.join(*pkgar)

    if not os.path.exists(pkg):
        os.mkdir(pkg)
    else:
        logger.info("path already exists")

    init_file = os.path.join(pkg, "__init__.py")

    if not os.path.isfile(init_file):
        fp = open(init_file, "w")
        fp.close()
    else:
        logger.info("init file already there")


def main():

    p = argparse.ArgumentParser()
    p.add_argument("package_name", help="the name of the package to create in"
                   " path notation")

    args = p.parse_args()

    path_list = []

    for i in os.path.split(args.package_name):

        if len(i) != 0:
            path_list.append(i)
            mkpkg(path_list)

if __name__ == "__main__":
    main()
