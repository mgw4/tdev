import argparse
import os
import re
import shutil

from pkgtools.mkpkg import make_package

_ROOT = os.path.abspath(os.path.dirname(__file__))


def make_setup(project_name, src_path):
    setup_path = os.path.join(src_path, 'setup.py')
    if os.path.exists(setup_path):
        setup_bak = "{}.bak".format(setup_path)
        shutil.copy(setup_path, setup_bak)
        print("copied the old setup to {}".format(setup_bak))

    with open(setup_path, 'w') as fp:
        with open(os.path.join(_ROOT, 'setup_template.dat'), 'r') as fpr:
            tmpl = fpr.read()
            tmpl = re.sub('projname', project_name, tmpl)
            fp.write(tmpl)


def make_manifest(src_path):
    with open(os.path.join(src_path, "MANIFEST.in"), 'w') as fp:
        fp.write("include VERSION requirements.txt")


def make_gitignore(project_path):
    with open(os.path.join(_ROOT, "Python.gitignore.dat"), 'r') as fp:
        with open(os.path.join(project_path, ".gitignore"), 'w') as fpw:
            fpw.write(fp.read())


def make_requirements(project_path):
    with open(os.path.join(project_path, 'requirements.txt'), 'w') as fp:
        fp.write('')


def make_readme(project_path, project_name):

    with open(os.path.join(project_path, "README.rst"), "w") as fp:
        fp.write("="*len(project_name))
        fp.write(project_name)
        fp.write("="*len(project_name))
        fp.write("")
        fp.write("Introduction")
        fp.write("------------")


def main():  # pragma: nocover
    p = argparse.ArgumentParser(
        description="create a default setup for the project")
    p.add_argument("project_name", help="name of the project")
    p.add_argument("project_path", help="path of the project")
    p.add_argument("-version", help="the initial version of the project",
                   default="0.0.0")

    args = p.parse_args()

    src_path = os.path.join(args.project_path, 'src')

    try:
        os.makedirs(src_path)
    except OSError as e:
        if e.errno != 17:
            raise

    make_setup(args.project_name, src_path)
    make_manifest(src_path)
    make_requirements(src_path)
    make_gitignore(args.project_path)

    make_readme(args.project_path, args.project_name)
    make_package(args.project_name, src_path, args.version)


if __name__ == "__main__":  # pargma: nocover
    main()  # pragma: nocover
