#testing
#!/bin/python

import requests
import pandas
import bs4

database = pandas.read_csv('db.csv')
url = 'http://cloudportal.sathyabama.ac.in/cae/login.php'
regnos = []
names = []
sect = []
dmaw = []
ooad = []
da = []
cc = []
py = []
ns = []

for i in range(0, len(database)):
	info = {'regno' : str(database.iloc[i]['regno']), 'dob' : str(database.iloc[i]['dob'])}
	print('[Info]\tRipping \x1b[32m' + str(info.get('regno')) + '\x1b[0m...',end='')
	
	sess = requests.session()
	data = sess.post(url, data=info)
	
	bs = bs4.BeautifulSoup(data.content,features="html5lib")
	table_data = bs.findAll('td')
	if(len(table_data) > 33):
		regnos.append(table_data[0].text[-7:])
		names.append(table_data[1].text)
		sect.append(table_data[3].text[-3:].replace('[','').replace(']',''))
		dmaw.append(table_data[8].text)
		ooad.append(table_data[13].text)
		da.append(table_data[18].text)
		cc.append(table_data[23].text)
		py.append(table_data[28].text)
		ns.append(table_data[33].text)
		del(info)
		del(sess)
		del(bs)
		del(table_data)
		print('\x1b[32mDone!\x1b[0m')
	else:
		print('\x1b[31mData error!\x1b[0m')

print('Creating Dataframe...', end='')
dataframe = pandas.DataFrame({'Register Numbers' : regnos,
'Name' : names,
'Section' : sect,
'Data Mining & Data Warehousing' : dmaw,
'Object Oriented Analysis and Design' : ooad,
'Data analytics' : da,
'Cloud Computing' : cc,
'Python Programming' : py,
'Network Security' : ns})

dataframe.to_csv('out.csv')
print('Done!')