import sys

for line in sys.stdin:
	if(line[-1] == '\n'): line = line[:-1]
	while(line[-1] == '\t'): line = line[:-1]
	strings = line.split('\t')
	pattern = strings[0]
	print("-" + pattern)
	strings = strings[1:]
	if len(strings) == 1:
		print(">" + strings[0])
	else: 
		t = "><random>"
		for x in strings:
			t += "<li>" + x + "</li>"
		t += "</random>"
		print(t)
	print()