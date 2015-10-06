import dataprint
import copy

a = [['Name', 'Age', 'Color'],
	 ['Brad', 24, 'blue'],
	 ['Jeff', 20, 'yellow']]
a_default = "# Name  Age  Color\nBrad    24   blue\nJeff    20   yellow\n"

b = (('Year', 'Temp'),
	 (2000, 76.4329087834),
	 (5000, 8732.432432))
b_default = "# Year  Temp\n2000    76.4329087834\n5000    8732.432432\n"

c = [('A', 'B'),
	 ("longer string", "and this")]
c_def = "A              B\nlonger_string  and_this\n"

d = [['a', 'b', 'c'], [1, 2, 3]]
d_def = "# a  b  c\n1    2  3\n"

e = [['a', 'b', 'c'], [1, 2, 3]]
e_def = "a  b  c\n1  2  3\n"

def test_arrays ():
	temp = dataprint.to_string(a)
	assert temp == a_default

def test_tuples ():
	temp = dataprint.to_string(b)
	assert temp == b_default

def test_longer ():
	temp = dataprint.to_string(c)
	assert temp == c_def

def test_const ():
	c_copy = copy.deepcopy(c)
	temp = dataprint.to_string(c)
	assert c == c_copy

def test_simple ():
	temp = dataprint.to_string(d)
	assert temp == d_def

def test_no_comments ():
	temp = dataprint.to_string(e, comment_lead=None)
	assert temp == e_def
