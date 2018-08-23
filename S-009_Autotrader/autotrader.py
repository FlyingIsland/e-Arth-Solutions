import time
import json
import requests
from bs4 import BeautifulSoup
import argparse, sys
import csv
import re
import pymysql

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	parser.add_argument("-user","--user", help="DB user",type=str, required='True')
	parser.add_argument("-host","--host", help="DB host",type=str, required='True')
	parser.add_argument("-port","--port", help="DB port",type=str, required='True')
	parser.add_argument("-password","--password", help="DB password",type=str, required='True')
	parser.add_argument("-database","--database", help="DB name",type=str, required='True')
	parser.add_argument("-interval","--interval", help="time internal after each request",type=int, default=5)
	return vars(parser.parse_args())

arguments = build_arg_parser()
interval = arguments['interval']

try:
	conn = pymysql.connect(user = str(arguments['user']), port = int(arguments['port']), database = arguments['database'], host = arguments['host'], password = arguments['password'])
	cur = conn.cursor()
except Exception as e:
	print(str(e))
	print("Could not connect to Database")
	sys.exit()
try:
	select_query = "select zip, radius, startyear, endyear, make, model, trim, id, url from search"
	cur.execute(select_query)
	if(cur.rowcount > 0):
		search_result = cur.fetchall()
		for each_search in search_result:
			try:
				search_id = str(each_search[7])
				if(each_search[8] is not None and each_search[8] != ""):
					url_created = str(each_search[8])
				else:
					zipp = ""
					radius = ""
					startyear = ""
					endyear = ""
					make = ""
					model = ""
					trim = ""
					if(each_search[0]):
						zipp = each_search[0]
					if(each_search[1]):
						radius = each_search[1]
					if(each_search[2]):
						startyear = each_search[2]
					if(each_search[3]):
						endyear = each_search[3]
					if(each_search[4]):
						make = each_search[4]
					if(each_search[5]):
						model = each_search[5]
					if(each_search[6]):
						trim = each_search[6]
					url_created = "http://www.autotrader.com/cars-for-sale/searchresults.xhtml?zip="+str(zipp)+"&startYear="+str(startyear)+"&endYear="+str(endyear)+"&makeCodeList="+str(make)+"&searchRadius="+str(radius)+"&modelCodeList="+str(model)+"&trimCodeList="+str(trim)+"&sortBy=derivedpriceASC&numRecords=100&firstRecord=0"
					sql_update_search = "update search set url = '"+str(url_created)+"' where id = '"+str(search_id)+"'"
					cur.execute(sql_update_search)
					conn.commit()

				print("Working for url - "+url_created)
				time.sleep(interval)
				response = requests.get(url_created)
				html = response.content
				soup = BeautifulSoup(html,'html.parser')
				div_all = soup.findAll("div", {"class":"item-card row"})
				count = 0
				for each_div in div_all:
						a_tag = each_div.find('a', href=True)
						if(a_tag):
							link_each = a_tag['href']
							link_with_listing = link_each.split('&')[0]
							iisting_id = link_with_listing.split("listingId=")[1] if link_with_listing and len(link_with_listing.split("listingId=")) > 0 else "" 
							if(iisting_id):
								try:
									count +=  1
									url = "http://www.autotrader.com"+link_with_listing
									text = ""
									h2_tags = each_div.findAll(lambda tag: tag.name == 'h2')
									for each_h2 in h2_tags:
										name_tag = each_h2.parent.find("h2", {"class": lambda x: x and 'text-bold' in x.split() and 'text-gray-base' in x.split()})
										if(name_tag):
											text = name_tag.text
									
									time.sleep(interval)
									response = requests.get(url)
									html = response.content
									soup = BeautifulSoup(html,'html.parser')

									price = ""
									price_div = soup.findAll("div", {"class": "display-flex"})
									if(price_div):
										for each_div in price_div:
											price_tag = each_div.find('div', {"class" : lambda x: x and 'text-success' in x.split()})
											if(price_tag):
												price = price_tag.text
									
									mil_value = ""
									milage_div = soup.find(lambda tag: tag.name == 'div' and tag.text == "MILEAGE")
									if(milage_div):
										if(milage_div.parent.find('div',{'class':'item-card-body'})):
											for each_div in milage_div.parent.find('div',{'class':'item-card-body'}):
												mil_value = str(each_div.text)
									
									int_value = ""
									milage_div = soup.find(lambda tag: tag.name == 'div' and tag.text == "INTERIOR")
									if(milage_div):
										if(milage_div.parent.find('div',{'class':'item-card-body'})):
											for each_div in milage_div.parent.find('div',{'class':'item-card-body'}):
												int_value = str(each_div.text)

									ext_value = ""
									milage_div = soup.find(lambda tag: tag.name == 'div' and tag.text == "EXTERIOR")
									if(milage_div):
										if(milage_div.parent.find('div',{'class':'item-card-body'})):
											for each_div in milage_div.parent.find('div',{'class':'item-card-body'}):
												ext_value = str(each_div.text)

									stk_value = ""
									milage_div = soup.find(lambda tag: tag.name == 'span' and tag.text == "STOCK NUMBER")
									if(milage_div):
										if(milage_div.parent.find('span',{'class':'text-sm text-bold'})):
											for each_div in milage_div.parent.find('span',{'class':'text-sm text-bold'}):
												stk_value = str(each_div)

									vin_value = ""
									milage_div = soup.find(lambda tag: tag.name == 'span' and tag.text == "VIN")
									if(milage_div):
										if(milage_div.parent.find('span',{'class':'text-sm text-bold'})):
											for each_div in milage_div.parent.find('span',{'class':'text-sm text-bold'}):
												vin_value = str(each_div)
									print(iisting_id	)
									print(url)
									print(text)
									print(mil_value)
									print(int_value)
									print(ext_value)
									print(stk_value)
									print(vin_value)
									print(price)
									print(count)
									print("-----------")
									sql_insert_update_listing = "insert into listing (id, url, text, mileage, interior, exterior, stock, vin, search) values ('"+str(iisting_id	)+"', '"+str(url)+"', '"+str(text)+"', '"+str(mil_value)+"', '"+str(int_value)+"', '"+str(ext_value)+"', '"+str(stk_value)+"', '"+str(vin_value)+"', '"+str(search_id)+"') ON DUPLICATE KEY UPDATE id = values(id),url = values(url),text = values(text),mileage = values(mileage),interior = values(interior),exterior = values(exterior),stock = values(stock),vin = values(vin)"
									cur.execute(sql_insert_update_listing)
									conn.commit()
									sql_insert_update_price = "insert into price (listing, price) values ('"+str(iisting_id)+"', '"+str(price)+"') ON DUPLICATE KEY UPDATE listing = values(listing), price = values(price)"
									cur.execute(sql_insert_update_price)
									conn.commit()
								except Exception as e:
									print("Exception for iner id - "+str(iisting_id))
									print(str(e))
									continue
				print("Done for url - "+url_created)
			except Exception as e:
				print("Exception for url - "+url_created)
				print(str(e))
				continue

		print("Completed for each records in search table")
	else:
		print("No records in search table")
	cur.close()
	conn.close()
except Exception as e:
	print("Something went wrong")
	cur.close()
	conn.close()
	print(str(e))
