import dataprint
import copy

x = [4.5, 3]
y = [10, 6.99]
z = [1, 2, 3]
w = [100, 4500, 7]

a = "4.5  10\n3    6.99\n"
b = "4.5      10       1\n3        6.99     2\nMISSING  MISSING  3\n"
c = "100   1\n4500  2\n7     3\n"

def test_xy ():
	temp = dataprint.to_string([x, y], columns=True)
	assert temp == a

def test_xyz ():
	temp = dataprint.to_string([x, y, z], columns=True)
	assert temp == b

def test_wz ():
	temp = dataprint.to_string([w, z], columns=True)
	assert temp == c


