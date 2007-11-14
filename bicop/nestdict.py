# nestdict.py
#
# Copyright 2002 Wichert Akkerman <wichert@simplon.biz>
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Calculate shared library dependencies

""" Nested dictionaries

This module implements the NestedDict class, which is a simple
tool to make it simpler to deal with nested dictionaries.

Here is a simple example showing how to use it::

  dict=NestedDict()
  dict["sql/username"]="guest"
  dict["sql/password"]="secret"

  print "Username: " + dict["sql"]["username"]
  print "Password: " + dict["sql/password"]
"""

import types, UserDict

class NestedDict(UserDict.UserDict):
    """Nested dictionary class

    @ivar seperator: seperator string
    @type seperator: string
    """
    def __init__(self, dict=None):
        self.seperator="/"
        UserDict.UserDict.__init__(self, dict)


    def __getitem__(self, key):
        keys=key.split(self.seperator)
        top=self.data
        while len(keys)>1:
            top=top[keys[0]]
            keys=keys[1:]

        if type(top[keys[0]])==types.DictType:
            return NestedDict(top[keys[0]])
        else:
            return top[keys[0]]


    def __setitem__(self, key, item):
        keys=key.split(self.seperator)
        top=self.data

        while len(keys)>1:
            if not top.has_key(keys[0]):
                top[keys[0]]={}
            top=top[keys[0]]
            keys=keys[1:]

        top[keys[0]]=item
    

    def __delitem__(self, key):
        top=self.data

        path=key.split(self.seperator)
        (path, leaf)=(path[:-1], path[-1])

        try:
            for subkey in path:
                top=top[subkey]
        except KeyError:
            raise KeyError, key

        del top[leaf]


    def has_key(self, key):
        top=self.data

        try:
            for subkey in key.split(self.seperator):
                top=top[subkey]
        except KeyError:
            return False

        return True

