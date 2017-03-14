import argparse
import os
import re
import shutil


_ROOT = os.path.abspath(os.path.dirname(__file__))


def make_setup(project_name, src_path):
    setup_path = os.path.join(src_path, 'setup.py')
    if os.path.exists(setup_path):
        try:
            setup_bak = "{}.bak".format(setup_path)
            shutil.copy(setup_path, setup_bak)
            print("copied the old setup to {}".format(setup_bak))
        except:
            pass
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


def main():
    p = argparse.ArgumentParser(
        description="create a default setup for the project")
    p.add_argument("project_name", help="name of the project")
    p.add_argument("project_path", help="path of the project")

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


if __name__ == "__main__":
    main()
