from setuptools import setup, find_packages
import subprocess
import shlex
import shutil


def get_git_version(version):
    try:
        cmd = "git describe --tags --dirty"
        git_version = subprocess.check_output(shlex.split(cmd))
        git_version = git_version.strip()

        if git_version != version:
            with open(__file__, 'r') as fp:
                with open(__file__ + ".tmp", 'w') as fpw:
                    for line in fp.readlines():
                        print line
                        if line.startswith("    version = \""):
                            line = "    version = \"{}\"\n".format(git_version)
                        fpw.write(line)

            shutil.move(__file__ + ".tmp", __file__)

            version = git_version
    except:
        pass

    return version


def get_version():

    version = "0.0-dirty"
    version = get_git_version(version)  # --REMOVE-THIS-LINE

    return version

setup(
    name="tdev",
    version=get_version(),
    packages=find_packages(),
    scripts=['bin/tdev']
)
