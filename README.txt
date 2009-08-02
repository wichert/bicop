Introduction
============

*bicop* is a python library to process ISC bind-style configuration files.
These are nested structures that look like this::

    datasource1 {
        server     "server1.your.domain";
        username   "client";
        password   "secret";
        extra {
            isolation "full";
        };
    };

    tables {
        "users";
        "groups";
    };


Parsing
=======

Parsing is trivial using the ''parse'' method::

   from bicop import parse
   parse("/etc/bind/named.conf")

This returns a standard python dictionary with all data read from the
file. Entries in the dictionary can be other dictionaries or lists.


Merging
=======

A common need is to be able to support default values for configurations
or to handle configuration at multiple levels with priorities, for example
a uer configuration overriding entries from the system-wide configuration.
To support this bicop has a utility method that can merge dictionaries. You
can use it like this::

  from bicop import parse
  from bicop import merge

  configuration=parse("/etc/application.conf")
  userconfig=parse("/home/user/.application")
  merge(configuration, userconfig, overwrite=True)


Easy access for nested dictionaries
===================================

Configuration files in this format can have deeply nested structures. Accessing
those using standard python dictionaries is a slightly cumbersone. To make
this a bit more pleasant on the eyes you can use the NestedDict wrapper::

  from bicop import parse
  from bicop import NestedDict

  configuration=NestedDict(parse("/etc/application.conf"))
  print "Your signature is: %s" % configuration["profiles/user/signature"]


Changes
=======

1.0rc2 - August 2, 20009
------------------------

* Add an optional dictclass parameter to the parse method. This can be
  used to use alternative dictionary types, most typically ordered
  dictionaries.

* Drop dependency on nose to run tests.

* Use ez_setup to automatically install setuptools if needed.

