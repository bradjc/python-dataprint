from dataprint import dataprint
import pytest

a = "Simple String"

def test_not_iter ():
	with pytest.raises(dataprint.DataPrinterException):
		b = dataprint.to_string(a)

def test_invalid (tmpdir):
	fd = open(str(tmpdir) + "/exist.file", "w")
	fd.close()
	with pytest.raises(dataprint.DataPrinterException):
		dataprint.to_file(fd, a)

def test_notfile (tmpdir):
	with pytest.raises(dataprint.DataPrinterException):
		dataprint.to_file(3, a)

def test_not_writable (tmpdir):
	fd = open(str(tmpdir) + "/write.file", "w")
	fd.write("test")
	fd.close()
	fd = open(str(tmpdir) + "/write.file", "r")
	with pytest.raises(dataprint.DataPrinterException):
		dataprint.to_file(fd, a)

def test_exists (tmpdir):
	fd = open(str(tmpdir) + "/write.file", "w")
	fd.write("test")
	fd.close()
	with pytest.raises(dataprint.DataPrinterException):
		dataprint.to_file(str(tmpdir) + "/write.file", a)

def test_file_permission_denied (tmpdir):
	with pytest.raises(dataprint.DataPrinterException):
		dataprint.to_newfile("/write.file", a)
