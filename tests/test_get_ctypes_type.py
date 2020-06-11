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

import unittest

from .context import htopy
from htopy import process_headers

from testinputs import htopy_input_test_get_ctypes_type as htopy_input

################################################################################
LOCALDEBUG = 0

################################################################################
class Test_get_ctypes_type(unittest.TestCase):
    """Basic tests checking that types are mapped correctly."""

    def test_main(self):
        """Basic tests checking that types are mapped correctly."""
        testlist = [ 'int ijk_123[51];'        ,
                     'SSUPER_MODEL** sm;'      ,
                     'char* filename[MAXLINE];',
                     'unsigned int modulus;'   ,
                     'MPI_Comm ADH_COMM;'      ,
                     'hid_t* group_mesh[5];'   ,
                     'void myvoidvar;'         ,
                     'ID_LIST_ITEM** myptr[2];',
                     '#ifdef _MESSG'           ,
                     'int* myint[2][3];'       ,
                     'int** myint[4][5];'      ,
                     'int** myint[6];'         ,
                     'int* (*myint)[2][3];'    ,
                     'GINT unknown;'           ,
                     'enum CARD myenum;'       ,
                     '#include  "mpi.h" '      ,
                     '#include <stdio.h> '     ,
                     'FILE myfile;'            ,
                     'FILE *myfileptr;'        ,
                     'int a;;'                 ,
                    ]

        answer = { 'int ijk_123[51];'        : '               ("ijk_123", (ctypes.c_int*51)), #int ijk_123[51];',
                   'SSUPER_MODEL** sm;'      : '#UNKNOWN LINE: SSUPER_MODEL** sm; #SSUPER_MODEL** sm;',
                   'char* filename[MAXLINE];': '               ("filename", (ctypes.POINTER(ctypes.c_char)*MAXLINE)), #char* filename[MAXLINE];',
                   'unsigned int modulus;'   : '               ("modulus", ctypes.c_uint), #unsigned int modulus;',
                   'MPI_Comm ADH_COMM;'      : '               ("ADH_COMM", MPI_Comm), #MPI_Comm ADH_COMM;',
                   'hid_t* group_mesh[5];'   : '#UNKNOWN LINE: hid_t* group_mesh[5]; #hid_t* group_mesh[5];',
                   'void myvoidvar;'         : '#KNOWN UNSUPPORTED LINE: void myvoidvar; #void myvoidvar;',
                   'ID_LIST_ITEM** myptr[2];': '#UNKNOWN LINE: ID_LIST_ITEM** myptr[2]; #ID_LIST_ITEM** myptr[2];',
                   '#ifdef _MESSG'           : 'if (_MESSG==ON):    #ifdef _MESSG',
                   'int* myint[2][3];'       : '               ("myint", ((ctypes.POINTER(ctypes.c_int)*3)*2)), #int* myint[2][3];',
                   'int** myint[4][5];'      : '               ("myint", ((ctypes.POINTER(ctypes.POINTER(ctypes.c_int))*5)*4)), #int** myint[4][5];',
                   'int** myint[6];'         : '               ("myint", (ctypes.POINTER(ctypes.POINTER(ctypes.c_int))*6)), #int** myint[6];',
                   'int* (*myint)[2][3];'    : '               ("*", ((ctypes.POINTER(ctypes.c_int)*2)*myint)), #int* (* myint)[2][3];',
                   'GINT unknown;'           : '#UNKNOWN LINE: GINT unknown; #GINT unknown;',
                   'enum CARD myenum;'       : '#UNKNOWN LINE: enum CARD myenum; #enum CARD myenum;',
                   '#include  "mpi.h" '      : 'from mpi_h import *    ##include "mpi.h" ',
                   '#include <stdio.h> '     : '#include <stdio.h> ',
                   'FILE myfile;'            : '#KNOWN UNSUPPORTED LINE: FILE myfile; #FILE myfile;',
                   'FILE *myfileptr;'        : '               ("myfileptr", ctypes.c_void_p), #FILE* myfileptr;',
                   'int a;;'                 : '#UNKNOWN LINE: int a;; #int a;;',
                  }

        # Test
        for line in testlist:
            outline = process_headers.get_ctypes_type(line, htopy_input)
            #print(line+" ---->>>> "+outline)
            self.assertEqual(outline, answer[line])


################################################################################
if __name__ == '__main__':
    unittest.main()

