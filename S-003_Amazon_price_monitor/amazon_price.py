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
import datetime,sys, os
import requests
from email import encoders
import pymysql

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	# parser.add_argument("-asin","--asin", help="amazon asin",type=str, required='True')
	parser.add_argument("-user","--user", help="DB user",type=str, required='True')
	parser.add_argument("-host","--host", help="DB host",type=str, required='True')
	parser.add_argument("-port","--port", help="DB port",type=str, required='True')
	parser.add_argument("-password","--password", help="DB password",type=str, required='True')
	parser.add_argument("-database","--database", help="DB name",type=str, required='True')
	parser.add_argument("-path","--path", help="path to save csv",type=str, required='True')
	parser.add_argument("-i","--interval", help="time internal after each request",type=int, default=5)

	return vars(parser.parse_args())

def product_page(asin):
	name = ''
	weight = ''
	package_dimensions = ''
	new_shipping_weight = ''
	
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
			sql_insert = "insert into product (asin, name, weight, package_dimensions, shipping_weight) values ('"+str(asin)+"', '"+str(name)+"', '"+str(weight)+"', '"+str(package_dimensions)+"', '"+str(new_shipping_weight)+"') ON DUPLICATE KEY UPDATE name  = values(name), weight = values(weight), package_dimensions = values(package_dimensions), shipping_weight = values(shipping_weight)"
			print("Executing product Query")
			print(cur.execute(sql_insert))
			conn.commit()

		offer_url = 'https://www.amazon.com/gp/offer-listing/'+asin
		response_offer = requests.get(offer_url, headers=uaHeader)
		print(response_offer)
		html_offer = response_offer.content
		soup_offer = BeautifulSoup(html_offer, 'html.parser')
		data_list = []
		a = 0
		all_offers = []
		for i in range(1,4):
			final_price = 0
			condition = ''
			seller = ''
			offer_data = []
			row = []
			count = 0
			while(len(row) == 0):
				if(count == 1000):
					break
				count = count + 1
				a = a + 1
				row = soup_offer.select("#olpOfferList > div > div > div:nth-of-type("+str(a)+") > div.a-column.a-span2.olpPriceColumn > span")
			if(len(row)>0):
				price = row[0].text.strip()
				final_price = price.replace("$"," ")
				row_condition = soup_offer.select("#olpOfferList > div > div > div:nth-of-type("+str(a)+") > div.a-column.a-span3.olpConditionColumn > div > span")
				if(len(row_condition)>0):
					condition = row_condition[0].text.strip()
				
				row_seller = soup_offer.select("#olpOfferList > div > div > div:nth-of-type("+str(a)+") > div.a-column.a-span2.olpSellerColumn > h3 > span > a")
				
				if(len(row_seller)>0):
					seller = row_seller[0].text.strip()
				else:
					seller = "amazon"
				
				row_shipping = soup_offer.select("#olpOfferList > div > div > div:nth-of-type("+str(a)+") > div.a-column.a-span2.olpPriceColumn > p > span > span.olpShippingPrice")
				
				if(len(row_shipping)>0):
					shipping = row_shipping[0].text.strip()
					final_shipping = shipping.replace("$"," ")
					final_price = float(final_price) + float(final_shipping)
				
				print(final_price)
				print(condition)
				print(seller)
				
				if(final_price and condition and seller):
					sql_insert = "insert into offer (asin, rank, price_with_shipping, `condition`, seller) values ('"+str(asin)+"', '"+str(i)+"', '"+str(final_price).replace(" ", "")+"', '"+str(condition)+"', '"+str(seller)+"') ON DUPLICATE KEY UPDATE rank  = values(rank), price_with_shipping = values(price_with_shipping), `condition` = values(`condition`), seller = values(seller)"
					# print(sql_insert)
					print("Executing offer Query")
					print(cur.execute(sql_insert))
					conn.commit()
					
					offer_data = [asin, i, final_price, condition, seller]
					all_offers.append(offer_data)
		
		print(all_offers)
		return 1
	except Exception as e:
		print(str(e))
		print('Something went wrong')
		return 0

def sendmail(filenames):
	try:
		if(len(filenames) > 0):
			fromaddr = "mahesh.s@e-arth.in"
			toaddrs = ["mahesh.s@e-arth.in" , "himanshu@e-arth.in"]
			msg = MIMEMultipart()
			msg['From'] = fromaddr
			msg['To'] = ", ".join(toaddrs)
			msg['Subject'] = "Amazon Product and Offer Report"
			body = "Hello, \n \nPlease find the amazon product and offer report below: \n"
			msg.attach(MIMEText(body, 'plain'))
			for filename in filenames:
				attachment = open(filename, "rb")
				part = MIMEBase('application', 'octet-stream')
				part.set_payload((attachment).read())
				encoders.encode_base64(part)
				part.add_header('Content-Disposition', "attachment; filename= %s" % filename.split('/')[len(filename.split('/')) - 1])
				msg.attach(part)
			
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login("mahesh.s@e-arth.in", "")
			text = msg.as_string()
			server.sendmail(fromaddr, toaddrs, text)
			server.close()
			return 1
		else:
			print('Something went wrong while sending email')
			return 0
	except Exception as e:
		print(str(e))
		print('Something went wrong while sending email 1')
		return 0

argments = build_arg_parser()

try:
	conn = pymysql.connect(user = str(argments['user']), port = int(argments['port']), database = argments['database'], host = argments['host'], password = argments['password'])
	cur = conn.cursor()
except Exception as e:
	print(str(e))
	sys.exit()

asin_query = "select distinct asin from product where active = 1"
cur.execute(asin_query)
result = cur.fetchall()
if(cur.rowcount > 0):
	for asin in result:
		asin_amazon = asin[0]
		print(asin_amazon)
		time.sleep(int(argments['interval']))
		product_data = product_page(str(asin_amazon))

	# try:
	path = argments['path']
	date_format = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
	file_path_product = path+'/Amazonprices_'+str(date_format)+'.csv'
	#file_path_offer = path+'/Offer_'+str(date_format)+'.csv'
	
	#select_query = "select asin, name, weight, package_dimensions, shipping_weight, `condition`, active, updated from product"
	select_query = "select product.asin, product.name, product.weight, product.package_dimensions, product.shipping_weight, product.condition, product.active, product.updated, offer.asin, offer.rank, offer.price_with_shipping, offer.condition, offer.seller, offer.updated from product inner join offer on product.asin = offer.asin"
	cur.execute(select_query)
	product_result = cur.fetchall()
	all_data = []
	if(cur.rowcount > 0):
		
		for product in product_result:
			internal_data = []
			internal_data.append(product[0])
			internal_data.append(product[1])
			internal_data.append(product[2])
			internal_data.append(product[3])
			internal_data.append(product[4])
			internal_data.append(product[5])
			internal_data.append(product[6])
			internal_data.append(product[7])
			internal_data.append(product[9])
			internal_data.append(product[10])
			internal_data.append(product[11])
			internal_data.append(product[12])
			internal_data.append(product[13])
			all_data.append(internal_data)

	with open(file_path_product, 'w') as csvFile:
		fields = ["asin", "name", "weight", "package_dimensions", "shipping_weight", "condition", "active", "updated" , "rank", "price_with_shipping", "condition", "seller", "updated"]
		writer = csv.writer(csvFile, delimiter=',',quoting=csv.QUOTE_ALL)
		writer.writerow(fields)
		for row in all_data:
			writer.writerow(row)
		csvFile.close()

	if(os.path.exists(file_path_product)):
		sendmail([file_path_product])
	# except Exception as e:
	# 	print("Something went wrong while creating csv and send email")
	# 	print(str(e))

