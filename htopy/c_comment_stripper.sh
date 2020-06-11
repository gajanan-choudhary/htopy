#!/usr/bin/env bash

# This file was obtained from the public domain. We do not claim ownership or
# copyright over this file. The source of this file is one of the answers on
# Stackoverflow, available at the following link:
# https://stackoverflow.com/questions/13061785/remove-multi-line-comments/13062682#13062682

[ $# -eq 2 ] && arg="$1" || arg=""
eval file="\$$#"
sed 's/a/aA/g;s/__/aB/g;s/#/aC/g;s/^[[:space:]]*$/aD/' "$file" |
          gcc -P -E $arg - |
          sed 's/aD//;s/aC/#/g;s/aB/__/g;s/aA/a/g'

