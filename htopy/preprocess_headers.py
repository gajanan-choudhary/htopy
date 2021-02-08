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


################################################################################
def preprocess_C_comments(headerFile):
  """Return a string buffer having C header with comments stripped off.

  GCC is used to strip comments off of C header code.
  To do: Add support for other C compilers.
  """
  # Calling shell script to strip header file of its comments.
  # Shell script uses the compiler to preprocess the file. Ex. gcc -E ...
  # Preprocessor directives are preserved.
  dir_of_this_file = os.path.dirname(__file__)
  decomment_script = os.path.join(dir_of_this_file, "c_comment_stripper.sh")
  commentStripperCommand = [decomment_script + ' ' + headerFile]
  strippedHeaderFileContent = \
          subprocess.Popen(commentStripperCommand,
          stdout=subprocess.PIPE,
          shell=True).communicate()[0]

  #print("Stripping comments from C header file:", headerFile)
  #print(strippedHeaderFileContent)
  return StringIO(strippedHeaderFileContent.decode('utf-8'))

################################################################################
def process_spaces(line):
  """Strip spaces from the given line and return it.

  Replace all consecutive spaces with just a single space,
  and remove spaces at the beginning and end of the line.
  """
  for j in range (30):
      line = re.sub('  ', ' ', line)
  #print('Stripped    : ', line)
  return line.strip()

################################################################################
def insert_space_after_string(line, string):
  """Return line after add space after all occurences of given string."""
  return re.sub(string, string+' ', line)

################################################################################
def process_commaline(line):
  """Process line containing commas and return it.

  Assumption: Lines containing commas in headers are either multiple
  variable declarations in a single line, or are functions.
  """

  vartype = ''
  outline = ''
  nsemicolon = line.count(';')
  if (nsemicolon != 1): return line

  equalsplit = re.split('[=]+',line)
  commasplit = re.split('[,]+',line)
  myline = line
  for j in range (30):
      myline = re.sub('  ', ' ', myline)
  for j in range (10):
      myline = re.sub('\[ ', '[', myline)
      myline = re.sub(' \[', '[', myline)
      myline = re.sub('\] ', ']', myline)
      myline = re.sub(' \]', ']', myline)
      myline = re.sub('\{ ', '{', myline)
      myline = re.sub(' \{', '{', myline)
      myline = re.sub('\} ', '}', myline)
      myline = re.sub(' \}', '}', myline)
      myline = re.sub(', ', ',', myline)
      myline = re.sub(' ,', ',', myline)
  myline = re.sub('\t',  ' ', myline)
  myline = re.sub('\*', ' *', line) # To keep 1 space living before stars.
  for j in range (10): myline = re.sub('\* ', '*', myline)
  # Splits <space>, <,{}()*>.  below:
  wordsplit  = re.split('[^a-zA-Z0-9_\<\>\;\[\]\"]+',myline)
  nequal = line.count('=')
  ncomma = line.count(',')
  nwords = len(wordsplit)
  vsindex = 1 # Variable start index
  ignoredkwd = ['unsigned', 'static', 'extern', 'const']
  while (wordsplit[vsindex-1] in ignoredkwd):
    vsindex=vsindex+1

  # wordsplit[0 ... vsindex-1] should hopefully now be the variable type!
  #if (wordsplit[vsindex-1] in ['short', 'int', 'long', 'char']):
  for i in range(vsindex):
    vartype = vartype + wordsplit[i] + ' '
  #else:

  nopencurlbracs=0
  #outline = outline + commasplit[0]
  i=0
  #print('commasplit: ', commasplit)
  while (i<ncomma+1):
    if i==0: outline = outline + commasplit[i]
    else:    outline = outline + vartype + ' ' + commasplit[i]
    nopencurlbracs = nopencurlbracs + commasplit[i].count('{')
    nopencurlbracs = nopencurlbracs - commasplit[i].count('}')
    #print(i, nopencurlbracs, commasplit[i])
    if (nopencurlbracs!=0):
      i=i+1
      outline = outline + ',' + commasplit[i]
      nopencurlbracs = nopencurlbracs + commasplit[i].count('{')
      nopencurlbracs = nopencurlbracs - commasplit[i].count('}')
      #print(i, nopencurlbracs, commasplit[i])
      while (nopencurlbracs!=0):
        i=i+1
        #print("Searching for closing bracket:", line)
        outline = outline + ',' + commasplit[i]
        nopencurlbracs = nopencurlbracs + commasplit[i].count('{')
        nopencurlbracs = nopencurlbracs - commasplit[i].count('}')
        #print(i, nopencurlbracs, commasplit[i])
    if i!=ncomma: outline = outline + ';\n'
    else:           outline = outline + '\n'
    i=i+1
  #print('line      :', line)
  #print('equalsplit:', equalsplit)
  #print('commasplit:', commasplit)
  #print('wordsplit :', wordsplit)
  #print('outline   :', outline)
  return outline

################################################################################
def preprocess_header_file(htopy_obj, hfile):
  """Preprocess the given C header file to prep for ctypes generation.

  This makes it easier for the ctypes generator to do its job of
  automatically generating Python ctypes code.
  """

  interimHeaderFile = re.split('[^a-zA-Z0-9_]',hfile)[0]+htopy_obj.interimFileExtension
  buf = preprocess_C_comments(hfile)

  as_is_types = htopy_obj.htopy_input.as_is_types

  nopenbracs=0
  nopencurlbracs=0
  with open(interimHeaderFile, 'w') as writer:
    line = buf.readline()
    while line != '':  # The EOF char is an empty string

      line = insert_space_after_string(line, '}')

      line = process_spaces(line)

      ##############################################################
      # Hopefully normal lines, except for unforeseen problems
      ##############################################################
      splitline = re.split('[^a-zA-Z0-9_#*{}(),\[\]]+', line)
      if splitline[0] in as_is_types or splitline[0]=='virtual':
        if (splitline[0]!='enum' \
            and not(splitline[0]=='typedef' \
            and splitline[1]=='enum')):
          writer.write(line+'\n')
          nopenbracs  = nopenbracs + line.count('(') - line.count(')')
          #nopencurlbracs  = nopencurlbracs + line.count('{') - line.count('}')
          #print('Writing asis: ', line)
          line = buf.readline()
          continue
      elif (splitline[0]=='' and len(splitline)==1): # blank line
        line = buf.readline()
        continue
      elif (splitline[0]=='extern' \
          and splitline[1]=='C' \
          and splitline[2] == '{'):
        # Writes "extern C {" as-is.
        # That's because I don't yet know what to do with it.
        writer.write(line+'\n')
        line = buf.readline()
        continue
      #print('Processing  : ', line)

      ##############################################################
      # Remove functions from C header file
      # Side effect: it may delete for / while loops, and
      # at rare times, may also fail to remove a few functions
      ##############################################################
      # Find opening bracket
      nsemicolons = line.count(';')
      nopenbracs  = nopenbracs + line.count('(')
      if (nopenbracs==0 and nsemicolons==0 and line.count('{')==0):
        nopencurlbracs = nopencurlbracs - line.count('}')
        if (nopenbracs < 0): print('Weird line! ")" present without "("')
        line = line + ' ' + buf.readline().strip()
        nopenbracs = nopenbracs + line.count('(')
      if (nopenbracs>0): # Hopefully the only defining trait of a function definition?!
        # Find closing bracket
        nopenbracs  = nopenbracs - line.count(')')
        while (nopenbracs!=0):
          line = buf.readline()
          nopenbracs  = nopenbracs + line.strip().count('(') - line.strip().count(')')
        # Found the closing bracket. Continue to next loop iteration
        # Check if function has been defined in that line or the next!
        nsemicolons = line.count(';')
        nopencurlbracs = nopencurlbracs + line.count('{')
        if (nopencurlbracs==0 and nsemicolons==0):
          nopencurlbracs = nopencurlbracs - line.count('}')
          if (nopencurlbracs < 0): print('Weird line! "}" present without "{"')
          line = buf.readline()
          nopencurlbracs = nopencurlbracs + line.count('{')
          if (nopencurlbracs==0):
            nopencurlbracs = nopencurlbracs - line.count('}')
            if (nopencurlbracs < 0): print('Weird line! "}" present without "{"')
            continue
        if (nopencurlbracs>0): # Means a function has been defined
          nopencurlbracs = nopencurlbracs - line.count('}')
          while (nopencurlbracs!=0):
            line = buf.readline().strip()
            nopencurlbracs  = nopencurlbracs + line.count('{') - line.count('}')
            #print("Searching for closing bracket:", line)
        line = buf.readline()
        continue

      ##############################################################
      # Fix commas - multiple variable declarations in the same line
      ##############################################################
      myline = line
      while ((myline.count(';')==0 or (myline.count('{') - myline.count('}')!=0)) and line != ''):
      #while (myline.count(';')==0 and (myline.count('{') - myline.count('}')!=0) and line != ''):
        #(myline.count('{') - myline.count('}')!=0) part should only trigger for typedef enum. If it triggers for others, we're in trouble
        line = buf.readline()
        myline = myline+' '+line.strip()
      # Find comma in line
      commaline = re.split('[,]+', myline)
      if (len(commaline)!=1):
        # Tested manually
        #print("Comma line  :", myline)
        processedline = process_commaline(myline)
        #print(processedline)
        writer.write(processedline)
        line = buf.readline()
        continue

      #print('Writing line: ', myline)
      writer.write(myline+'\n')
      line = buf.readline()

################################################################################
def preprocess_all_files(htopy_obj):
  """Preprocess all C header files to prep for ctypes generation.

  This makes it easier for the ctypes generator to do its job of
  automatically generating Python ctypes code.
  """

  #for root, dirs, files in os.walk(htopy_obj.rootDir):
  for hfile in os.listdir(htopy_obj.rootDir):
      # Only process header files, and not any htopy interim header files in
      # case they exist:
      if (hfile.endswith(htopy_obj.inFileExtension)
              and not hfile.endswith(htopy_obj.interimFileExtension)):

          print(color.PURPLE+'Processing file: '+hfile+color.NONE) #filename
          preprocess_header_file(htopy_obj, hfile)
  print()

################################################################################

