import re
import os

from setuptools import setup, find_packages


class SetupException(Exception):
    pass


def get_name():
    return "pkgtools"


def get_version():

    init_file = os.path.join(get_name(), "__init__.py")
    with open(init_file, 'r') as fp:
        init = fp.read()

    grp = re.search(r"__VERSION__ = \"(.+)\"", init)
    if not grp:
        raise SetupException("Unable to get version")
    return grp.group(1)


def get_requires():
    with open('requirements.txt', 'r') as fp:
        return fp.readlines()


def main():

    setup(
        name=get_name(),
        version=get_version(),
        packages=find_packages(),
        install_requires=get_requires(),
        scripts=[],
        entry_points={
            'console_scripts': ['mkpkg=pkgtools.mkpkg:main',
                                'mksetup=pkgtools.mksetup:main']
        },
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
