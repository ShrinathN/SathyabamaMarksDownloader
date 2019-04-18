#!/bin/python

#importing and stuff
import requests
import pandas
import bs4

#constants
base_url = 'http://cloudportal.sathyabama.ac.in/cae/login.php'
cae1_url = 'http://cloudportal.sathyabama.ac.in/cae/cae.php?cae=1'
cae2_url = 'http://cloudportal.sathyabama.ac.in/cae/cae.php?cae=2'

#formatting constants
COLOR_RED = '\x1b[31m'
COLOR_NORMAL = '\x1b[0m'
COLOR_GREEN = '\x1b[32m'
COLOR_INFO = '\x1b[32;41m'

#subject names
subjects_name_set = False
sub0_name = ""
sub1_name = ""
sub2_name = ""
sub3_name = ""
sub4_name = ""
sub5_name = ""

#lists for storing details
regnos1 = []
regnos2 = []
names1 = []
names2 = []
sub0_1 = []
sub1_1 = []
sub2_1 = []
sub3_1 = []
sub4_1 = []
sub5_1 = []
sub0_2 = []
sub1_2 = []
sub2_2 = []
sub3_2 = []
sub4_2 = []
sub5_2 = []

#data from the database
database = pandas.read_csv('db.csv')

for i in range(0, len(database)):
	info = {'regno' : str(database.iloc[i]['regno']), 'dob' : str(database.iloc[i]['dob'])}
	print(COLOR_INFO + '[Info]' + COLOR_NORMAL + '\tScrapping ' + COLOR_GREEN + str(info.get('regno')) + COLOR_NORMAL)
	
	##logging in
	#creating session
	sess = requests.session()
	#sending login info
	sess.post(base_url, data=info)
	
	#getting marks for CAE1
	data = sess.get(cae1_url)
	bs = bs4.BeautifulSoup(data.content,features="html5lib")
	table_data = bs.findAll('td')
	if(len(table_data) > 33):
		if(not subjects_name_set):
			sub0_name = table_data[7].text
			sub1_name = table_data[12].text
			sub2_name = table_data[17].text
			sub3_name = table_data[22].text
			sub4_name = table_data[27].text
			sub5_name = table_data[32].text
			subjects_name_set = True
		regnos1.append(table_data[0].text.replace('Register Number: ', ''))
		names1.append(table_data[1].text.replace('Student Name: ', ''))
		sub0_1.append(table_data[8].text)
		sub1_1.append(table_data[13].text)
		sub2_1.append(table_data[18].text)
		sub3_1.append(table_data[23].text)
		sub4_1.append(table_data[28].text)
		sub5_1.append(table_data[33].text)
		print('\t' + COLOR_GREEN + '[OK]' + COLOR_NORMAL + ' Midsem-1')
		#repeating the same process for CAE 2
		data = sess.get(cae2_url)
		bs = bs4.BeautifulSoup(data.content,features="html5lib")
		table_data = bs.findAll('td')
		if(len(table_data) > 33):
			regnos2.append(table_data[0].text.replace('Register Number: ', ''))
			names2.append(table_data[1].text.replace('Student Name: ', ''))
			sub0_2.append(table_data[8].text)
			sub1_2.append(table_data[13].text)
			sub2_2.append(table_data[18].text)
			sub3_2.append(table_data[23].text)
			sub4_2.append(table_data[28].text)
			sub5_2.append(table_data[33].text)
			print('\t' + COLOR_GREEN + '[OK]' + COLOR_NORMAL + ' Midsem-2')
		else:
			#continue because the CAE2 might not have taken place yet
			print('\t' + COLOR_RED + '[ER]' + COLOR_NORMAL + ' Midsem-2')
			continue
	else:
		print('\t' + COLOR_RED + '[ER]' + COLOR_NORMAL + ' Midsem-1')
	#deleting objects because i do not trust the garbage collector
	del(info)
	del(sess)
	del(bs)
	del(table_data)

print('Creating Dataframe...', end='')

dataframe1 = pandas.DataFrame({'Register Numbers' : regnos1,
'Name' : names1,
sub0_name : sub0_1,
sub1_name : sub1_1,
sub2_name : sub2_1,
sub3_name : sub3_1,
sub4_name : sub4_1,
sub5_name : sub5_1})
dataframe1.to_csv('midsem-1.csv')

try:
	dataframe2 = pandas.DataFrame({'Register Numbers' : regnos2,
	'Name' : names2,
	sub0_name : sub0_2,
	sub1_name : sub1_2,
	sub2_name : sub2_2,
	sub3_name : sub3_2,
	sub4_name : sub4_2,
	sub5_name : sub5_2})
	dataframe2.to_csv('midsem-2.csv')
except:
	print('Error OwO')
	