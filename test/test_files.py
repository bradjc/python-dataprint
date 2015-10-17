import dataprint
import io

a = [['Name', 'Age', 'Color'],
	 ['Brad', 24, 'blue'],
	 ['Jeff', 20, 'yellow']]
a_default = "# Name  Age  Color\nBrad    24   blue\nJeff    20   yellow\n"

def test_existing (tmpdir):
	fd = open(str(tmpdir) + "/exist.file", "w")
	dataprint.to_file(fd, a)
	fd.close()
	fd = open(str(tmpdir) + "/exist.file", "r")
	temp = fd.read()
	fd.close()
	assert temp == a_default

def test_new (tmpdir):
	dataprint.to_newfile(str(tmpdir) + "/new.file", a)
	fd = open(str(tmpdir) + "/new.file", "r")
	temp = fd.read()
	fd.close()
	assert temp == a_default

def test_io_existing (tmpdir):
	fd = io.open(str(tmpdir) + "/exist.file", "w")
	dataprint.to_file(fd, a)
	fd.close()
	fd = open(str(tmpdir) + "/exist.file", "r")
	temp = fd.read()
	fd.close()
	assert temp == a_default
