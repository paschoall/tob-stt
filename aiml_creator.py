import sys

def create_category(pattern, that, template):
	patterns = []
	# create all configurations of pattern
	cnt = 0
	for c in pattern:
		cnt += 1 if c == '^' else 0

	for i in range(1 << cnt):
		s = ""
		ind = 0
		for c in pattern:
			if c == '^':
				if ((i >> ind)&1) == 1:
					s += '*'
				ind += 1
			else: s += c

		s2 = ""
		last = ' '
		for c in s:
			if c != ' ' or c != last:
				s2 += c
			last = c
		while s2[-1] == ' ': s2 = s2[:-1]
		patterns.append(s2);

	str = ""
	for pat in patterns:
		str += "\t<category>\n"
		str += "\t\t<pattern>"+ pat +"</pattern>\n"
		if that != "": str += "\t\t<that>"+ that +"</that>\n"
		str += "\t\t<template>"+ template +"</template>\n"
		str += "\t</category>\n"
	return str

result = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n"
question = ""
that = ""
for line in sys.stdin:
	if line[0] == '\n': continue
	line = line.replace("\n", "");
	if line[0] == '-': # question
		if question != "":
			sys.exit("Something is wrong with your format")
		question = line[1:]
	if line[0] == '@': # question
		if that != "":
			sys.exit("Something is wrong with your format")
		that = line[1:]
	elif line[0] == '>': # answer
		if question == "":
			sys.exit("Something is wrong with your format")
		answer = line[1:]
		result += create_category(question, that, answer)
		question = ""
		that = ""

result += "</aiml>"
print(result)