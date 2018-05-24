import os
import sys
from scrapy.crawler import CrawlerProcess
import scrapy
import re
import datetime

class ParktakesSpider_level(scrapy.Spider):
    name = 'parktakes_levq'
    def __init__(self, inputq=""):
        self.inputw = inputq
        # self.records_count = 0
    def start_requests(self):
        url = self.inputw
        yield self.make_requests_from_url(url)

    def parse(self, response):
        NAME_SELECTOR = 'table tr'
        for each_td in response.css(NAME_SELECTOR):
            if(each_td.css('tr td p::text').extract_first()):
                if("Records" in str(each_td.css('tr td p::text').extract_first().encode('ascii','ignore'))):
                    records_count.append(each_td.css('tr td p b::text').extract()[2].encode('ascii','ignore'))
                    break

search_url = sys.argv[1]
records_count = []
SETTINGS = {'LOG_ENABLED': False}
process = CrawlerProcess(SETTINGS)
x = ParktakesSpider_level()
process.crawl(x,search_url)
process.start()
print(int(records_count[0]))
