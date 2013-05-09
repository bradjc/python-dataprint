from dataprint import dataprint

data = [['Color', 'Length'],
        ['blue', 4],
        ['red', 3],
        ['orange yellow', 13]]

print dataprint.to_string(data, min_padding=4, separator='-')
