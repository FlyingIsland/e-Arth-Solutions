import argparse
import unittest
import time,re
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.request
from bs4 import BeautifulSoup
import csv
import datetime,sys
import requests
from email import encoders

import pymysql

name = ''
weight = ''
package_dimensions = ''
new_shipping_weight = ''
file_path = ''

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	parser.add_argument("-asin","--asin", help="amazon asin",type=str, required='True')
	parser.add_argument("-user","--user", help="DB user",type=str, required='True')
	parser.add_argument("-host","--host", help="DB host",type=str, required='True')
	parser.add_argument("-port","--port", help="DB port",type=str, required='True')
	parser.add_argument("-password","--password", help="DB password",type=str, required='True')
	parser.add_argument("-database","--database", help="DB name",type=str, required='True')
	parser.add_argument("-path","--path", help="path to save csv",type=str, required='True')

	return vars(parser.parse_args())

def product_page(asin, path):
	global name
	global weight
	global package_dimensions
	global new_shipping_weight
	global file_path
	product_url = 'https://www.amazon.com/dp/'+asin
	uaHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
	response = requests.get(product_url, headers=uaHeader)
	print(response.status_code)
	html = response.content
	soup = BeautifulSoup(html, 'html.parser')
	data_list = []
	try:
		elem1 = soup.find('span', attrs={'class': 'a-size-large'})
		name = elem1.text.strip()
		print(name)
		for table_row in soup.select("#prodDetails > div.wrapper.USlocale > div.column.col1 > div > div.content.pdClearfix > div > div > table"):
			cells = table_row.findAll('td')
			if len(cells) > 0:
				weight = cells[1].text.strip()
				print(weight)
				package_dimensions = cells[3].text.strip()
				print(package_dimensions)
		for table_row1 in soup.select("#prodDetails > div.wrapper.USlocale > div.column.col2 > div:nth-of-type(1) > div.content.pdClearfix > div > div > table"):
			cells = table_row1.findAll('td')
			if len(cells) > 0:
				shipping_weight = cells[7].text.strip()
				new_shipping_weight = re.sub(r'\(.*\)', '', shipping_weight)
				print(new_shipping_weight)

		if(name and weight and package_dimensions and new_shipping_weight):
			date_format = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
			print(date_format)
			array = [{'Name' : name, 'Item Weight' : weight, 'Package Dimensions' : package_dimensions, 'Shipping Weight' : new_shipping_weight}]
			file_path = path+'/Products_'+str(date_format)+'.csv'
			# print(file_path)
			with open(file_path, 'w') as csvFile:
				fields = ['Name', 'Item Weight', 'Package Dimensions', 'Shipping Weight', 'Datetime']
				writer = csv.DictWriter(csvFile, fieldnames=fields)
				writer.writeheader()
				writer.writerows(array)
				csvFile.close()
		else:
			print('Something went wrong. Data not found')
			return 0
		return 1
	except Exception as e:
		print(str(e))
		print('Something went wrong')
		return 0

def sendmail():
	print(file_path)
	try:
		if(file_path):
			fromaddr = "mahesh.s@e-arth.in"
			toaddrs = ["himanshu@e-arth.in" , "mahesh.s@e-arth.in"]
			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['To'] = ", ".join(toaddrs)
			msg['Subject'] = "Amazon Product Report"
			body = "Hello, \n \nPlease find the amazon product report below: \n"
			msg.attach(MIMEText(body, 'plain'))
			filename = "Products.csv"
			attachment = open(file_path, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
			msg.attach(part)
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login("mahesh.s@e-arth.in", "mahesh_1711")
			text = msg.as_string()
			server.sendmail(fromaddr, toaddrs, text)
			server.close()
			return 1
		else:
			print('Something went wrong while sending email.CSV file not found')
			return 0
	except Exception as e:
		print(str(e))
		print('Something went wrong while sending email')
		return 0

argments = build_arg_parser()
product_data = product_page(argments['asin'], argments['path'])
if(product_data):
	try:
		conn = pymysql.connect(user = str(argments['user']), port = int(argments['port']), database = argments['database'], host = argments['host'], password = argments['password'])
		cur = conn.cursor()

		if(name and weight and package_dimensions and new_shipping_weight):
			sql_insert = "insert into product (asin, name, weight, package_dimensions, shipping_weight) values ('"+str(argments['asin'])+"', '"+str(name)+"', '"+str(weight)+"', '"+str(package_dimensions)+"', '"+str(new_shipping_weight)+"') ON DUPLICATE KEY UPDATE name  = values(name), weight = values(weight), package_dimensions = values(package_dimensions), shipping_weight = values(shipping_weight)"
			print(cur.execute(sql_insert))
			conn.commit()
			cur.close()
			conn.close()
	except Exception as e:
		print(str(e))

	send_mail = sendmail()
	print(send_mail)
	if(send_mail == 1):
		print('Send Email successfully')



