import scrapy
import re
from scrapy import Request

class QuakegetterSpider(scrapy.Spider):
    name = 'quakeGetter'
    allowed_domains = ['earthquaketrack.com']
    start_urls = ['https://earthquaketrack.com/p/japan/recent', 'https://earthquaketrack.com/v/asia/recent']

    custom_settings = {'LOG_ENABLED': True,  'CONCURRENT_REQUESTS': '1'
    }



    def parse(self, response):
        


        # Scraping the raw list of earthquakes.
        quakeList = response.xpath("//div[contains(@class, 'quakes-info-list')]//div[contains(@class, 'quake-info-container')]")

        # now we clean up the information and merge the strings from each tag into single items in a new list.
        scrubbedQuakes = []

        for earthquake in quakeList:
            quakeStrings = earthquake.xpath("./a//text()").extract()
            commasInvade = quakeStrings[-3]+', '+quakeStrings[-2]+', '+quakeStrings[-1]

            scrubbedQuakes.append(re.sub("\n\s+", " ", " ".join([" ".join(quakeStrings[:-3]), commasInvade]).strip()))

        
    


        # Getting all the earthquake data from the page. I'm trying to make it as vague as possible for reusuability. 
        quakeInfo = {

            #Getting the day, year, month stats.
            'counts'     :  "\n".join(response.xpath("//div[contains(@class, 'col col-lg-4 col-md-6 col-sm-12 col-12')]//li/text()").extract()),
            #Getting the strongest Earthquakes stats.
            'strengths'  :  re.sub('\s+', ' ', "\n".join(response.xpath("//div[contains(@class, 'col col-lg-5 col-md-6 col-sm-12 col-12')]//li//text()").extract())),
            # Grabbing a list of Magnitudes for tallying.
            'magnitudes' : [re.findall("\d\.\d+", item)[0] for item in response.xpath("//div[contains(@class, 'quake-info-container')]//span[contains(@class, 'text-')]//text()").extract()],
            # Grabbing a raw list of quakes for processing to create things like the labels for graphs.
            'rawList'    : scrubbedQuakes

        }

        
        
        yield quakeInfo
