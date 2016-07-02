import shlex
import subprocess
import sys

from setuptools import setup, find_packages

git_stashed = False


class SetupException(Exception):
    pass


def git_unstash():
    global git_stashed

    if git_stashed:

        cmd_git_unstash = "git stash pop"
        subprocess.check_call(cmd_git_unstash)

        print "###############################"
        print "# Restored uncomitted changes"
        print "###############################"


def git_stash():
    global git_stashed

    cmd_git_stash = "git stash"
    print ("#####################################################"
           "##########################################")
    print ("# Git repo is dirty will stash un-commited changes and "
           "restore them once the package is created")
    print ("#####################################################"
           "##########################################")
    subprocess.check_call(cmd_git_stash)

    git_stashed = True


def set_git_version():
    try:
        cmd_git_version = "git describe --tags --dirty"
        cmd_git_hash = "git rev-parse HEAD"

        git_version = subprocess.check_output(shlex.split(cmd_git_version))
        if git_version.find('dirty') != -1 and '--force' not in sys.argv:
            git_stash()
            raise SetupException("Git repository is in a dirty state. "
                                 "Not all changes have been commited. "
                                 "Use --force option to force the creation "
                                 "of the package")

        if '--force' in sys.argv:
            sys.argv.remove('--force')
            cmd_git_version = "git describe --tags "
            git_version = subprocess.check_output(shlex.split(cmd_git_version))

        git_hash = subprocess.check_output(shlex.split(cmd_git_hash))

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
            micro = '0'

        return ".".join([major, minor, micro])
    except ValueError:
        raise SetupException("The git tag must be set to a <number>.<number>. "
                             "Currently set to {}".format(split_version[0]))


def get_version():

    set_git_version()
    try:
        with open('VERSION', 'r') as fp:
            version = fp.readline().strip()
    except:
        raise SetupException("Unable to read the version file. something "
                             "unexpected happened in the prep function")
    version = parse_version(version)

    return version

setup(
    name="tdev",
    version=get_version(),
    packages=find_packages(),
    requires=[
        'pip',
        'virtualenvwraper'
    ],
    scripts=['bin/tdev'],
    entry_points={
        'console_scripts': ['mkpkg=pkgtools.mkpkg:main',
                            'mksetup=pkgtools.mksetup:main']
    },
    include_package_data=True,
)


git_unstash()
