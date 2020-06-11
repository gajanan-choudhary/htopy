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
Module for getting ctypes variable type from C variable type.

It is important that the functions in this file are only used after
prepping the C header files with functions in the preprocess_headers
module.
"""

import re

from htopy.colors import colorClass as color

################################################################################
DEBUG = 1

################################################################################
def unknown_line(line):
    """
    Returns string as an 'unknown' line not understood by htopy.
    """

    outputstring = '#UNKNOWN LINE: ' + line + ' #' + line
    if (DEBUG>0): print 'Output     :', color.RED, outputstring + color.NONE
    return outputstring

################################################################################
def known_unsupported_line(line):
    """
    Returns string as a known 'unsupported' line by htopy.
    """

    outputstring = '#KNOWN UNSUPPORTED LINE: ' + line + ' #' + line
    if (DEBUG>0): print 'Output     :', color.CYAN, outputstring + color.NONE
    return outputstring

################################################################################
def get_ctypes_type(line, hi):
    """Return ctypes equivalent from a line of preprocessed C header code."""

    # line :   line to be analyzed
    # hi   :   alias for user-supplied 'htopy_input.py' module

    ##############################################################
    # Fix pointers. The stars should stay separate from var name.
    ##############################################################
    myline = line
    myline = re.sub('\*', '* ', myline)
    myline = re.sub('\t', ' ', myline)
    for j in range (30):
        myline = re.sub('  ',   ' ', myline)
        myline = re.sub(' \*', '* ', myline)
    line = myline

    ##############################################################
    # Start analyzing parts of line.
    ##############################################################
    uflag = '' # Flag for unsigned stuff
    splitline = re.split('[^a-zA-Z0-9*#_{}\[\]=]+',line,1)
    myline = line
    if (splitline[0]=='struct'       or
            splitline[0]=='enum'     or
            splitline[0]=='unsigned' ):
        if (DEBUG>1): print line.count("{"), line.count(";")
        if (splitline[0]=='unsigned'): uflag = 'u'
        if (line.count('{')==0 and line.count(';')==1):
            # This would mean its a struct variable declaration.
            myline = splitline[1]
            splitline = re.split('[^a-zA-Z0-9*#_{}\[\]=]+',splitline[1],1)

    nstars = splitline[0].count('*')
    if (nstars>0): splitstar = re.split('\*', myline)
    else:          splitstar = re.split('[^a-zA-Z0-9_]',myline,1)

    if (DEBUG>1): print '\nsplitline  : ', splitline
    if (DEBUG>1): print 'splitstar  : ', splitstar
    if (DEBUG>1): print 'Star count : ', nstars

    # Cannot handle lines with multiple semicolons.
    if (line.count(';')>1): return unknown_line(line)

    ##############################################################
    # Deal with easy types first.
    ##############################################################
    if splitline[0] in hi.as_is_types:
        # Special treatment for #include statements
        # #include <> left as is
        # #include "BLAH.h" translated as "from BLAH_h import *"
        if (splitline[0]=='#include'):
            if splitline[1].count('\"')>0:
                line = 'from ' \
                     + re.split('[^a-zA-Z0-9_\/]+',splitline[1],1)[0] \
                     + '_h import *    #' \
                     + line

        # Special treatment for #ifdef statements
        # #ifdef _MESSG translated to "    if _MESSG==ON:    #ifdef _MESSG"
        if (splitline[0]=='#ifdef'):
            line = 'if (' + splitline[1] + '==ON):    ' + line

        # Special treatment for struct definitions
        if (splitline[0]=='typedef' and
                re.split('[^a-zA-Z0-9#*_]+',splitline[1])[0]=='struct'):
            line = 'class (ctypes.Structure): \n    _fields_ = [    #' + line

        if (DEBUG>0): print 'Output     :', color.YELLOW, line, color.NONE
        return line

    elif splitline[0] in hi.knownunsupportedtypes:
        return known_unsupported_line(line)

    ##############################################################
    # Now deal with the complicated types.
    ##############################################################
    # Get base variable type
    i=0
    outputcolor = color.GREEN
    if splitstar[i] in hi.basic_c_datatypes:
        ctypestring = 'ctypes.c_'+uflag+splitstar[i]
    elif splitstar[i] in hi.char_c_datatypes:
        ctypestring = 'ctypes.c_'+splitstar[i]
        if (uflag=='u'): ctypestring = 'ctypes.c_ubyte'
        outputcolor = color.BLUE
    elif splitstar[i] in hi.enumtypes:
        ctypestring = 'ctypes.c_int'
    elif splitstar[i] in hi.typedefintypes:
        index = hi.typedefintypes.index(splitstar[i])
        ctypestring = hi.typedefouttypes[index]
        if (splitstar[i]=='GCHAR'):
            outputcolor = color.BLUE
    elif splitstar[i] in hi.typedefpointerintypes:
        index = hi.typedefpointerintypes.index(splitstar[i])
        ctypestring = 'ctypes.POINTER('+hi.typedefpointerouttypes[index]+')'
        if hi.typedefpointerouttypes[index] in hi.voidpointertypes:
            ctypestring = 'ctypes.c_void_p'
    elif splitstar[i] in hi.supported_datastructs:
        ctypestring = splitstar[i]
    elif splitstar[i] in hi.externaltypes:
        ctypestring = splitstar[i] # Must be set in build_types.py
    elif splitstar[i] in hi.outliervoidpointertypes:
        ctypestring = 'ctypes.c_void_p'
    elif splitstar[i] in hi.template_datastructs:
        splitline = re.split('[^a-zA-Z0-9\*\_\[\]\=]+',splitline[1],1)
        if (DEBUG>1): print 'splitline  : ', splitline
        ctypestring = splitstar[i]+'_'+splitline[0]
        #ctypestring = splitstar[i]+'_'+re.split('[^a-zA-Z0-9_]',splitline[0])[1]
    elif splitstar[i] in hi.voidpointertypes:
        if nstars==0: return known_unsupported_line(line)
        else:         nstars = nstars-1
        ctypestring = 'ctypes.c_void_p'
    elif (uflag=='u'):
        i=i-1
        ctypestring = 'ctypes.c_uint'
    elif (splitstar[i]=='unsigned' and nstars>0):
        ctypestring = 'ctypes.c_uint'
    elif (splitstar[i] in hi.knownunsupportedtypes and
            splitstar[i] not in hi.voidpointertypes  ):
        return known_unsupported_line(line)
    else:
        return unknown_line(line)

    ## Search for brackets
    i=i+1
    if len(splitline)>1:
        while (splitline[i]==''):i=i+1
    nopeningbrackets = splitline[i].count('[')
    nclosingbrackets = splitline[i].count(']')
    if (nopeningbrackets != nclosingbrackets):
        return unknown_line(line)
    bracketline = re.split('[^a-zA-Z0-9_#*{}]+', splitline[i])
    if (DEBUG>1): print 'bracketline: ', bracketline
    if (DEBUG>1): print 'bracketcnt : ', nopeningbrackets, \
                        '"[" and', nclosingbrackets, '"]"'

    # If you are here, you are hopefully a proper variable.
    ctypesvar = bracketline[0]
    # This is variable is finally printed in the output file.
    outputstring  ='               ("'+ctypesvar+'"'+', '
    stringendpart ='), #'+line

    for j in range(nopeningbrackets,0,-1):
      outputstring = outputstring + '('
    for j in range(nstars):
      outputstring = outputstring + 'ctypes.POINTER('

    outputstring = outputstring + ctypestring

    for j in range(nstars):
      outputstring = outputstring + ')'
    for j in range(nclosingbrackets,0,-1):
      outputstring = outputstring + '*'+ bracketline[j]+')'

    outputstring = outputstring + stringendpart

    if (DEBUG>0): print 'Output     :', outputcolor, outputstring + color.NONE
    return outputstring

################################################################################
if __name__ == "__main__":
    pass

