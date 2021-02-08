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

from __future__ import print_function
import os
import subprocess
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
import re

from htopy.colors import colorClass as color
from htopy.preprocess_headers import preprocess_all_files
from htopy.process_headers import get_ctypes_type

################################################################################
class Htopy:
    ############################################################################
    def __init__(self):
        """Set default variables of htopy."""

        # Path containing input files -- Simply the current directory.
        self.rootDir = os.getcwd()

        # File extensions
        self.inFileExtension = '.h'
        self.interimFileExtension = '-htopy-interim.h'
        self.outFileExtension = '_h.py'

        # Debug levels for output logging
        self.debugLevel = 0

    ############################################################################
    def initialize(self):
        """Write intermediate, cleaned up header files first."""
        preprocess_all_files(self)

    ############################################################################
    def run(self):
        """Write python classes from intermediate header files."""
        #for root, dirs, files in os.walk(self.rootDir):
        for hfile in os.listdir(self.rootDir):
          if hfile.endswith(self.interimFileExtension):
            pyfile = re.split('[^a-zA-Z0-9_]',hfile)[0]+self.outFileExtension
            print('\n'+color.PURPLE+'Processing file: '+hfile+color.NONE) #filename

            # Calling sed script to strip header file of its comments.
            bashcommand = ['cat ' + hfile]
            strippedhfilecontent = subprocess.Popen(bashcommand,stdout=subprocess.PIPE,shell=True).communicate()[0]

            #print(strippedhfilecontent)
            buf = StringIO(strippedhfilecontent.decode('utf-8'))
            with open(pyfile, 'w') as writer:
              writer.write('#!/usr/bin/python\n')
              writer.write('import ctypes\n')
              writer.write('##############################################################################################\n')
              line = buf.readline()
              while line != '':  # The EOF char is an empty string
                line = line.strip()

                outputstring = get_ctypes_type(line, self.htopy_input)
                writer.write(outputstring+'\n')

                line = buf.readline()
              writer.write('\n##############################################################################################\n')
              writer.write('def tests():\n')
              writer.write('    pass\n')
              writer.write('\n##############################################################################################\n')
              writer.write('if (__name__ == \'__main__\'):\n')
              writer.write('    tests()\n')
        print() #new line

    ############################################################################
    def finalize(self):
        """Finalize htopy by removing intermediate files."""

