# Author: Brad Campbell
#         bradjc@umich.edu
#
# Print data that is stored in lists and tuples to a file in a nice way.
#

def dprint_string (data):
	printer = DataPrinter()
	return printer.output(data)

class DataPrinter:
	def __init__ (self):
		pass

	def output (self, data):
		out = ""
		padding_size = 2

		# assume we have a list of lists
		max_lens = [0] * len(data[0])

		# get the maximum len of each column
		for row in data:
			for i, col in zip(range(len(row)), row):
				if len(str(col)) > max_lens[i]:
					max_lens[i] = len(str(col))

		for row in data:
			for i, col in zip(range(len(row)), row):
				if i < len(row) - 1:
					out += "{1:<{0}s}".format(max_lens[i]+padding_size, col)
				else:
					# Don't add padding to the end of the last column
					out += "{0}".format(col)

			out += "\n"

		return out
