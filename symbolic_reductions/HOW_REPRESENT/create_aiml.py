import sys

def reduction(original, target):
	str = ""
	
	cnt = 0
	for c in original:
		cnt +=  1 if c == '*' else 0
	str += "<category>\n"
	str += "\t<pattern>" + original + "</pattern>\n"
	str += "\t<template><srai>" + target + " <star index='" + chr(ord('0') + cnt) + "'/></srai></template>\n"
	str += "</category>\n"
	return str

first = 0
intent = ""
result = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n"

reductions = []
for line in sys.stdin:
	line = line.replace("\n", "")
	if first == 0:
		first = 1
		intent = line
	else:
		reductions.append(reduction(line, intent))

for str in reductions:
	result += "\t" + str.replace("\n", "\n\t")
	result = result[:-1]

result += "</aiml>"
print(result)