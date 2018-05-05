import argparse
import os
from scrapy.crawler import CrawlerProcess
import csv
import scrapy
import re
import datetime
import subprocess
import time

class ParktakesSpider   (scrapy.Spider):
        name = 'parktakes'
        def __init__(self, input_url="", records_count = 0, internval = 0):
                self.input = input_url
                self.records_count = records_count
                self.interval = interval

        def start_requests(self):
                url = self.input
                total_records = int(self.records_count)
                offset_count = total_records/20
                offset_list = []
                off_set = 0
                for i in range(0,round(offset_count+1)):
                        offset_list.append(off_set)
                        off_set = off_set + 20

                for i in offset_list:
#                       time.sleep(self.interval)
                        yield self.make_requests_from_url(url+"&offset=%s" % i)

        def parse(self, response):
                NAME_SELECTOR = 'table tr'
                for each_td in response.css(NAME_SELECTOR):
                        if(len(each_td.css('td')) == 4):
                                row = []
                                for col in each_td.css('td'):
                                        if((col.css('td a::text').extract())):
                                                data = (col.css('td a::text').extract_first().encode('ascii','ignore'))
                                                row.append(data)
                                        else:
                                                if(col.css('td ::text').extract_first()):
                                                        data = (col.css('td ::text').extract_first().encode('ascii','ignore'))
                                                        row.append(data)
                                all_data.append(row)
''' build_arg_parser to get arguments from command line while executing script like category, path, keyword, etc. Note : path and category are required arguments'''
def build_arg_parser():
        parser = argparse.ArgumentParser(description='Script to learn basic argparse')
        parser.add_argument("-p","--path", help="path of output csv file",type=str, required='True', default='.')
        parser.add_argument("-i","--interval", help="time internal after each request",type=int, default=5)
        parser.add_argument("-c","--category", help="category to search",type=str, required='True')
        parser.add_argument("-k","--keyword", help="keyword to search",type=str, default='9999')
        parser.add_argument("-s","--subject", help="subject to search",type=str, default='')
        parser.add_argument("-a","--age", help="age to search",type=str, default='9999')
        parser.add_argument("-d","--day", help="day to search",type=str, default='9999')
        parser.add_argument("-w","--week", help="week to search",type=str)

        return vars(parser.parse_args())

''' Function to create query from arguments passed'''
def build_query_from_arguments(arguments):
        query_string = ""

        ''' Check if arguments are not empty and create query string as required'''
        if(arguments):
                query_string = "rev1_quickresult.asp?category2="+arguments['category'].replace('"','').replace("'","")+"&keywrd="+arguments['keyword'].replace('"','').replace("'","")+"&subject="+arguments['subject'].replace('"','').replace("'","")+"&age="+arguments['age'].replace('"','').replace("'","")
                if(arguments['week']):
                        query_string += "&week="+arguments['week']
                else:
                        query_string += "&day="+arguments['day']

                query_string += "&Submit2=Search"
                print("Arguments ->")
                print("path -> "+arguments['path'])
                print("category -> "+arguments['category'])


        ''' if query string is formed then append the base url and query string'''
        if(query_string):
                final_query = base_url + query_string
                return final_query
        else:
                print('Something went wrong arguments not passed correctly')
                return ""

regex = re.compile(r'[\n\r\t]')
all_data = []

base_url = "http://parktakes.fairfaxcounty.gov/"

arguments = build_arg_parser()
search_url = build_query_from_arguments(arguments)
interval = arguments['interval']
if(search_url):
        print("")
        print("Complete URL -> "+search_url)
        p = subprocess.check_output("python3 ./get_total_records_counts.py '"+search_url+"'", shell = True)
        if(p):
                SETTINGS = {'LOG_ENABLED': False}
                process = CrawlerProcess(SETTINGS)
                x = ParktakesSpider()
                process.crawl(x,search_url,int(p),int(interval))
                process.start()
                if(all_data):
                        try:
                                filename = arguments['path']+"/"+datetime.datetime.now().strftime('%Y%m%d.%H.%M.%S.')+arguments['category']+".csv"
                                with open(filename, "w") as csv_file:
                                        writer = csv.writer(csv_file, delimiter=',')
                                        header_add_flag = 0
                                        for line in all_data:
                                                line = [str(x, 'utf-8') for x in line]
                                                if(header_add_flag == 0):
                                                        if('Title' in line and 'Location' in line and 'Time' in line):
                                                                writer.writerow(line)
                                                                header_add_flag = 1
                                                                continue
                                                if('Title' not in line and 'Location' not in line and 'Time' not in line):
                                                        if(len(line)):
                                                                writer.writerow(line)
                                print("")
                                print("Search Result File Saved in -> "+filename)
                        except Exception as e:
                                print(str(e))
                                print("Something went wrong")
                else:
                        print("Something went wrong data not got for csv")
        else:
                print("Something went wrong data. Not got total records counts")
else:
        print('Something went wrong search URL not generated')