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

"""
Module for parsing command line arguments to htopy.
"""

from __future__ import print_function
import os
import sys
import argparse as ap

from .import_htopy_input import check_if_file_exists

helpstring = (
"""
htopy - A Python interface generator for C codes
Copyright (C) 2020 Gajanan Choudhary (gajananchoudhary91@gmail.com)

Example usage 1:
    a. Copy all C header files in a new folder
    b. Copy the file htopy_input.py into that folder, and edit it to suite your
       needs
    c. Set the current directory to that folder
    d. Run the following command:
           htopy
    e. Edit the generated *_h.py files - these form the ctypes Python interface
    f. Test, test, test!

Example usage 1:
    a. Copy all C header files in a new folder
    b. Set the current directory to that folder
    c. Edit the file htopy_input.py to suite your needs, wherever it may be
    d. Run the following command:
            htopy  -i htopy_input.py  -p <path to htopy_input.py>
    e. Edit the generated *_h.py files - these form the ctypes Python interface
    f. Test, test, test!
"""
)


################################################################################
def parse_args():
    """Parsing command line arguments supplied to htopy."""
    p = ap.ArgumentParser(description=helpstring,
                          formatter_class=ap.RawDescriptionHelpFormatter
                          )

    p.add_argument("-i", "--input", type=str,
                   default="htopy_input.py",
                   help=("Input file for htopy; you must edit the sample "
                         "file that was supplied to you with htopy "
                         "(default: %(default)s)")
                   )
    p.add_argument("-p", "--path", type=str,
                   default="./",
                   help=("Input file path; (default: %(default)s)")
                   )

    # To do:
    #
    #p.add_argument("-v", "--verbosity",
    #               type=int, choices=[0,1,2], default=0,
    #               help="Increase output verbosity (default: %(default)s)"
    #               )
    #p.add_argument("-d", "--debug",
    #               type=int, choices=[0,1], default=0,
    #               help="Run in debug mode (default: %(default)s)"
    #               )

    args = p.parse_args()

    check_if_file_exists(args.input, args.path)

    return args


################################################################################
if __name__=="__main__":
    try:
        args = parse_args()
        print(args)
    except:
        print('Try $ python parse_args.py -h')

    print()

