from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fr:
    requirements = fr.read()

setup(
    name='sway-smart-workspace',
    version='0.1.0',
    package_data={'templates': ['sway_smart_workspace/templates/*']},
    packages=['sway_smart_workspace', 'sway_smart_workspace/templates'],
    url='https://github.com/GeneralDenmark/PyOutputHandler',
    license='GNU Lesser General Public License v3 or later (LGPLv3+)',
    install_requires=requirements.split('\n'),
    entry_points={"console_scripts": ["sway-smart-workspace=sway_smart_workspace.__main__:main"]},
    scripts=["sway_smart_workspace/__main__.py"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Asger Geel Weirsøe',
    author_email='asger@weirsoe.dk',
    description='Simple program that looks through the sway config and finds the bound workspaces for each output, and then opening that workspace on the output, that the mouse is currently on.',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Desktop Environment :: Window Managers",
    ],
)
