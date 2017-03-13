import shlex
import subprocess
# import sys
import re

from setuptools import setup, find_packages

git_stashed = False


class SetupException(Exception):
    pass


def set_git_version():
    try:
        cmd_git_version = "git describe --tags --dirty"
        cmd_git_hash = "git rev-parse HEAD"

        git_version = subprocess.check_output(shlex.split(cmd_git_version))
        ver = parse_version(git_version)
        git_hash = subprocess.check_output(shlex.split(cmd_git_hash))

        with open('VERSION', 'w') as fp:
            fp.write(ver + "\n")
            fp.write(git_version.decode('utf-8').strip())
            fp.write(git_hash.decode('utf-8').strip())

    except SetupException:
        raise

    # except Exception as e:
    #     print(e)
    #     pass


def parse_version(git_version):
    rem = re.match("^(?P<major>\d+)\.(?P<minor>\d+)"
                   "(?:$|[-.](?:(?P<micro>\d+)|(?P<dirty>dirty)$)"
                   "(?:.*?)(?:$|-(?P<dirty1>dirty)$))",
                   git_version.decode('utf-8'))
    if not rem:
        raise SetupException("The git tag must be set to a <number>.<number>. "
                             "Currently set to {}".format(git_version))

    rev = rem.groupdict()
    try:
        if rev['micro'] is None:
            rev['micro'] = 0
    except:
        rev['micro'] = 0

    ver = [str(rev['major']), str(rev['minor']), str(rev['micro'])]
    if rev['dirty'] is not None or rev['dirty1'] is not None:
        ver.append('dirty')

    return ".".join(ver)


def get_version():

    set_git_version()
    try:
        with open('VERSION', 'r') as fp:
            version = fp.readline().strip()
    except:
        raise SetupException("Unable to read the version file. something "
                             "unexpected happened in the prep function")

    return version


def get_requires():
    with open('requirements.txt', 'r') as fp:
        return fp.readlines()


def main():

    setup(
        name="tdev",
        version=get_version(),
        packages=find_packages(),
        requires=get_requires(),
        scripts=['bin/tdev'],
        entry_points={
            'console_scripts': ['mkpkg=pkgtools.mkpkg:main',
                                'mksetup=pkgtools.mksetup:main']
        },
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
