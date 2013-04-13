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


To Do
-----

  - Document the thing
  - Make all the options work
  - Lot more testing with different data inputs


