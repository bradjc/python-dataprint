from dataprint import dataprint

a = [['Name', 'Age', 'Color'],
     ['Brad', 24, 'blue'],
     ['Jeff', 20, 'yellow']]

print dataprint.to_string(a)
dataprint.to_newfile("test.file", a)
