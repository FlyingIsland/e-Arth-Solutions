import argparse, sys
import os
from scrapy.crawler import CrawlerProcess
import csv
import scrapy
import re
import datetime
import subprocess
import time
import pymysql

class CikExtract(scrapy.Spider):
	name = 'cikextract'
	def __init__(self, input_url="", stop_flag = 0, internval = 0):
		self.input = input_url
		self.stop_flag = stop_flag
		self.interval = interval

	def start_requests(self):
		url = self.input
		offset = 0
		while(True):
			if(self.stop_flag == 0):
				url_to_search = url+str(offset)+"&count=40&hidefilings=0"
				offset += 40
				time.sleep(self.interval)
				yield self.make_requests_from_url(url_to_search)
			else:
				print("Extracting Data Completed")
				break
	
	def parse(self, response):
		NAME_SELECTOR = 'table tr'
		table_element = response.css(NAME_SELECTOR)
		if(len(table_element) == 0):
			self.stop_flag = 1
		for each_td in table_element:
			if(len(each_td.css('td')) == 3):
				row = []
				cik = each_td.css('td ::text').extract()[0].encode('ascii','ignore')
				company = each_td.css('td ::text').extract()[1].encode('ascii','ignore')
				state = each_td.css('td ::text').extract()[2].encode('ascii','ignore')
				row.append(cik)
				row.append(company)
				row.append(state)
				all_data.append(row)

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	parser.add_argument("-sic","--sic", help="sic to search",type=str)
	parser.add_argument("-state","--state", help="state to search",type=str)
	
	parser.add_argument("-user","--user", help="DB user",type=str, required='True')
	parser.add_argument("-host","--host", help="DB host",type=str, required='True')
	parser.add_argument("-port","--port", help="DB port",type=str, required='True')
	parser.add_argument("-password","--password", help="DB password",type=str, required='True')
	parser.add_argument("-database","--database", help="DB name",type=str, required='True')
	parser.add_argument("-i","--interval", help="time internal after each request",type=int, default=5)

	return vars(parser.parse_args())

arguments = build_arg_parser()
try:
	conn = pymysql.connect(user = str(arguments['user']), port = int(arguments['port']), database = arguments['database'], host = arguments['host'], password = arguments['password'])
	cur = conn.cursor()
except Exception as e:
	print(str(e))
	sys.exit()
interval = arguments['interval']

sic = ''
state = ''
if(arguments['sic']):
	sic = arguments['sic']
elif(arguments['state']):
	state = arguments['state']
else:
	print("Please provide state or sic as input argument")
	sys.exit()

all_data = []


if(sic):
	search_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC="+str(sic)+"&owner=include&match=&start="

elif(state):
	search_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&State="+str(state)+"&owner=include&match=&start="
else:
	print("Please provide state or sic as input argument")
	sys.exit()

SETTINGS = {'LOG_ENABLED': False}
process = CrawlerProcess(SETTINGS)
x = CikExtract()
process.crawl(x,search_url, 0, int(interval))
process.start()
if(len(all_data) > 0):
	print("Inserting/Updating Records in Table")
	for data in all_data:
		cik_to_update = data[0]
		company_to_update = data[1].replace("\\",'')
		if(sic):
			state_to_update = data[2]
			sic_to_update = sic
		else:
			state_to_update = state
			sic_to_update = ''
		sic_to_update = sic
		try:
			sql_insert = 'insert into company (cik, name, state, sic) values ("'+str(cik_to_update).replace('"',"'")+'", "'+str(company_to_update).replace('"',"'")+'", "'+str(state_to_update).replace('"',"'")+'", "'+str(sic_to_update)+'") ON DUPLICATE KEY UPDATE cik = values(cik), name = values(name), state = values(state)'
			# sql_insert = "insert into company (cik, name, state, sic) values ('"+str(cik_to_update)+"', '"+str(company_to_update)+"', '"+str(state_to_update)+"', '"+str(sic_to_update)+"') ON DUPLICATE KEY UPDATE cik = values(cik), name = values(name), state = values(state)"
			print(cur.execute(sql_insert))
			conn.commit()
		except Exception as e:
			print(e)
			continue
	print("Inserted/Updated Records in Table")
