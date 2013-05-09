from dataprint import dataprint

data = [['Color', 'Length'],
        ['blue', 4],
        ['red', 3]]

fd = open('example4.dat', 'w')

fd.write('# This data file is for example 4.\n\n')

dataprint.to_file(open_file=fd, data=data)
