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
Colored output for terminals using ANSI escape characters.
"""

class colorClass:
    """Colored output on terminals."""
    NONE = '\033[0m'

    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    GRAY = '\033[0;37m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    PURPLE = '\033[0;35m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

