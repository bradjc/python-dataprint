from dataprint import dataprint

a = [['Name', 'Age', 'Color'],
     ['Brad', 24, 'blue'],
     ['Jeff', 20, 'yellow']]

print dataprint.to_string(a)
dataprint.to_newfile("test.file", a)

fd = open("exist.file", "w")
fd.write("add some content\n")
dataprint.to_file(fd, a)
fd.close()

print dataprint.to_string(a, tabwidth=4)

b = [['Name', 'Age', 'Color'],
     ['Brad', 24, 'blue'],
     ['Jeff', 20, 'yellow'],
     ['ReallyLong Name', 100, 'aafdlksjfkld']]

dataprint.to_newfile("notab.file", b)
dataprint.to_newfile("tab.file", b, tabwidth=4)
dataprint.to_newfile("tab1space.file", b, tabwidth=4, min_padding=1)
dataprint.to_newfile("tab5.file", b, tabwidth=5, min_padding=1)
dataprint.to_newfile("space_nogap.file", b, min_padding=0)
