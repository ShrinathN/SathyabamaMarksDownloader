#!/bin/python
#ripper for May 2019 exams
import requests
import random
import pandas
import re
import bs4

#constants
results_url = 'http://www.sathyabama.ac.in/result.php'
submit_url = 'http://www.sathyabama.ac.in/searchSamplestudent.php'

database = pandas.read_csv('db.csv')


name_list = []
marks_string_list = []

for i in range(0, len(database)):
	try:
		output_file = open('output_may2019.txt','a')
		
		info = {'Regnum' : str(database.iloc[i]['regno']), 'stu_dob' : str(database.iloc[i]['dob'])}
		print('Sending request for ',str(database.iloc[i]['regno']))
		sess = requests.session()
		data = sess.get(results_url)
		print('Got response!')

		bs = bs4.BeautifulSoup(data.text,features="html5lib")
		magic_num = re.sub('[^0-9]','',str(bs.findAll(attrs={'class' : 'sub-btn'})[0]))
		info.update({'rnum' : str(database.iloc[i]['regno']) + '.' + str(magic_num) + str(random.random())})
		
		print('Sending spoofed request')
		data = sess.post(submit_url, data=info)
		bs = bs4.BeautifulSoup(data.text,features="html5lib")
		print('Got result!\n')
		
		data_text = bs.findAll(attrs={'class' : 'result-content2'})
		name_list.append(re.sub(' NAME : ', '', data_text[2].text))
		print(re.sub(' NAME : ', '', data_text[2].text))
		output_file.write(re.sub(' NAME : ', '', data_text[2].text) + '\n')
	
		temp_str = ''
		for x in range(12, len(data_text)-1, 6):
			temp_str = temp_str + str(data_text[x + 1].text) + '->' + str(data_text[x + 4].text) + '\n'
		print(temp_str)
		marks_string_list.append(temp_str)
		output_file.write(temp_str + '\n')
		output_file.close()
	except:
		print('Error')
		continue