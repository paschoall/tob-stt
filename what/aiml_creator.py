import sys

def create_category(pattern, template):
	str = ""
	str += "\t<category>\n"
	str += "\t\t<pattern>"+ pattern +"</pattern>\n"
	str += "\t\t<template>"+ template +"</template>\n"
	str += "\t</category>\n"
	return str

result = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n"
question = ""
for line in sys.stdin:
	if line[0] == '\n': continue
	line = line.replace("\n", "");
	if line[0] == '-': # question
		if question != "":
			sys.exit("Something is wrong with your format")
		question = line[1:]
	elif line[0] == '>': # answer
		if question == "":
			sys.exit("Something is wrong with your format")
		answer = line[1:]
		result += create_category(question, answer)
		question = ""

result += "</aiml>"
print(result)