import subprocess
import shlex
import sys

from setuptools import setup, find_packages


class SetupException(Exception):
    pass


def set_git_version():
    try:
        cmd = "git describe --tags --dirty"
        cmd1 = "git rev-parse HEAD"
        git_version = subprocess.check_output(shlex.split(cmd))
        if git_version.find('dirty') != -1 and '--force' not in sys.argv:
            raise SetupException("Git repository is in a dirty state. "
                                 "Not all changes have been commited. "
                                 "Use --force option to force the creation "
                                 "of the package")

        if '--force' in sys.argv:
            sys.argv.remove('--force')
            cmd = "git describe --tags "
            cmd1 = "git rev-parse HEAD"
            git_version = subprocess.check_output(shlex.split(cmd))

        git_hash = subprocess.check_output(shlex.split(cmd1))

        with open('VERSION', 'w') as fp:
            fp.write(git_version)
            fp.write(git_hash)

    except SetupException:
        raise

    except:
        pass


def parse_version(git_version):
    split_version = git_version.split('-')
    try:

        (major, minor) = split_version[0].split('.')

        if len(split_version) == 3:
            micro = split_version[1]
        else:
            micro = 0

        return ".".join([major, minor, micro])
    except ValueError:
        raise SetupException("The git tag must be set to a <number>.<number>. "
                             "Currently set to {}".format(split_version[0]))


def get_version():

    set_git_version()
    with open('VERSION', 'r') as fp:
        version = fp.readline().strip()
    version = parse_version(version)

    return version

setup(
    name="tdev",
    version=get_version(),
    packages=find_packages(),
    scripts=['bin/tdev'],
    include_package_data=True,
)
