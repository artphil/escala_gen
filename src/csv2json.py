import sys
import json

def capita(txt):
	txt_list = txt.split(' ')
	txt_capita = ''
	for word in txt_list:
		txt_capita += word.capitalize()
		txt_capita += ' '
	
	return txt_capita[:-1]


if len(sys.argv) < 2:
	print('No arguments')
	quit()

csv_file = open(sys.argv[1], 'r') 
if not csv_file: 
	print('invalid argument')
	quit()

lines = []
for line in csv_file.readlines():
	lines.append(line[:-1].split(';'))

dictionary = {}
titles = lines[0]
for line in lines[1:]:
	dictionary[line[0]] = {}
	for i in range(len(titles)):
		if titles[i] == "name" or titles[i] == "alias":
			dictionary[line[0]][titles[i]] = capita(line[i])
		else:
			dictionary[line[0]][titles[i]] = line[i]

json_file = open(sys.argv[1][:-3]+'json', 'w') 
json_file.write(json.dumps(dictionary, sort_keys=True, indent=4))

csv_file.close()
json_file.close()

print(json.dumps(dictionary, sort_keys=True, indent=4))

