from selenium import webdriver
from inspect import getsourcefile
import time
import os
from os.path import abspath
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

file_path = abspath(getsourcefile(lambda _: None))
file_dir = os.path.normpath(file_path + os.sep + os.pardir)

chromedriver = file_dir + "/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
driver.get("http://delve.tech/ip")
driver.close()
