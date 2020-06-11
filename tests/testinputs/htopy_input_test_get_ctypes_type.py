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


################################################################################
# WARNING:  DO NOT CHANGE ANY VARIABLE NAMES.


################################################################################
# basic_c_datatyes 'foo' is mapped to Python ctypes datatype 'ctypes.c_foo'
basic_c_datatypes = ['bool', 'int', 'long', 'float', 'double']
char_c_datatypes = ['char']

as_is_types = [
        '#include'     , '#define'      , '#if'          , '#ifdef'       ,
        '#ifndef'      , '#else'        , '#elif'        , '#endif'       ,
        '#error'       , 'typedef'      , 'struct'       , 'enum'         ,
        'class'        , 'public'       , 'private'      , 'protected'    ,
        'template'     , 'union'        , '#pragma'      , '{'            ,
        '}'            ,
        ]

# The following are enum type, stored as int in C.
enumtypes = []

################################################################################
# Note that these external library variables that MUST be set manually in
# build_types.py. Portability issues remain untested. They are printed as is.
#
# Some help for such 'externaltypes': Example, system-dependent type: time_t
# Important bash command to get type of time_t on systems. Bash command:
# echo | gcc -E -xc -include 'time.h' - | grep time_t | grep typedef
################################################################################
externaltypes=['MPI_Comm']

# The following are typedef'd to some data type in AdH. Ordered pairs needed.
typedefintypes  = []
typedefouttypes = []

# The following are typedef'd as pointers to some class/struct in AdH
typedefpointerintypes  = []
typedefpointerouttypes = []

# Supported data types without any issues.
# Enter your data structures here as a list of strings. ['foo', 'bar', ...]
supported_datastructs=[]

#Templates. Limited support for C++. Clever hacks are possible.
template_datastructs=[]

# The following in voidpointertypes MUST be accompanied with a '*' in header
# files as they will have to be treated as void POINTERS.
voidpointertypes = ['void', 'FILE', 'MPI_Status']

# These are outlier pointers we'll replace with void.
# Stuff line function pointers.
outliervoidpointertypes=[]

# These are datastructs that aren't supported. Pointers to these data structs
# MIGHT be supported as void pointers by adding them to the variable
# voidpointertypes above.
# If lines saying "KNOWN UNSUPPORTED LINE: ..." pop up in the output of a
# structure's constituents, DO NOT USE THAT DATASTRUCTURE.
# Note, although "FILE" is unsupported, "FILE*" is supported as a void pointer!
knownunsupportedtypes = ['FILE', 'MPI_Status']

#All remaining lines not fitting into above types are flagged as
# 'unknown' lines when printing.

