import os
import re
import shutil


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
        fp.write("\n")
        fp.write(project_name)
        fp.write("\n")
        fp.write("="*len(project_name))
        fp.write("\n")
        fp.write("")
        fp.write("\n")
        fp.write("Introduction")
        fp.write("\n")
        fp.write("------------")
        fp.write("\n")
