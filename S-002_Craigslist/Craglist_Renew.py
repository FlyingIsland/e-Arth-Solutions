from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from inspect import getsourcefile
import time
import os
from os.path import abspath

# Will need to uncomment this 3 lines will running on server

# from pyvirtualdisplay import Display


# display = Display(visible=0, size=(1024, 768))
# display.start()

# Email Id and password of Craiglist Account
email_id = ''
password = ''

file_path = abspath(getsourcefile(lambda _: None))
file_dir = os.path.normpath(file_path + os.sep + os.pardir)

chromedriver = file_dir + "/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
driver.get("https://accounts.craigslist.org/login/home")

driver.find_element_by_id('inputEmailHandle').send_keys(email_id)
driver.find_element_by_id('inputPassword').send_keys(password)

try:
	driver.find_element_by_xpath('/html/body/section/section/div/div[1]/form/div[3]/button').click()

except Exception as e:
	print(e)
	print('Something went wrong')
	time.sleep(2)

time.sleep(2)
count = 0


try:
	table = driver.find_element_by_xpath('//*[@id="paginator"]/table')
	for table_rows in table.find_elements_by_tag_name("tr"):
		for table_data in table_rows.find_elements_by_tag_name("td"):
			class_name = table_data.get_attribute("class")
			if(str(class_name) == "buttons active"):
				button_div = table_data.find_element_by_tag_name('div')
				for buttons_forms in button_div.find_elements_by_tag_name('form'):
					for input_in_forms in buttons_forms.find_elements_by_tag_name('input'):
						get_type = input_in_forms.get_attribute("type")
						get_value = input_in_forms.get_attribute("value")
						if(str(get_value) == "renew" and str(get_type) == "submit"):
							count = count + 1
except Exception as e:
	print(e)
	print('Something went wrong')
	time.sleep(2)


print("Total Renew Count : "+str(count))

flag = 0
max_count = 0
renew_done = 0

while(count != 0 or max_count == 1000):
	max_count += 1
	driver.get("https://accounts.craigslist.org/login/home")
	table = driver.find_element_by_xpath('//*[@id="paginator"]/table')
	try:
		for table_rows in table.find_elements_by_tag_name("tr"):
			if(flag == 1):
				flag = 0
				break
			for table_data in table_rows.find_elements_by_tag_name("td"):
				if(flag == 1):
					flag = 0
					break
				class_name = table_data.get_attribute("class")
				if(str(class_name) == "buttons active"):
					button_div = table_data.find_element_by_tag_name('div')
					for buttons_forms in button_div.find_elements_by_tag_name('form'):
						if(flag == 1):
							flag = 0
							break
						for input_in_forms in buttons_forms.find_elements_by_tag_name('input'):
							get_type = input_in_forms.get_attribute("type")
							get_value = input_in_forms.get_attribute("value")
							# if(str(get_value) == "renew" and str(get_type) == "submit"):								
							if(str(get_value) == "renew" and str(get_type) == "submit"):
								input_in_forms.click()
								# print(input_in_forms.get_attribute("value"))
								count = count - 1
								renew_done += 1
								time.sleep(3)
								flag = 1
								break
	except Exception as e:
		continue

print("Total Renew done : "+str(renew_done))
driver.close()