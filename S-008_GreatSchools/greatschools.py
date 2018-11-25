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
	parser.add_argument("-url","--url", help="url to search",type=str)
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
print("Starting Data extraction for the State and Cities")

states_url = []
base_url = 'https://www.greatschools.org'
first_state_url = arguments['url']
states_url.append(first_state_url)
response = requests.get(first_state_url)
html = response.content
soup = BeautifulSoup(html,'html.parser')
drop_down = soup.find("select", {"id": "dropdown_menu"})
if(drop_down):
	options = drop_down.findAll("option")
	for each_option in options:
		# option_value = each_option.find("option")
		start = str(each_option).find('value="')
		end_to = str(each_option).find('">')
		if(start > 1 and end_to > 1):
			start_from = start + 7
			complete_url = base_url + str(each_option)[start_from:end_to]
			states_url.append(complete_url)

if(len(states_url) > 0):
	for each_state_url in states_url:
		print("Working for :"+str(each_state_url))
		splited_url = each_state_url.split('/')
		if(len(splited_url) == 8):
			state = splited_url[5]
			state_abbr = splited_url[6]
		else:
			state = ''
			state_abbr = ''
		state_url = each_state_url
		time.sleep(interval)
		response = requests.get(each_state_url)
		html = response.content
		soup = BeautifulSoup(html,'html.parser')
		table_tr = soup.find("table").findAll('tr')
		for each_tr in table_tr:
			td_row = each_tr.find('td')
			if(td_row):
				a_td = td_row.find('a')
				if(a_td):
					if(a_td['href']):
						city_url = a_td['href']
						splited_city_url = city_url.split('/')
						if(len(splited_city_url) == 6):
							city = splited_city_url[4]
						else:
							city = ""
						sql_insert_update = "insert into city (state, state_abbr, state_url, city, city_url) values ('"+state.replace("'","")+"', '"+state_abbr.replace("'","")+"', '"+state_url.replace("'","")+"', '"+city.replace("'","")+"', '"+city_url.replace("'","")+"') ON DUPLICATE KEY UPDATE state = values(state), state_abbr = values(state_abbr), state_url = values(state_url), city = values(city), city_url = values(city_url)"
						cur.execute(sql_insert_update)
						conn.commit()

print("Completed the State and Cities Data Extraction. Now extracting School data whose list_school = 1")
select_list_school = "select id, city_url from city where list_school = 1"
cur.execute(select_list_school)
if(cur.rowcount > 0):
	list_school = cur.fetchall()
	for each_School in list_school:
		if(each_School and each_School[1]):
			search_url = each_School[1]
			city_id = each_School[0]
			print("Extracting for City URL "+str(search_url))
			all_school_details = []
			counter = 0
			page_count = 1
			while(True):
				url_to_search = search_url+"schools/?page="+str(page_count)+"&view=table"
				page_count += 1
				try:
					time.sleep(interval)
					response = requests.get(url_to_search)
					html = response.text
					soup = BeautifulSoup(html,'html.parser')
					s = soup.findAll('script')
					cdata = soup.find(text=re.compile("CDATA"))
					splited = cdata.split(";")
					for each in splited:
						if("gon.search" in each):
							gon_search = each
					gon_search_splited = gon_search.replace('gon.search=',"")
					#if(len(gon_search_splited) > 0):
					#	gon_search = gon_search_splited[1]
					#else:
					#	print("Not able to extract for "+str(url_to_search))
					#	continue
					d = json.loads(gon_search_splited)
					if(len(d['schools']) > 0):
						for table_row in d['schools']:
							school_details = []
							if(table_row['name']):
								name = str(table_row['name'].encode().decode().strip())
							else:
								name = ""
							
							if(table_row['links']['profile']):
								school_url = "https://www.greatschools.org"+str(table_row['links']['profile'])
							else:
								school_url = ""
							
							if(table_row['address']['street1']):
								address = str(table_row['address']['street1'].encode().decode().strip())+", "
							else:
								address = ""
							if(table_row['address']['street2'] != "" and table_row['address']['street2']):
								address += str(table_row['address']['street2'].encode().decode().strip())+", "
							if(table_row['address']['city']):
								address += str(table_row['address']['city'].encode().decode().strip())+", "
							if(table_row['state']):
								address += str(table_row['state'].encode().decode().strip())+", "
							if(table_row['address']['zip']):
								address += str(table_row['address']['zip'])
							
							if(table_row['schoolType']):
								schooltype = str(table_row['schoolType'])
							else:
								schooltype = ""
							if(table_row['gradeLevels']):
								grades = str(table_row['gradeLevels'])
							else:
								grades = ""
							# if(table_row['rating'] is not None):
							# 	greatschools_rating = str(table_row['rating'])
							# else:
							# 	greatschools_rating = ""
							if(table_row['parentRating'] is not None):
								review_stars = str(table_row['parentRating'])
							else:
								review_stars = ""

							if(table_row['numReviews'] is not None):
								reviews_count = str(table_row['numReviews'])
							else:
								reviews_count = ""

							if(table_row['enrollment'] is not None):
								enrollment = str(table_row['enrollment'])
							else:
								enrollment = ""

							if('studentsPerTeacher' in table_row and table_row['studentsPerTeacher'] is not None):
								students_per_teacher = str(table_row['studentsPerTeacher'])
							else:
								students_per_teacher = "N/A"
							
							if(table_row['districtName'] is not None):
								district = str(table_row['districtName'])
							else:
								district = ""

							if(school_url):
								response = requests.get(school_url)
								html = response.text
								soup = BeautifulSoup(html,'html.parser')
								test_scores_a_tag = soup.find(lambda tag: tag.name == 'a' and tag.get('href') == "#Test_scores" and tag.find("span", {"class": lambda x: x and 'gs-rating' in x.split()}))
								if(test_scores_a_tag):
									test_scores_span_tag = test_scores_a_tag.find("span", {"class": lambda x: x and 'gs-rating' in x.split()})
									if(test_scores_span_tag):
										test_scores = test_scores_span_tag.text.strip().encode().decode().strip()
									else:
										test_scores = ""
								else:
									test_scores = ""

								academic_progress_a_tag = soup.find(lambda tag: tag.name == 'a' and tag.get('href') == "#Academic_progress" and tag.find("span", {"class": lambda x: x and 'gs-rating' in x.split()}))
								if(academic_progress_a_tag):
									academic_progress_span_tag = academic_progress_a_tag.find("span", {"class": lambda x: x and 'gs-rating' in x.split()})
									if(academic_progress_span_tag):
										academic_progress = academic_progress_span_tag.text.strip().encode().decode().strip()
									else:
										academic_progress = ""
								else:
									academic_progress = ""

								equity_overview_a_tag = soup.find(lambda tag: tag.name == 'a' and tag.get('href') == "#Equity_overview" and tag.find("span", {"class": lambda x: x and 'gs-rating' in x.split()}))
								if(equity_overview_a_tag):
									equity_overview_span_tag = equity_overview_a_tag.find("span", {"class": lambda x: x and 'gs-rating' in x.split()})
									if(equity_overview_span_tag):
										equity_overview = equity_overview_span_tag.text.strip().encode().decode().strip()
									else:
										equity_overview = ""
								else:
									equity_overview = ""

								try:
									student_low_income = ""
									s = soup.findAll('script',{"data-component-name":"SchoolProfileComponent"})
									if(s):
										if(len(s) > 0):
											for each_s in s:
												if(each_s.text):
													d1 = json.loads(each_s.text)
													if("title" in d1):
														if(d1['title'] == "Low-income students"):
															if("data" in d1):
																if(len(d1['data'])):
																	for each_d1 in d1['data']:
																		if('data' in each_d1):
																			if(each_d1['data']):
																				for each_d1_data in each_d1['data']:
																					if('values' in each_d1_data):
																						if(each_d1_data['values']):
																							for each_value in each_d1_data['values']:
																								if("breakdown" in each_value):
																									if(each_value['breakdown'] and each_value['breakdown'] == "Low-income"):
																										if('percentage' in each_value):
																											if(each_value['percentage'] and each_value['percentage'] != "None"):
																												student_low_income = str(each_value['percentage'])
																								else:
																									for key, value in each_d1_data['values'].items():
																										for each_value1 in value:
																											if("breakdown" in each_value1):
																												if(each_value1['breakdown'] and each_value1['breakdown'] == "Low-income"):
																													if('percentage' in each_value1):
																														if(each_value1['percentage'] and each_value1['percentage'] != "None"):
																															student_low_income = str(each_value1['percentage'])


								except Exception as e:
									print(e)
									student_low_income = ""

								
								try:
									students_gender_male = ""
									cdata = soup.find(text=re.compile("CDATA"))
									splited = cdata.split(";")
									for each in splited:
										if("gon.gender" in each):
											gon_gender = each
									gon_gender_splited = gon_gender.split("=")
									if(len(gon_gender_splited) > 0):
										gon_gender = gon_gender_splited[1]
										d2 = json.loads(gon_gender)
										if('Male' in d2):
											if(len(d2['Male']) > 0):
												gender_data = d2['Male'][0]
												if('school_value' in gender_data):
													students_gender_male = str(gender_data['school_value'])
									else:
										print("Not able to extract gender data for "+str(school_url))
								except Exception as e:
									print(e)
									students_gender_male = ""

								student_ethnicities_asian = ""
								student_ethnicities_filipino = ""
								student_ethnicities_hispanic = ""
								student_ethnicities_two_or_more_races = ""
								student_ethnicities_white = ""
								student_ethnicities_black = ""
								student_ethnicities_pacific_Islander = ""
								student_ethnicities_american_indian_alaska_native = ""
								student_ethnicities_hawaiian_native_pacific_islander = ""
								student_ethnicities_asian_or_pacific_islander = ""
								student_ethnicities_asian_or_asian_pacific_islander = ""
								try:
									cdata = soup.find(text=re.compile("CDATA"))
									splited = cdata.split(";")
									for each in splited:
										if("gon.ethnicity" in each):
											gon_ethnicity = each
									gon_ethnicity_splited = gon_ethnicity.split("=")
									if(len(gon_ethnicity_splited) > 0):
										gon_ethnicity_array = gon_ethnicity_splited[1]
										d3 = json.loads(gon_ethnicity_array)
										if(d3):
											for each_ethnicity in d3:
												if("breakdown" in each_ethnicity):
													if(each_ethnicity['breakdown'] == 'Asian'):
														if("school_value" in each_ethnicity):
															student_ethnicities_asian = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Filipino'):
														if("school_value" in each_ethnicity):
															student_ethnicities_filipino = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Hispanic'):
														if("school_value" in each_ethnicity):
															student_ethnicities_hispanic = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Two or more races'):
														if("school_value" in each_ethnicity):
															student_ethnicities_two_or_more_races = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'White'):
														if("school_value" in each_ethnicity):
															student_ethnicities_white = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Black'):
														if("school_value" in each_ethnicity):
															student_ethnicities_black = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Pacific Islander'):
														if("school_value" in each_ethnicity):
															student_ethnicities_pacific_Islander = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'American Indian/Alaska Native'):
														if("school_value" in each_ethnicity):
															student_ethnicities_american_indian_alaska_native = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Hawaiian Native/Pacific Islander'):
														if("school_value" in each_ethnicity):
															student_ethnicities_hawaiian_native_pacific_islander = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Asian or Pacific Islander'):
														if("school_value" in each_ethnicity):
															student_ethnicities_asian_or_pacific_islander = each_ethnicity['school_value']
													elif(each_ethnicity['breakdown'] == 'Asian or Asian/Pacific Islander'):
														if("school_value" in each_ethnicity):
															student_ethnicities_asian_or_asian_pacific_islander = each_ethnicity['school_value']
													else:
														print("Found new student_ethnicities : ")
														print(each_ethnicity)

									else:
										print("Not able to extract ethnicity data for "+str(school_url))
								except Exception as e:
									print(e)
							else:
								test_scores = ""
								academic_progress = ""
								equity_overview = ""
								student_low_income = ""
								students_gender_male = 0
							school_details.append(name)
							school_details.append(school_url)
							school_details.append(address)
							school_details.append(schooltype)
							school_details.append(grades)
							# school_details.append(greatschools_rating)
							school_details.append(review_stars)
							school_details.append(reviews_count)
							school_details.append(enrollment)
							school_details.append(students_per_teacher)
							school_details.append(district)
							school_details.append(test_scores)
							school_details.append(academic_progress)
							school_details.append(equity_overview)
							school_details.append(student_low_income)
							school_details.append(students_gender_male)
							school_details.append(student_ethnicities_asian)
							school_details.append(student_ethnicities_filipino)
							school_details.append(student_ethnicities_hispanic)
							school_details.append(student_ethnicities_two_or_more_races)
							school_details.append(student_ethnicities_white)
							school_details.append(student_ethnicities_black)
							school_details.append(student_ethnicities_pacific_Islander)
							school_details.append(student_ethnicities_american_indian_alaska_native)
							school_details.append(student_ethnicities_hawaiian_native_pacific_islander)
							school_details.append(student_ethnicities_asian_or_pacific_islander)
							school_details.append(student_ethnicities_asian_or_asian_pacific_islander)
							# print(school_details)
							sql_insert_update_school = "insert into school (name, school_url, address, schooltype, grades, review_stars, reviews_count, enrollment, students_per_teacher, district, test_scores, academic_progress, equity_overview, student_low_income, students_gender_male, student_ethnicities_asian, student_ethnicities_filipino, student_ethnicities_hispanic, student_ethnicities_two_or_more_races, student_ethnicities_white, student_ethnicities_black, student_ethnicities_pacific_Islander, student_ethnicities_american_indian_alaska_native, student_ethnicities_hawaiian_native_pacific_islander, student_ethnicities_asian_or_pacific_islander, student_ethnicities_asian_or_asian_pacific_islander) values ('"+str(name).replace("'","")+"','"+str(school_url).replace("'","")+"','"+str(address).replace("'","")+"','"+str(schooltype).replace("'","")+"','"+str(grades).replace("'","")+"','"+str(review_stars).replace("'","")+"','"+str(reviews_count).replace("'","")+"','"+str(enrollment).replace("'","")+"','"+str(students_per_teacher).replace("'","")+"','"+str(district).replace("'","")+"','"+str(test_scores).replace("'","")+"','"+str(academic_progress).replace("'","")+"','"+str(equity_overview).replace("'","")+"','"+str(student_low_income).replace("'","")+"','"+str(students_gender_male).replace("'","")+"','"+str(student_ethnicities_asian).replace("'","")+"','"+str(student_ethnicities_filipino).replace("'","")+"','"+str(student_ethnicities_hispanic).replace("'","")+"','"+str(student_ethnicities_two_or_more_races).replace("'","")+"','"+str(student_ethnicities_white).replace("'","")+"','"+str(student_ethnicities_black).replace("'","")+"','"+str(student_ethnicities_pacific_Islander).replace("'","")+"','"+str(student_ethnicities_american_indian_alaska_native).replace("'","")+"','"+str(student_ethnicities_hawaiian_native_pacific_islander).replace("'","")+"','"+str(student_ethnicities_asian_or_pacific_islander).replace("'","")+"','"+str(student_ethnicities_asian_or_asian_pacific_islander).replace("'","")+"') ON DUPLICATE KEY UPDATE name = values(name),school_url = values(school_url),address = values(address),schooltype = values(schooltype),grades = values(grades),review_stars = values(review_stars),reviews_count = values(reviews_count),enrollment = values(enrollment),students_per_teacher = values(students_per_teacher),district = values(district),test_scores = values(test_scores),academic_progress = values(academic_progress),equity_overview = values(equity_overview),student_low_income = values(student_low_income),students_gender_male = values(students_gender_male),student_ethnicities_asian = values(student_ethnicities_asian),student_ethnicities_filipino = values(student_ethnicities_filipino),student_ethnicities_hispanic = values(student_ethnicities_hispanic),student_ethnicities_two_or_more_races = values(student_ethnicities_two_or_more_races),student_ethnicities_white = values(student_ethnicities_white),student_ethnicities_black = values(student_ethnicities_black),student_ethnicities_pacific_Islander = values(student_ethnicities_pacific_Islander),student_ethnicities_american_indian_alaska_native = values(student_ethnicities_american_indian_alaska_native), student_ethnicities_asian_or_pacific_islander = values(student_ethnicities_asian_or_pacific_islander), student_ethnicities_asian_or_asian_pacific_islander = values(student_ethnicities_asian_or_asian_pacific_islander)"

							cur.execute(sql_insert_update_school)
							conn.commit()
							all_school_details.append(school_details)
							counter += 1

					else:
						break
				except Exception as e:
					print("Something went wrong for url : "+str(url_to_search))
					print(str(e))
				if(page_count > 1000000):
					print("Breaking the Loop as crossed limit of 1000000")
					break
			print("Total Schools : "+str(counter))
			update_school_count = "update city set school_count = '"+str(counter)+"' where id = '"+str(city_id)+"'"
			conn.commit()
		else:
			print("Not got city_url for id :"+str(each_School[0]))
else:
	print("No School with List school set as 1")
