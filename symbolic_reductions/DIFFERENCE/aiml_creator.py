import sys

def category(pattern, template):
	s = "\t<category>\n"
	s += "\t\t<pattern>" + pattern + "</pattern>\n"
	s += "\t\t<template><srai>"
	cnt = 0
	for c in template:
		if c == '*':
			s += "<star index = '" + str(cnt) + "'/>"
			cnt += 1
		else:
			s += c
	s += "</srai></template>\n"
	s += "\t</category>\n"
	return s

template = ""
result = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n"
for line in sys.stdin:
	if line[-1] == '\n': line = line[:-1]
	if template == "":
		template = line
	else:
		result += category(line, template)
result += "</aiml>"
print(result)