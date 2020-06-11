#!/usr/bin/env python

# htopy - A Python interface generator for C codes
# Copyright (C) 2020 Gajanan Choudhary (Email: gajananchoudhary91@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys

################################################################################
def check_if_file_exists(filename, filepath):
    """Check if file exists and is a file."""
    #currentpath = os.getcwd()
    fullpath = os.path.join(filepath, filename)
    print "Checking for existence of", fullpath

    if not os.path.exists(fullpath):
        sys.stderr.write("Specified file does not exist.\n")
        sys.exit(1)
    elif not os.path.isfile(fullpath):
        sys.stderr.write("Specified filename does not appear to be a file.\n")
        sys.exit(1)
    else:
        print 'Input file', filename, 'found at the above path'
        print 'Variables supplied in that file will be used as input to htopy.'

################################################################################
def import_htopy_input(filename, filepath):
    """Version-indendent import of user-supplied htopy_input.py file."""

    fullpath = os.path.join(filepath, filename)

    try:
        if sys.version_info<(3,0,0):
            from imp import load_source
            htopy_input = load_source('htopy_input', fullpath)
        elif sys.version_info>=(3,3,0) or sys.version_info<(3,4,9):
            from importlib.machinery import SourceFileLoader
            htopy_input = \
                    SourceFileLoader('htopy_input', fullpath).load_module()
        elif sys.version_info>=(3,5,0):
            import importlib.util
            spec = importlib.util.spec_from_file_location('htopy_input',
                                                          fullpath)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        else:
            sys.stderr.write("Don't know how to dynamically import module "
                             "for your version of Python. Sorry!\n")
            sys.exit(1)

    except:
        sys.stderr.write("Failed to load user-supplied input file.\n")
        sys.exit(1)

    return htopy_input

################################################################################
if __name__=="__main__":
    main();

