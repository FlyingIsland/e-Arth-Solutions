import xml.etree.ElementTree as ET
import argparse
import requests
import datetime
import os

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	parser.add_argument("-url","--url", help="url of the xml",type=str, required='True')
	parser.add_argument("-year","--year", help="year to search",type=str, required='True')
	return vars(parser.parse_args())

argments = build_arg_parser()

file_url = argments['url']
year = argments['year']

xmlgot = requests.get(file_url).text

timenow = str(datetime.datetime.now().strftime('%H%M%S'))
file_path = '/tmp/file_'+str(timenow)+'.xml'

f = open(file_path, 'w')
f.write(str(xmlgot))
f.close()

tree=ET.parse(file_path)
root=tree.getroot()

# date_range_1 = 'C_0001318605_20170101_20171231'
date_range = 'C_0001318605_'+str(year)+'0101_'+str(year)+'1231'

ns = {'us-gaap':'http://fasb.org/us-gaap/2017-01-31'}

try:
	element = root.findall("us-gaap:Revenues[@contextRef='"+date_range+"']", ns)
	if(len(element)):
		for each in element:
			print("For "+str(year)+" => "+str(each.text))
	else:
		print("Not found for "+str(year))

except Exception as e:
	print(e)
	print('Something went wrong')

os.remove(file_path)
