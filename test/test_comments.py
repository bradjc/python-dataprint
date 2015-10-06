import dataprint
import copy

data = [['Name', 'Age', 'Color'],
        ['Brad', 24, 'blue'],
        ['Jeff', 20, 'yellow']]

a_comments = "This is a comment"
a_default = "# This is a comment\n# Name  Age  Color\nBrad    24   blue\nJeff    20   yellow\n"
a_symbol  = "%This is a comment\n%Name  Age  Color\nBrad   24   blue\nJeff   20   yellow\n"
a_none    = "This is a comment\nName  Age  Color\nBrad  24   blue\nJeff  20   yellow\n"

b_comments = ["This comment 1", "And comment 2"]
b_default = "# This comment 1\n# And comment 2\n# Name  Age  Color\nBrad    24   blue\nJeff    20   yellow\n"
b_symbol  = "%This comment 1\n%And comment 2\n%Name  Age  Color\nBrad   24   blue\nJeff   20   yellow\n"


def test_single_comment ():
	temp = dataprint.to_string(data, comments=a_comments)
	assert temp == a_default

def test_multiple_comments ():
	temp = dataprint.to_string(data, comments=b_comments)
	assert temp == b_default

def test_comment_character_single ():
	temp = dataprint.to_string(data, comments=a_comments, comment_lead='%')
	assert temp == a_symbol

def test_comment_character_multiple ():
	temp = dataprint.to_string(data, comments=b_comments, comment_lead='%')
	assert temp == b_symbol

def test_no_comment_character ():
	temp = dataprint.to_string(data, comments=a_comments, comment_lead=None)
	assert temp == a_none

