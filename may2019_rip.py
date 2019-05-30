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

for i in range(0, len(database)):
	info = {'Regnum' : str(database.iloc[i]['regno']), 'stu_dob' : str(database.iloc[i]['dob'])}
	
	sess = requests.session()
	data = sess.get(results_url)
	
	bs = bs4.BeautifulSoup(data.text,features="html5lib")
	magic_num = re.sub('[^0-9]','',str(bs.findAll(attrs={'class' : 'sub-btn'})[0]))
	info.update({'rnum' : str(database.iloc[i]['regno']) + '.' + str(magic_num) + str(random.random())})
	
	data = sess.post(submit_url, data=info)
	f = open('wewlad', 'w')
	f.write(str(data.text))
	f.close()
	
	exit()