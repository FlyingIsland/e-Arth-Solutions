import argparse
import datetime,sys, os
import pymysql
import csv

def build_arg_parser():
	parser = argparse.ArgumentParser(description='Script to learn basic argparse')
	parser.add_argument("-file_path","--file_path", help="File path",type=str, required='True')
	parser.add_argument("-account_number","--account_number", help="Account Number",type=str, required='True')
	parser.add_argument("-user","--user", help="DB user",type=str, required='True')
	parser.add_argument("-host","--host", help="DB host",type=str, required='True')
	parser.add_argument("-port","--port", help="DB port",type=str, required='True')
	parser.add_argument("-password","--password", help="DB password",type=str, required='True')
	parser.add_argument("-database","--database", help="DB name",type=str, required='True')
	return vars(parser.parse_args())

def chase_credit_card(file_path,  currency, account_id, conn):
	print(file_path)
	number_of_columns = 5
	with open(file_path) as File:
		reader = csv.reader(File)
		# Validity Check for number of columns
		ncol=len(next(reader))
		File.seek(0)
		if(ncol == number_of_columns):
			print("Number of columns match")
		else:
			print("Number of columns not match")
			return 0
		# Validity Check for Headers
		sniffer = csv.Sniffer()
		has_header = sniffer.has_header(File.read(2048))
		File.seek(0)
		if(has_header):
			next(reader)
			print("Header present")
		else:
			print("Header not present")

		total_rows = 0
		valid_data_array = []
		for row in reader:
			total_rows = total_rows + 1
			
			internal_row_array = []
			
			date = row[1]
			amount = row[4]
			description = row[3]

			# Validity Check for Date format
			isValidDate = True
			if(currency == 'USD'):
				month,day,year = date.split('/')
			else:
				day,month,year = date.split('/')
			try:
				datetime.datetime(int(year),int(month),int(day))
			except ValueError :
				isValidDate = False
			
			if(isValidDate):
				print("Date Field is in valid format")
			else:
				print("Date Field is not in valid format")
				continue

			# Validity Check for Amount Field
			try:
				amount_decimal = float(amount)
				print("Amount Field is Decimal number")
			except ValueError:
				print("Amount Field is not Decimal number")
				continue

			if(currency == 'USD'):
				date_to_update = datetime.datetime.strptime(str(date),'%m/%d/%Y').strftime('%Y-%m-%d 00:00:00')
			else:
				date_to_update = datetime.datetime.strptime(str(date),'%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
			internal_row_array.append(account_id)
			internal_row_array.append(date_to_update)
			internal_row_array.append(amount)
			internal_row_array.append(description)
			valid_data_array.append(internal_row_array)
		print("------------------------------------")
		if(has_header):
			print("Total rows read from CSV with Header :"+str(total_rows))
		else:
			print("Total rows read from CSV without Header :"+str(total_rows))

		print("Total rows from CSV having Valid Date, Amount : "+str(len(valid_data_array)))
		cur1 = conn.cursor()
		existing_count = 0
		for each_valid in valid_data_array:
			select_count = "select count(id) from transaction where account = '"+str(each_valid[0])+"' and date = '"+str(each_valid[1])+"' and amount = '"+str(each_valid[2])+"' and description = '"+str(each_valid[3]).replace("'","")+"'"			
			# print(select_count)
			cur1.execute(select_count)
			if(cur1.rowcount > 0):
				count = cur1.fetchone()[0]
				if(count):
					existing_count = existing_count + 1
		print("Total transactions exits in the database :"+str(existing_count))
		print("Total transactions will be imported in the database :"+str(len(valid_data_array) - existing_count))
		if((len(valid_data_array) - existing_count) > 0):
			confirmation = str(input("Do you want to import data (yes/no) ?"))
			if(confirmation == "yes"):
				insert_count = 0
				not_inserted_array = []
				for each_valid in valid_data_array:
					# select_count = "select count(id) from transaction where account = '"+str(each_valid[0])+"' and date = '"+str(each_valid[1])+"' and amount = '"+str(each_valid[2])+"' and description = '"+str(each_valid[3])+"'"
					insert_query = "insert into transaction (account, date, amount, description) values ('"+str(each_valid[0])+"', '"+str(each_valid[1])+"', '"+str(each_valid[2])+"', '"+str(each_valid[3]).replace("'","")+"') ON DUPLICATE KEY UPDATE account = account, date = date, amount = amount, description = description "
					# print(insert_query)
					try:
						inserted = cur1.execute(insert_query)
						conn.commit()
						if(inserted == 1):
							insert_count = insert_count + 1
					except Exception as e:
						not_inserted_array.append(each_valid)
				print("Total records imported successfully : "+str(insert_count))
				print("Records failed to import : "+str(len(not_inserted_array)))
				if(len(not_inserted_array) > 0):
					print("Records Failed :")
					for each in not_inserted_array:
						print(str(each[0])+" "+str(each[1])+" "+str(each[2])+" "+str(each[3]))
			else:
				print("Not imported")
		else:
			print("No records to import")

def wf_checking(file_path,  currency, account_id, conn):
	print(file_path)
	number_of_columns = 5
	with open(file_path) as File:
		reader = csv.reader(File)
		# Validity Check for number of columns
		ncol=len(next(reader))
		File.seek(0)
		if(ncol == number_of_columns):
			print("Number of columns match")
		else:
			print("Number of columns not match")
			return 0
		# Validity Check for Headers
		sniffer = csv.Sniffer()
		has_header = sniffer.has_header(File.read(2048))
		File.seek(0)
		if(has_header):
			next(reader)
			print("Header present")
		else:
			print("Header not present")

		total_rows = 0
		valid_data_array = []
		for row in reader:
			total_rows = total_rows + 1
			
			internal_row_array = []
			
			date = row[0]
			amount = row[1]
			description = row[4]

			# Validity Check for Date format
			isValidDate = True
			if(currency == 'USD'):
				month,day,year = date.split('/')
			else:
				day,month,year = date.split('/')
			try:
				datetime.datetime(int(year),int(month),int(day))
			except ValueError :
				isValidDate = False
			
			if(isValidDate):
				print("Date Field is in valid format")
			else:
				print("Date Field is not in valid format")
				continue

			# Validity Check for Amount Field
			try:
				amount_decimal = float(amount)
				print("Amount Field is Decimal number")
			except ValueError:
				print("Amount Field is not Decimal number")
				continue

			if(currency == 'USD'):
				date_to_update = datetime.datetime.strptime(str(date),'%m/%d/%Y').strftime('%Y-%m-%d 00:00:00')
			else:
				date_to_update = datetime.datetime.strptime(str(date),'%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
			internal_row_array.append(account_id)
			internal_row_array.append(date_to_update)
			internal_row_array.append(amount)
			internal_row_array.append(description)
			valid_data_array.append(internal_row_array)
		print("------------------------------------")
		if(has_header):
			print("Total rows read from CSV with Header :"+str(total_rows))
		else:
			print("Total rows read from CSV without Header :"+str(total_rows))

		print("Total rows from CSV having Valid Date, Amount : "+str(len(valid_data_array)))
		cur1 = conn.cursor()
		existing_count = 0
		for each_valid in valid_data_array:
			select_count = "select count(id) from transaction where account = '"+str(each_valid[0])+"' and date = '"+str(each_valid[1])+"' and amount = '"+str(each_valid[2])+"' and description = '"+str(each_valid[3])+"'"

			cur1.execute(select_count)
			if(cur1.rowcount > 0):
				count = cur1.fetchone()[0]
				if(count):
					existing_count = existing_count + 1
		print("Total transactions exits in the database :"+str(existing_count))
		print("Total transactions will be imported in the database :"+str(len(valid_data_array) - existing_count))
		if((len(valid_data_array) - existing_count) > 0):
			confirmation = str(input("Do you want to import data (yes/no) ?"))
			if(confirmation == "yes"):
				insert_count = 0
				not_inserted_array = []
				for each_valid in valid_data_array:
					# select_count = "select count(id) from transaction where account = '"+str(each_valid[0])+"' and date = '"+str(each_valid[1])+"' and amount = '"+str(each_valid[2])+"' and description = '"+str(each_valid[3])+"'"
					insert_query = "insert into transaction (account, date, amount, description) values ('"+str(each_valid[0])+"', '"+str(each_valid[1])+"', '"+str(each_valid[2])+"', '"+str(each_valid[3]).replace("'","")+"') ON DUPLICATE KEY UPDATE account = account, date = date, amount = amount, description = description "
					# print(insert_query)
					try:
						inserted = cur1.execute(insert_query)
						conn.commit()
						if(inserted == 1):
							insert_count = insert_count + 1
					except Exception as e:
						not_inserted_array.append(each_valid)
				print("Total records imported successfully : "+str(insert_count))
				print("Records failed to import : "+str(len(not_inserted_array)))
				if(len(not_inserted_array) > 0):
					print("Records Failed :")
					for each in not_inserted_array:
						print(str(each[0])+" "+str(each[1])+" "+str(each[2])+" "+str(each[3]))
			else:
				print("Not imported")
		else:
			print("No records to import")

def icici_savings(file_path,  currency, account_id, conn):
	print(file_path)
	number_of_columns = 8
	with open(file_path) as File:
		reader = csv.reader(File)
		# Validity Check for number of columns
		ncol=len(next(reader))
		File.seek(0)
		if(ncol == number_of_columns):
			print("Number of columns match")
		else:
			print("Number of columns not match")
			return 0
		# Validity Check for Headers
		sniffer = csv.Sniffer()
		has_header = sniffer.has_header(File.read(2048))
		File.seek(0)
		if(has_header):
			next(reader)
			print("Header present")
		else:
			print("Header not present")

		total_rows = 0
		valid_data_array = []
		for row in reader:
			total_rows = total_rows + 1
			
			internal_row_array = []
			
			date = row[2]
			
			if(row[5] == '0' or row[5] == '' or row[5] == 0):
				amount = row[6]
			else:
				amount = '-'+row[5]
			description = row[4]

			# Validity Check for Date format
			isValidDate = True
			if(currency == 'USD'):
				month,day,year = date.split('/')
			else:
				day,month,year = date.split('/')
			try:
				datetime.datetime(int(year),int(month),int(day))
			except ValueError :
				isValidDate = False
			
			if(isValidDate):
				print("Date Field is in valid format")
			else:
				print("Date Field is not in valid format")
				continue

			# Validity Check for Amount Field
			try:
				amount_decimal = float(amount)
				print("Amount Field is Decimal number")
			except ValueError:
				print("Amount Field is not Decimal number")
				continue

			if(currency == 'USD'):
				date_to_update = datetime.datetime.strptime(str(date),'%m/%d/%Y').strftime('%Y-%m-%d 00:00:00')
			else:
				date_to_update = datetime.datetime.strptime(str(date),'%d/%m/%Y').strftime('%Y-%m-%d 00:00:00')
			internal_row_array.append(account_id)
			internal_row_array.append(date_to_update)
			internal_row_array.append(amount)
			internal_row_array.append(description)
			valid_data_array.append(internal_row_array)
		print("------------------------------------")
		if(has_header):
			print("Total rows read from CSV with Header :"+str(total_rows))
		else:
			print("Total rows read from CSV without Header :"+str(total_rows))

		print("Total rows from CSV having Valid Date, Amount : "+str(len(valid_data_array)))
		cur1 = conn.cursor()
		existing_count = 0
		for each_valid in valid_data_array:
			select_count = "select count(id) from transaction where account = '"+str(each_valid[0])+"' and date = '"+str(each_valid[1])+"' and amount = '"+str(each_valid[2])+"' and description = '"+str(each_valid[3])+"'"
			cur1.execute(select_count)
			if(cur1.rowcount > 0):
				count = cur1.fetchone()[0]
				if(count):
					existing_count = existing_count + 1
		print("Total transactions exits in the database :"+str(existing_count))
		print("Total transactions will be imported in the database :"+str(len(valid_data_array) - existing_count))
		if((len(valid_data_array) - existing_count) > 0):
			confirmation = str(input("Do you want to import data (yes/no) ?"))
			if(confirmation == "yes"):
				insert_count = 0
				not_inserted_array = []
				for each_valid in valid_data_array:
					# select_count = "select count(id) from transaction where account = '"+str(each_valid[0])+"' and date = '"+str(each_valid[1])+"' and amount = '"+str(each_valid[2])+"' and description = '"+str(each_valid[3])+"'"
					insert_query = "insert into transaction (account, date, amount, description) values ('"+str(each_valid[0])+"', '"+str(each_valid[1])+"', '"+str(each_valid[2])+"', '"+str(each_valid[3]).replace("'","")+"') ON DUPLICATE KEY UPDATE account = account, date = date, amount = amount, description = description "
					# print(insert_query)
					try:
						inserted = cur1.execute(insert_query)
						conn.commit()
						if(inserted == 1):
							insert_count = insert_count + 1
						
					except Exception as e:
						not_inserted_array.append(each_valid)
				print("Total records imported successfully : "+str(insert_count))
				print("Records failed to import : "+str(len(not_inserted_array)))
				if(len(not_inserted_array) > 0):
					print("Records Failed :")
					for each in not_inserted_array:
						print(str(each[0])+" "+str(each[1])+" "+str(each[2])+" "+str(each[3]))
			else:
				print("Not imported")
		else:
			print("No records to import")

argments = build_arg_parser()
try:
	conn = pymysql.connect(user = str(argments['user']), port = int(argments['port']), database = argments['database'], host = argments['host'], password = argments['password'])
	cur = conn.cursor()
except Exception as e:
	print(str(e))
	sys.exit()

account_number = argments['account_number']
file_path = argments['file_path']

bank_query = "select account.id, account.bank, account.type, account.currency, bank.shortname from account join bank on account.bank = bank.id where account.number = "+str(account_number)

cur.execute(bank_query)
if(cur.rowcount > 0):
	account_data = cur.fetchone()
	account_id = account_data[0]
	bank = account_data[1]
	account_type = account_data[2]
	currency = account_data[3]
	shortname = account_data[4]
	
	print(shortname)
	print(account_type)

	if(shortname == 'wf' and account_type == 'checking'):
		wf_checking(file_path, currency, account_id, conn)
	elif(shortname == 'icici' and account_type == 'savings'):
		icici_savings(file_path, currency, account_id, conn)
	elif(shortname == 'chase' and account_type == 'credit card'):
		chase_credit_card(file_path, currency, account_id, conn)
	else:
		print("Not Found function")
else:
	print("No Found records for account number in accounts tables")

