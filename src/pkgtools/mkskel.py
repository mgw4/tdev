import argparse
import os

from pkgtools.mksetup import (make_setup,
                              make_manifest,
                              make_readme,
                              make_requirements,
                              make_gitignore)
from pkgtools.mkpkg import make_package


def make_skel(project_name, project_path, version):
    src_path = os.path.join(project_path, 'src')

    try:
        os.makedirs(src_path)
    except OSError as e:
        if e.errno != 17:
            raise

    make_setup(project_name, src_path)
    make_manifest(src_path)
    make_requirements(src_path)
    make_gitignore(project_path)

    make_readme(project_path, project_name)
    make_package(project_name, src_path, version)


def main():  # prgama: nocover

    p = argparse.ArgumentParser(
        description="create a default setup for the project")
    p.add_argument("project_name", help="name of the project")
    p.add_argument("project_path", help="path of the project")
    p.add_argument("-version", help="the initial version of the project",
                   default="0.0.0")

    args = p.parse_args()
    make_skel(args.project_name, args.project_path, args.version)


if __name__ == "__main__":  # pragma: nocover
    main()  # pragma: nocover
