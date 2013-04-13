# Author: Brad Campbell
#         bradjc@umich.edu
#
# Print data that is stored in lists and tuples to a file in a nice way.
#



"""
Return the data pretty printed as a string.
"""
def to_string (data, tabs=False, tabwidth=0, padding=2):
	printer = DataPrinter(tabs=tabs, tabwidth=tabwidth, padding=padding)
	return printer.string_output(data)

def to_newfile (filename, data, tabs=False, tabwidth=0, padding=2):
	printer = DataPrinter(tabs=tabs, tabwidth=tabwidth, padding=padding)
	printer.new_file_output(filename=filename, data=data)

def to_file (open_file, data, tabs=False, tabwidth=0, padding=2):
	printer = DataPrinter(tabs=tabs, tabwidth=tabwidth, padding=padding)
	printer.append_file_output(fd=open_file, data=data)


class DataPrinter:
	def __init__ (self, tabs=False, tabwidth=0, padding=2):
		self._tabs = tabs
		self._tabwidth = tabwidth
		self._padding = padding

	def string_output (self, data):
		fstring = StringFile()
		self.format(data, fstring)
		return fstring.get()

	def new_file_output (self, filename, data):
		f = open(filename, 'w')
		self.format(data, f)
		f.close()

	def append_file_output (self, fd, data):
		self.format(data, fd)

	def format (self, data, outfile):
		out = ""

		if type(data) is not list:
			raise DataPrinterException("Data is not a valid format.")

		num_columns = [max(len(str(x)) for x in line) for line in zip(*data)][0]

		# assume we have a list of lists
		max_lens = [0] * num_columns

		# get the maximum len of each column
		for row in data:
			for i, col in zip(range(len(row)), row):
				if len(str(col)) > max_lens[i]:
					max_lens[i] = len(str(col))

		for row in data:
			for i, col in zip(range(len(row)), row):
				if i < len(row) - 1:
					outfile.write("{1:<{0}s}".format(max_lens[i]+self._padding,
						                             str(col)));
				else:
					# Don't add padding to the end of the last column
					outfile.write("{0}\n".format(col))




class StringFile:
	def __init__ (self):
		self.internal_str = ""

	def write (self, add_str):
		self.internal_str += add_str

	def get (self):
		return self.internal_str

class DataPrinterException(Exception):
	def __init__ (self, value):
		self.value = value

	def __str__ (self):
		return repr(self.value)
