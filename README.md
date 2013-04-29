python-dataprint
================

Python module to print data to a file in a nice way. Usually data processing
scripts write data to a file, but it is a hassle to format it nicely each
time. So data files end up looking like:

    x y z
    50 678 9
    5643 908 44
    321 2 2

which I find very hard to read. This module lets you take

    data = [
     ['x', 'y', 'z'],
     [50, 678, 9],
     [5643, 908, 44],
     [321, 2, 2]
    ]

then do:

    from dataprint import dataprint
    dataprint.to_file("xyz.dat", data)

to get:

	x     y    z
    50    678  9
    5643  908  44
    321   2    2

Much better.


Install
-------

    sudo pip install dataprint

OR

    git clone https://github.com/bradjc/python-dataprint.git
    cd python-dataprint
    sudo python setup.py install

Usage
-----

Dataprint provides three easy functions to use:

    to_string (data, tabwidth=0, min_padding=2, separator='_')
    to_newfile (filename, data, tabwidth=0, min_padding=2, separator='_', overwrite=False):
    to_file (open_file, data, tabwidth=0, min_padding=2, separator='_')

The options:

    data:        A 2D array of data that should be formatted
    filename:    string name of a file the data should be put in
    open_file:   a file descriptor the data should be added to
    tabwidth:    if 0, use spaces as the column separators.
                 if >1, use tabs of tabwidth length to separate columns
    min_padding: minimum number of spaces between columns in the output
    separator:   string that will replace whitespace in the column data.
                 This prevents spaces in data from creating more columns.
    overwrite:   whether or not to overwrite a file if it exists


Changelog
---------

### Version 0.2
Added many tests, more error checking, and a separator replacement for spaces.

### Version 0.1
Initial release. Supports data layouts of lists of lists, separates with tabs
or spaces, and can write to a string or file.

To Do
-----

  - Document the thing
  - Lot more testing with different data inputs


