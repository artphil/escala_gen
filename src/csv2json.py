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
for line in lines:
	dictionary[line[0]] = {}
	dictionary[line[0]]['nome'] = capita(line[1])
	dictionary[line[0]]['alias'] = capita(line[2])
	dictionary[line[0]]['p'] = '1'

json_file = open(sys.argv[1][:-3]+'json', 'w') 
json_file.write(json.dumps(dictionary, sort_keys=True, indent=4))

csv_file.close()
json_file.close()

print(json.dumps(dictionary, sort_keys=True, indent=4))

