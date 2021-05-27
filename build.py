import argparse
import subprocess
import pathlib
import os

def main():
    parser = argparse.ArgumentParser("Build script for pypi and pypi test")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--test', action='store_true', help='Build to test.pypi.org')
    group.add_argument('--pypi', action='store_true', help='Build to pypi.org')
    group.add_argument('--check', action='store_true', help='Displays the twine check for dist')
    args = parser.parse_args()

    for path in pathlib.Path('dist').iterdir():
        os.remove(path)

    subprocess.call(['python3', 'setup.py', 'sdist', 'bdist_wheel'], stdout=subprocess.PIPE)

    if args.test:
        subprocess.call(['twine', 'upload', '--config-file', '.pypirc', '--repository', 'testpypi', 'dist/*'])

    elif args.pypi:
        subprocess.call(['twine', 'upload', '--config-file', '.pypirc', '--repository', 'pypi', 'dist/*'])

    else:
        subprocess.call(['twine', 'check', 'dist/*'])


if __name__ == '__main__':
    main()
