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

import itertools
import io
import os
import sys

PY3 = sys.version > '3'

def to_string (data,
               tabwidth=0, min_padding=2, separator='_', columns=False,
               comments=None, comment_lead='# '):
	"""
	Return the data pretty printed as a string.
	"""
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      columns=columns,
	                      comments=comments,
	                      comment_lead=comment_lead,
	                      )
	return printer.string_output(data)

def to_newfile (filename, data,
                tabwidth=0, min_padding=2, separator='_', columns=False,
                overwrite=False,
                comments=None, comment_lead='# '):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      overwrite=overwrite,
	                      columns=columns,
	                      comments=comments,
	                      comment_lead=comment_lead,
	                      )
	printer.new_file_output(filename=filename, data=data)

def to_file (open_file, data,
             tabwidth=0, min_padding=2, separator='_', columns=False,
             comments=None, comment_lead='# '):
	printer = DataPrinter(tabwidth=tabwidth,
	                      min_padding=min_padding,
	                      separator=separator,
	                      columns=columns,
	                      comments=comments,
	                      comment_lead=comment_lead,
	                      )
	printer.append_file_output(fd=open_file, data=data)



MISSING_STRING = "MISSING"


class DataPrinter(object):
	def __init__ (self, tabwidth=0, min_padding=2, separator='_',
	              overwrite=False, columns=False,
	              comments=None, comment_lead='# '):
		self._tabwidth     = int(tabwidth)
		self._padding      = int(min_padding)
		self._separator    = str(separator)
		self._overwrite    = bool(overwrite)
		self._columns      = bool(columns)
		self._comments     = comments
		self._comment_lead = str(comment_lead) if comment_lead else ''

		if isinstance(self._comments, str):
			self._comments = [self._comments, ]

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

		# Write any comments out first
		if self._comments:
			for comment in self._comments:
				outfile.write('{}{}\n'.format(self._comment_lead, comment))

		# If columnar, invert the data
		if self._columns:
			if PY3:
				data = list(itertools.zip_longest(*data, fillvalue=MISSING_STRING))
			else:
				data = list(itertools.izip_longest(*data, fillvalue=MISSING_STRING))

		num_cols = [max(len(x) for x in data)][0]
		num_rows = len(data)

		# Assume we have a list of lists
		max_lens = [0] * num_cols

		# Check if the data is mixed string and numbers, if so, assume the
		# strings at the beginning are actually headers and comment them as
		# appropriate
		def has_any_numeric(row):
			for r in row:
				try:
					float(r)
					break
				except ValueError:
					pass
			else:
				return False
			return True

		number_of_leading_comments = 0
		if self._comment_lead:
			if len(data) > 1:
				if has_any_numeric(data[-1]):
					i = 0
					while not has_any_numeric(data[i]):
						i += 1
					number_of_leading_comments = i

		# Get the maximum len of each column
		for i, array in zip(range(len(data)), data):
			for j, item in zip(range(len(array)), array):
				# Determine the len of the data item after separators are used
				if i < number_of_leading_comments:
					if j == 0:
						item_str = '{}{}'.format(self._comment_lead, item)
					else:
						item_str = item
				else:
					item_str = self._separator.join(str(item).split())

				column_index = j

				if len(item_str) > max_lens[column_index]:
					max_lens[column_index] = len(item_str)

		for row_idx, row in zip(range(len(data)), data):
			for col_idx, item in zip(range(len(row)), row):
				if row_idx < number_of_leading_comments:
					if col_idx == 0:
						istr = '{}{}'.format(self._comment_lead, item)
					else:
						istr = item
				else:
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
