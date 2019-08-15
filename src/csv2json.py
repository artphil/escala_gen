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
db = []
titles = lines[0]
for line in lines[1:]:
	dictionary[line[0]] = {}
	item = {}
	for i in range(len(titles)):
		if titles[i] == "name" or titles[i] == "alias":
			dictionary[line[0]][titles[i]] = capita(line[i])
			item[titles[i]] = capita(line[i])
		elif titles[i] == "trecho" or titles[i] == "code":
			dictionary[line[0]][titles[i]] = line[i]
			item[titles[i]] = line[i]
		else:
			dictionary[line[0]][titles[i]] = line[i]
			if line[i]:
				item[titles[i]] = int(line[i])
		
	db.append(item)	

json_file = open(sys.argv[1][:-3]+'json', 'w') 
json_file.write(json.dumps(dictionary, sort_keys=True, indent=4))

db_file = open(sys.argv[1][:-4]+'_db.json', 'w')
# db_file.write(json.dumps(db))
for item in db:
	db_file.write(json.dumps(item))
	db_file.write("\n")

csv_file.close()
db_file.close()
json_file.close()

print(json.dumps(db, sort_keys=True, indent=4))

