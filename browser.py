#!/usr/local/bin/python2
# -*- coding: utf-8 -*-
import re
import mechanize
from bs4 import BeautifulSoup
import calendar
import json
import os
from datetime import datetime, timedelta
import sys

info = []
content = {}
begin = 2015
end = 2015

now = datetime.now()

URL = 'http://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx'
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def Print_Fun(code, date, value):
	filename = 'his/''r-' + str(code) + '.csv'
	f = open (filename, 'a+')
	result = 'epa.aqx.site_code' + '.' + str(code) + '.' + 'pm25' + ',' + str(date) + ',' + value + "\n"
	print result
	f.write(result)
	f.close

""" Get days of every month """

for year in range(begin, end + 1):
	for month in range(3, 13):
		days = calendar.monthrange(year, month)[1]

		for day in range(1, days + 1):
			
			""" it will delay 1~2 days for data update, so will fetch (now - 2) days """
			if datetime(year, month, day) > now - timedelta(days=2):
				print "date upate to", year, month, (day - 1)
				sys.exit(0)
			

			""" Create folder and file for storing data """
			c_path = os.getcwd()
			directory = c_path + '/' +str(year)
			if not os.path.exists(directory):
				print "create directory"
				os.makedirs(directory)
			filename = str(month) + '-' + str(day) + '.json'
			f = open(directory + '/' + filename, 'w+')

			""" Generate data for post form """
			r = br.open(URL)
			br.select_form(nr=0)
			#print br.form

			br['ctl00$cphMain$cboSearch'] = ['主要水庫']
			br['ctl00$cphMain$ucDate$cboYear'] = [str(year)]
			br['ctl00$cphMain$ucDate$cboMonth'] = [str(month)]
			br['ctl00$cphMain$ucDate$cboDay'] = [str(day)]

			br.set_all_readonly(False)
			br['__EVENTTARGET'] = 'ctl00$cphMain$btnQuery'


			#br.find_control("btnQuery").disabled = True

			response = br.submit()
			page =  br.response().get_data() 


			""" Read response """
			soup = BeautifulSoup(page)
			#print soup.prettify()

			print year, month, day

			""" Parse necessary data """
			for element in soup.find(id='frame').tr.next_siblings:
				if element:
					element = str(element).replace(',','')
					element = str(element).replace('--','0')
					element = str(element).replace(' %','')

				m = re.match(r'(<tr>|<tr class="alternate">)\s*<td>(.*)</td><td align="right">(.*)</td><td>\s*.*<br/>\s*.*\s*</td><td align="right">(.*)</td><td align="right">(.*)</td><td align="right">(.*)</td><td align="right">(.*)</td><td>(.*)</td><td>(.*)</td><td align="right">(.*)</td><td align="right">(.*)</td><td align="right">(.*)</td>', str(element), re.M)

				if m:
					#print m.group(2)
					content = {
				"name": m.group(2),
				"capacity": m.group(3),
				"rain": m.group(4),
				"income": m.group(5),
				"outcome": m.group(6),
				"diff": m.group(7),
				"nuclear": m.group(8),
				"now_time": m.group(9),
				"now_level": m.group(10),
				"now_capacity": m.group(11),
				"now_percent": m.group(12)
						}
					info.append(content)
					#f.write(json.dumps(content, ensure_ascii=False))
					#json.dumps(content, f, ensure_ascii=False)
					#json.dump(content, f, ensure_ascii=False)
					#json.dump(content, f, ensure_ascii=False)
					#f.write('\n')

					""" now data"""
					# SiteName,County,PSI,MajorPollutant,Status,SO2,CO,(O3,PM10,PM2.5),NO2,WindSpeed,WindDirec,FPMI,PublishTime
					# 水庫名稱, ,蓄水量百分比(PSI), , , , ,進水量(O3),出水量(PM10),有效蓄水量(PM.25), , , , ,  
					#print m.group(2) + ',,' + m.group(12) + ',,,,,' + m.group(5) + ',' + m.group(6) + ',' + m.group(11) + ',,,,,'
					""" end """
					
					""" history data """
					
					date = re.match(r'(.*)\((.*)時\)', m.group(9), re.I)
					if date:
						""" date format 2015-03-13 00:00:00 """
						date = date.group(1) + ' ' + date.group(2) + ":00:00"
					name = m.group(2)
					value = m.group(11)

					if name == '石門水庫':
						code = 1
						Print_Fun(code, date, value)
					elif name == '新山水庫':
						code = 2 
						Print_Fun(code, date, value)
					elif name == '翡翠水庫':
						code = 3 
						Print_Fun(code, date, value)
					elif name == '寶山水庫':
						code = 4 
						Print_Fun(code, date, value)
					elif name == '寶山第二水庫':
						code = 5 
						Print_Fun(code, date, value)
					elif name == '永和山水庫':
						code = 6 
						Print_Fun(code, date, value)
					elif name == '明德水庫':
						code = 7 
						Print_Fun(code, date, value)
					elif name == '鯉魚潭水庫':
						code = 8 
						Print_Fun(code, date, value)
					elif name == '德基水庫':
						code = 9 
						Print_Fun(code, date, value)
					elif name == '石岡壩':
						code = 10
						Print_Fun(code, date, value)
					elif name == '霧社水庫':
						code = 11
						Print_Fun(code, date, value)
					elif name == '日月潭水庫':
						code = 12
						Print_Fun(code, date, value)
					elif name == '仁義潭水庫':
						code = 13 
						Print_Fun(code, date, value)
					elif name == '蘭潭水庫':
						code = 14
						Print_Fun(code, date, value)
					elif name == '烏山頭水庫':
						code = 15
						Print_Fun(code, date, value)
					elif name == '曾文水庫':
						code = 16
						Print_Fun(code, date, value)
					elif name == '南化水庫':
						code = 17
						Print_Fun(code, date, value)
					elif name == '阿公店水庫':
						code = 18
						Print_Fun(code, date, value)
					elif name == '阿公店水庫(洩洪至二仁溪)':
						code = 19
						Print_Fun(code, date, value)
					elif name == '牡丹水庫':
						code = 20
						Print_Fun(code, date, value)
					elif name == '成功水庫':
						code = 21
						Print_Fun(code, date, value)

					""" epa.aqx.site_code.14.pm25,2015-03-12 16:00:00,1.0 """
					#print 'epa.aqx.site_code' + '.' + str(code) + '.' + 'cap' + ',' + str(date) + ',' + m.group(11)


					#print m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7), m.group(8), m.group(9), m.group(10), m.group(11), m.group(12)
			f.close	
			#print info[1]


