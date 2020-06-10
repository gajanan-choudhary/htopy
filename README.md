# htopy - A Python interface generator for C codes

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
    * [Dependencies](#dependencies)
    * [Usage](#usage)
* [Features](#features)
* [Status](#status)
* [License](#license)
* [Contributors](#contributors)
* [Acknowledgments](#acknowledgments)

## General info
This software generates a Python `ctypes` wrapper from C header files of
libraries. The motivation for this work is to quickly wrap entire libraries or
software into Python 'quickly' while giving users full/significant control over
what data structures and functions they wish to wrap.

## Setup
### Dependencies
* Bash
* GCC -- for now; workaround is possibly easy: Change the compiler in the bash script.
* Python 2.7 -- for now; hopefully we'll make it 3-compatible later.

### Usage
Create and maintain an input file named `htopy_input.py` for use with `htopy`.
This file must contain lists that identify the C data structures that you want
to be wrapped into your Python interface. Note that there may be
OS/architecture-dependent data types which, you may yourself have to dig into
for your system and find the base type of. See the examples for help.

## Features
List of features that are ready:
* Partially automates writing the `ctypes`-wrapped headers
* User decides how deep the C code is wrapped into Python
* Compiler-flag-dependent structs can be smartly dealt with
* With some clever hacks, significant chunks of C++ can also be wrapped

To-do list:
* Complete automation is the ultimate goal
* Automate dealing with OS/architecture-dependent data types
* Enable options to use compilers other than GCC
* Make the source code Python-version-independent

## Status
Project is: _in progress_.

## License
The licensing spirit of this code is very much same as that of
[SWIG](http://www.swig.org/legal.html), that is, the `htopy` source code is to
remain GPL'd, whereas `htopy` output is free for users to use based on their
choice/requirements. Note that the `htopy`-generated output code for your input
C software may be governed by the licensing terms of that C software.

The `htopy` source code is licensed under the terms of GNU GPL v3.0. See the
[LICENSE file](https://github.com/gajanan-choudhary/htopy/blob/master/LICENSE)
in the main/root directory of this repository, or visit
[https://www.gnu.org/licenses/](https://www.gnu.org/licenses/) for details.

## Contributors
* **Gajanan Choudhary** - [website](https://users.oden.utexas.edu/~gajanan/)

## Acknowledgments
* `ctypes` documentation
* Stackoverflow

