# Author: Brad Campbell
#         bradjc@umich.edu
#
# Print data that is stored in lists and tuples to a file in a nice way.
#


#
# tabwidth:    if 0, use spaces. if > 0, sets the width of the tab to be used
#              for column aligning
# min_padding: number of spaces to put between columns
# separator:   character to replace whitespace in the data. This is to prevent
#              the same character that is used to separate columns from being in
#              the column itself.
#

import os

"""
Return the data pretty printed as a string.
"""
def to_string (data, tabwidth=0, min_padding=2, separator='_'):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator)
	return printer.string_output(data)

def to_newfile (filename, data, tabwidth=0, min_padding=2, separator='_',
                overwrite=False):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      overwrite=overwrite)
	printer.new_file_output(filename=filename, data=data)

def to_file (open_file, data, tabwidth=0, min_padding=2, separator='_'):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator)
	printer.append_file_output(fd=open_file, data=data)


class DataPrinter:
	def __init__ (self, tabwidth=0, min_padding=2, separator='_',
	              overwrite=False):
		self._tabwidth  = int(tabwidth)
		self._padding   = int(min_padding)
		self._separator = str(separator)
		self._overwrite = bool(overwrite)

		if self._tabwidth < 0 or self._padding < 0:
			raise DataPrinterException("Invalid padding or tabwidth.")

	def string_output (self, data):
		fstring = StringFile()
		self.format(data, fstring)
		return fstring.get()

	def new_file_output (self, filename, data):
		if not self._overwrite:
			# Check if file exists already
			try:
				with open(filename):
					raise DataPrinterException("File exists. Set 'overwrite' \
to True in order to overwrite the file.")
			except IOError:
				pass
		try:
			f = open(filename, 'w')
		except IOError:
			raise DataPrinterException("Cannot open file: {0}".format(filename))

		self.format(data, f)
		f.close()

	def append_file_output (self, fd, data):
		if type(fd) is not file:
			raise DataPrinterException("Provided file descriptor was not valid.")
		if 'w' not in fd.mode:
			raise DataPrinterException("Cannot write to file.")
		self.format(data, fd)

	def format (self, data, outfile):
		out = ""

		try:
			data.__iter__
		except AttributeError:
			raise DataPrinterException("Data is not a valid format.")

		num_columns = [max(len(str(x)) for x in line) for line in zip(*data)][0]

		# assume we have a list of lists
		max_lens = [0] * num_columns

		# get the maximum len of each column
		for row in data:
			for i, col in zip(range(len(row)), row):
				col_str = str(col)
				# Determine the len of the data item after separators are used
				col_str = self._separator.join(str(col).split())

				if len(col_str) > max_lens[i]:
					max_lens[i] = len(col_str)

		for row in data:
			for i, col in zip(range(len(row)), row):
				col_str = self._separator.join(str(col).split())

				if i == len(row) - 1:
					# Don't add padding to the end of the last column
					outfile.write("{0}\n".format(col_str))
					continue

				if self._tabwidth == 0:
					# use spaces
					outfile.write("{1:<{0}s}".format(max_lens[i]+ self._padding,
					                                 col_str));
				else:
					max_line = max_lens[i] + self._padding
					max_line_tabs = ((max_line - 1) // self._tabwidth) + 1
					tabs = max_line_tabs - (len(str(col)) // self._tabwidth)
					outfile.write("{1:\t<{0}s}".format(tabs + len(col_str),
					                                   col_str));


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
