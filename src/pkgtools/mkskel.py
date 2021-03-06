import argparse
import os
import subprocess
import shlex
import shutil
import logging
import sys

import pkgtools.logging

from pkgtools.mksetup import (make_setup,
                              make_manifest,
                              make_readme,
                              make_requirements,
                              make_gitignore)
from pkgtools.mkpkg import make_package, update_version

logger = logging.getLogger(__name__)


def make_git(project_path):  # pragma: nocover  check_call will fail
    # make sure there is a / at the end
    project_path = os.path.join(project_path, "")
    cmd = "git -C {project_path} init".format(project_path=project_path)
    subprocess.check_call(shlex.split(cmd))
    logger.info("created git repository")
    logger.info("adding files to repository")
    cmd = "git -C {project_path} add -A".format(project_path=project_path)
    subprocess.check_call(shlex.split(cmd))
    cmd = ("git -C {project_path} commit "
           "-m 'Initial commit of skeleton'").format(project_path=project_path)
    subprocess.call(shlex.split(cmd))


def pipenv_install(project_dir, package_list, develop=False):
    assert os.path.isfile(os.path.join(project_dir, "Pipfile"))
    package_list = [package_list] if isinstance(
        package_list, str) else package_list
    tmp_dir = os.getcwd()

    try:
        os.chdir(project_dir)
        flags = "-d" if develop else ""
        for package in package_list:
            cmd = "pipenv install {} {}".format(flags, package)

            env = os.environ.copy()
            env.pop("VIRTUAL_ENV", None)  # disable the venv if present

            subprocess.check_call(shlex.split(cmd), env=env)

    except subprocess.CalledProcessError as ex:
        raise Exception(
            "There was a problem installing package to pipenv in folder %s", os.getcwd()) from ex
    finally:
        os.chdir(tmp_dir)


def make_pipenv(project_dir, python_binary=None):
    """make_pipenv

    prepare the pipenv

    :param project_dir: location to create the project
    :param python_binary: binary to create the pipenv from
    """

    assert os.path.isdir(project_dir), "the project directory must exist"

    tmp_dir = os.getcwd()

    try:
        os.chdir(project_dir)
        env = os.environ.copy()
        env.pop("VIRTUAL_ENV", None)  # disable the venv if present
        flags = "--python {}".format(python_binary) if python_version else ""
        cmd = "pipenv {flags} install".format(flags=flags)
        logger.info("creating pipenv")
        subprocess.check_call(shlex.split(cmd), env=env)
        logger.info("successfully created pipenv")

    except subprocess.CalledProcessError as ex:
        raise Exception(
            "There was a problem creating the pipenv in folder %s", os.getcwd()) from ex
    finally:
        os.chdir(tmp_dir)


def make_skel(project_name, project_path):
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
    make_package(project_name, src_path)


def launch_shell(project_path):
    tmpdir = os.getcwd()
    try:
        env = os.environ.copy()
        env.pop("VIRTUAL_ENV", None)  # disable the venv if present
        cmd = "pipenv shell"
        logger.info("launching shell")
        subprocess.check_call(shlex.split(cmd))
    except subprocess.CalledProcessError as ex:
        raise Exception("Problem running %s from %s", cmd, os.getcwd()) from ex
    finally:
        os.chdir(tmpdir)


def main():  # prgama: nocover

    default_path = os.getenv("DEVPATH",
                             os.path.join(os.getenv("HOME"), "github", "devel")
                             )
    default_path = os.path.join(default_path, "{project_name}")
    p = argparse.ArgumentParser(
        description="create a default setup for the project")
    p.add_argument("project_name", help="name of the project")
    p.add_argument("-project_path", help="path of the project",
                   default=default_path)
    p.add_argument("-version", help="the initial version of the project",
                   default="0.0.0")
    p.add_argument("-install_packages",
                   help="packages to install in venv", nargs='*', default=None)
    p.add_argument("-overwrite", help="will remove all files in the project path "
                   "before creting the new one", default=False,
                   action='store_true')
    p.add_argument("-no_shell",
                   help="will not launch the shell in the environement",
                   default=False, action='store_true')
    p.add_argument("-python_binary", 
                   help="path to the python binary",
                   default="/usr/local/bin/python3.6")

    dev_packages = ["ipython", "ipdb", "flake8", "autopep8", "pylint"]

    args = p.parse_args()
    args.project_path = args.project_path.format(
        project_name=args.project_name)
    if os.path.exists(args.project_path):
        if args.overwrite:
            logger.info("found existing project files, now removing them")
            import time
            print("-----------------------------------------------")
            print("sleeping for 5 seconds, pressk ctrl-c to cancel")
            print("-----------------------------------------------")
            time.sleep(5)
            shutil.rmtree(args.project_path)
            logger.info("folder %s has been removed", args.project_path)
        else:
            logger.info("not overwriting exiting")
            sys.exit(1)
    logger.info("creating project in {}".format(args.project_path))
    make_skel(args.project_name, args.project_path)
    make_git(args.project_path)
    src_path = os.path.join(args.project_path, "src")
    update_version(args.project_name, args.version, src_path, True)
    make_pipenv(args.project_path,
                python_binary=args.python_binary)
    pipenv_install(args.project_path, dev_packages, develop=True)

    if args.install_packages is not None:
        pipenv_install(args.project_path, args.install_packages)

    print(args.no_shell)
    if args.no_shell:
        launch_shell(args.project_path)


if __name__ == "__main__":  # pragma: nocover
    main()  # pragma: nocover
