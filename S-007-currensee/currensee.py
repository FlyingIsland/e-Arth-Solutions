import requests
from dateutil.parser import parse
import csv
import sys
import datetime
import argparse
import pymysql

def create_csv(file_path, csv_data):
	files = open(file_path,'w')
	w = csv.writer(files)
	i = 0
	try:
		for row in csv_data:
			if(i ==0 ):
				w.writerow(row.keys())
			w.writerow(row.values())
			i += 1
		return 1
	except Exception as e:
		print(e)
		return 0

def db_operation(all_data, records_date):
	for eachrow in all_data:
		sql_insert_update = "insert into currensee (contract, best_bid_quantity, best_bid_amount, best_ask_amount, best_ask_quantity, spread, ltp, volume, value, oi, number_of_trades, records_date) values ('"+eachrow['contract']+"', '"+eachrow['bset_bid_quantity']+"', '"+eachrow['bset_bid_amount']+"', '"+eachrow['best_ask_amount']+"', '"+eachrow['best_ask_quantity']+"', '"+eachrow['spread']+"', '"+eachrow['ltp']+"', '"+eachrow['volume']+"', '"+eachrow['value']+"', '"+eachrow['oi']+"', '"+eachrow['no_of_trades']+"', '"+str(records_date)+"') ON DUPLICATE KEY UPDATE contract = values(contract), best_bid_quantity = values(best_bid_quantity), best_bid_amount = values(best_bid_amount), best_ask_amount = values(best_ask_amount), best_ask_quantity = values(best_ask_quantity), spread = values(spread), ltp = values(ltp), volume = values(volume), value = values(value), oi = values(oi), number_of_trades = values(number_of_trades), records_date = values(records_date)"
		print(cur.execute(sql_insert_update))
		conn.commit()

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	parser.add_argument("-db_operation","--db_operation", help="DB operation",type=str, required='True')
	parser.add_argument("-csv_operation","--csv_operation", help="CSV operation",type=str, required='True')
	parser.add_argument("-user","--user", help="DB user",type=str, required='True')
	parser.add_argument("-host","--host", help="DB host",type=str, required='True')
	parser.add_argument("-port","--port", help="DB port",type=str, required='True')
	parser.add_argument("-password","--password", help="DB password",type=str, required='True')
	parser.add_argument("-database","--database", help="DB name",type=str, required='True')
	parser.add_argument("-path","--path", help="Path to Save CSV",type=str, required='True')
	return vars(parser.parse_args())

argments = build_arg_parser()

if(argments['csv_operation'] == '0' and argments['db_operation'] == '0'):
	print("Please pass atleast one of the arguments db_operation, csv_operation as 1")
	sys.exit()

if(argments['db_operation'] == '1'):
	try:
		conn = pymysql.connect(user = str(argments['user']), port = int(argments['port']), database = argments['database'], host = argments['host'], password = argments['password'])
		cur = conn.cursor()
	except Exception as e:
		print(str(e))
		print("Could not connect to Database")
		sys.exit()

date_url = 'https://www.nseindia.com/marketinfo/fxTracker/ajaxTicker.jsp'
response_date = requests.post(date_url, data={})
data_output = response_date.text.strip()
	
try:
	splited_data = data_output.split(":")
	splited_dates = splited_data[2].split(" ")
	date = splited_dates[2]
	time = splited_dates[3]
	final_dt = parse(date).strftime('%Y-%m-%d')
	final_time = time.replace(";",":")
	final_datetime = datetime.datetime.strptime(final_dt+" "+final_time,'%Y-%m-%d %H:%M:%S')
except Exception as e:
	print(data_output)
	print(e)
	print("Could not extract the date from url")
	sys.exit()

if(type(final_datetime) == datetime.datetime):
	data = {'instrument':'FUTCUR','currency':'USDINR'}
	API_url = "https://www.nseindia.com/marketinfo/fxTracker/priceWatchData.jsp"
	response = requests.post(API_url, data=data)
	data_output = response.text.strip()
	records_date = final_datetime.strftime('%Y-%m-%d %H:%M:%S')
	i = 0 
	all_data = []
	if("SUCCESS" in str(response.text)):
		splited_data = data_output.split('~')
		for a1 in splited_data:
			if(i == 0):
				each_row = a1[a1.index('USDINR'):]
			else:
				each_row = a1
			data = {}
			each_splited = each_row.split(':')
			if(len(each_splited) == 19):
				data['contract'] = each_splited[0]
				data['bset_bid_quantity'] = each_splited[6]
				data['bset_bid_amount'] = each_splited[7]
				data['best_ask_amount'] = each_splited[8]
				data['best_ask_quantity'] = each_splited[9]
				data['spread'] = str(round(float(data['best_ask_amount']) - float(data['bset_bid_amount']),4))
				data['ltp'] = each_splited[10]
				data['volume'] = each_splited[11]
				data['value'] = each_splited[13].replace(',','')
				data['oi'] = each_splited[12].replace(',','')
				data['no_of_trades'] = each_splited[14]
				all_data.append(data)
			i += 1
	else:
		print("Not got success message from Ajax request.")
		sys.exit()
	
	filename_of_csv = final_datetime.strftime('%Y%m%d-%H%M%S')
	if(argments['db_operation'] == '1'):
		db_operation(all_data, records_date)
	if(argments['csv_operation'] == '1'):
		csv_created = create_csv(str(argments['path'])+"/"+filename_of_csv+".csv", all_data)
		if(csv_created):
			print('CSV Created')
		else:
			print('Something went wrong. CSV Not Created')
else:
	print("Date Time stamp not able to extract. So terminating script")

