#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


htopy_cmds = ['htopy = htopy.__main__:main']

setup(
    name='htopy',
    version='0.1.0',
    description='A Python ctypes wrapper generator for C codes',
    keywords='wrapper, interface, ctypes, C, automatic',
    long_description=readme,
    author='Gajanan Choudhary',
    author_email='gajananchoudhary91@gmail.com',
    url='https://github.com/gajanan-choudhary/htopy',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={'console_scripts': htopy_cmds},
    package_data={'': ['*.sh']},
)
