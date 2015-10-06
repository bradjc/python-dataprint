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

    import dataprint
    dataprint.to_file("xyz.dat", data)

to get:

    # x   y    z
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



Examples
--------

### Example 1

Basic usage.

```python
import dataprint

data = [['Color', 'Length'],
        ['blue', 4],
        ['red', 3]]

print dataprint.to_string(data)
```

Will print:

    # Color  Length
    blue     4
    red      3



### Example 2

Change the settings.

```python
import dataprint

data = [['Color', 'Length'],
        ['blue', 4],
        ['red', 3],
        ['orange yellow', 13]]

print dataprint.to_string(data, min_padding=4, separator='-')
```

    # Color          Length
    blue             4
    red              3
    orange-yellow    13


### Example 3

Output to a file.

```python
import dataprint

data = [['Color', 'Length'],
        ['blue', 4],
        ['red', 3]]

dataprint.to_newfile(filename='example3.dat', data=data)
```

Will create `example3.dat` containing:

    # Color  Length
    blue     4
    red      3


### Example 4

You may want to put the formatted data into an already opened file.

```python
import dataprint

data = [['Color', 'Length'],
        ['blue', 4],
        ['red', 3]]

fd = open('example4.dat', 'w')

fd.write('# This data file is for example 4.\n\n')

dataprint.to_file(open_file=fd, data=data)
```

This will create `example4.dat` containing:

    # This data file is for example 4.

    # Color  Length
    blue     4
    red      3


### Example 5

Your data may be in columns instead of rows. To use this data, set `columns` to
`TRUE`.

```python
import dataprint

x = [1, 2, 3]
y = [10, 20, 30]

print dataprint.to_string(data=[x, y], columns=True)
```
Output:

    1  10
    2  20
    3  30


### Example 6

You may want to add extra notes to your data file, or have complicated data
that requires some extra explanation.

```python
import dataprint
import time

data = [['blue', 4],
        ['red', 3]]

print dataprint.to_string(data, comments='Generated at {}'.format(time.asctime()))
```

Will print:

    # Generated at Tue Oct  6 12:15:45 2015
    blue   4
    red    3


Changelog
---------

### Version 1.0
No longer a package (just use `import dataprint`).
Python 3 support.

### Version 0.3
Added support for column based data.

### Version 0.2
Added many tests, more error checking, and a separator replacement for spaces.

### Version 0.1
Initial release. Supports data layouts of lists of lists, separates with tabs
or spaces, and can write to a string or file.

To Do
-----

  - Document the thing
  - Lot more testing with different data inputs


