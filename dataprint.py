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

import io
import os
import sys

PY3 = sys.version > '3'

def to_string (data, tabwidth=0, min_padding=2, separator='_', columns=False):
	"""
	Return the data pretty printed as a string.
	"""
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      columns=columns)
	return printer.string_output(data)

def to_newfile (filename, data, tabwidth=0, min_padding=2, separator='_',
                overwrite=False, columns=False):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      overwrite=overwrite,
	                      columns=columns)
	printer.new_file_output(filename=filename, data=data)

def to_file (open_file, data, tabwidth=0, min_padding=2, separator='_',
             columns=False):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      columns=columns)
	printer.append_file_output(fd=open_file, data=data)



MISSING_STRING = "MISSING"


class DataPrinter(object):
	def __init__ (self, tabwidth=0, min_padding=2, separator='_',
	              overwrite=False, columns=False):
		self._tabwidth  = int(tabwidth)
		self._padding   = int(min_padding)
		self._separator = str(separator)
		self._overwrite = bool(overwrite)
		self._columns   = bool(columns)

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
		if type(fd) == io.TextIOWrapper:
			if fd.closed or not fd.writable():
				raise DataPrinterException("Cannot write to file.")
			self.format(data, fd)
		else:
			if PY3 or (type(fd) is not file):
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

		if type(data) == str:
			raise DataPrinterException("Data is not a valid format.")

		if self._columns:
			# Data is formated such that each list in data contains all the
			# values for a column of data
			num_cols = len(data)
			num_rows = [max(len(x) for x in data)][0]
		else:
			num_cols = [max(len(x) for x in data)][0]
			num_rows = len(data)

		# Assume we have a list of lists
		max_lens = [0] * num_cols

		# Get the maximum len of each column
		for i, array in zip(range(len(data)), data):
			for j, item in zip(range(len(array)), array):
				# Determine the len of the data item after separators are used
				item_str = self._separator.join(str(item).split())

				column_index = i if self._columns else j

				if len(item_str) > max_lens[column_index]:
					max_lens[column_index] = len(item_str)

		# Update the max lens if we have column data.
		# Need to compensate if one column is longer than another.
		if self._columns:
			for i in range(num_cols):
				if len(data[i]) < num_rows:
					if len(MISSING_STRING) > max_lens[i]:
						max_lens[i] = len(MISSING_STRING)

		# Iterate and write the output data
		if self._columns:
			# Iterate over the length the longest column
			for row_idx in range(num_rows):
				for col_idx in range(num_cols):
					if row_idx < len(data[col_idx]):
						istr = self._separator.join(
							str(data[col_idx][row_idx]).split())
					else:
						istr = MISSING_STRING

					pad = (col_idx != num_cols - 1)

					self.write_to_output(outfile, istr, pad, max_lens[col_idx])

		else:
			for row_idx, row in zip(range(len(data)), data):
				for col_idx, item in zip(range(len(row)), row):
					istr = self._separator.join(str(item).split())

					pad = (col_idx != len(row) - 1)

					self.write_to_output(outfile, istr, pad, max_lens[col_idx])


	def write_to_output (self, outfile, item, padding, max_len):
		if not padding:
			# Don't add padding to the end of the last column
			outfile.write(u"{0}\n".format(item))
			return

		if self._tabwidth == 0:
			# use spaces
			outfile.write(u"{1:<{0}s}".format(max_len+ self._padding, item));
		else:
			max_line = max_len + self._padding
			max_line_tabs = ((max_line - 1) // self._tabwidth) + 1
			tabs = max_line_tabs - (len(str(item)) // self._tabwidth)
			outfile.write(u"{1:\t<{0}s}".format(tabs + len(item), item));


class StringFile(object):
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
