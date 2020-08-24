import sys

def reduction(original, target):
	str = ""

	# palavra sozinha
	str += "<category>\n"
	str += "\t<pattern>" + original + "</pattern>\n"
	str += "\t<template><srai>" + target + "</srai></template>\n"
	str += "</category>\n"

	# palavra com * na frente
	str += "<category>\n"
	str += "\t<pattern>" + original + " *</pattern>\n"
	str += "\t<template><srai>" + target + " <star/></srai></template>\n"
	str += "</category>\n"

	# palavra com * antes
	str += "<category>\n"
	str += "\t<pattern>* " + original + "</pattern>\n"
	str += "\t<template><srai><star/> " + target + "</srai></template>\n"
	str += "</category>\n"

	# palavra com * antes e depois
	str += "<category>\n"
	str += "\t<pattern>* " + original + " *</pattern>\n"
	str += "\t<template><srai><star/> " + target + " <star index='2' /></srai></template>\n"
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