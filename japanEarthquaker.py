from __future__ import unicode_literals

""" This is the module file for an app that tracks Earthquakes in Japan.
    It uses BeautifulSoup to parse HTML and scrape data from earthquaketrack.com. It then checks for earthquakes and
    displays the data in a GUI via PyQt5.
"""

""" Written By: Tom Mullins
    Version: 0.85
    Modified: 1/27/23
"""
"""* Changelog:
   * V 0.5. The initial completed library, with two modules.
   * V 0.55. Formatting error fixes. Optimization of scraping, getting whole sections instead of just lines. Addition
     of an about section in the menu.
   * V 0.60 : Minor formatting fixes, correcting spelling errors in the scraped strings.
   * V 0.85 : Japan Quakes was rewritten completely to use Scrapy instead of Bs4, eliminating the need for all the functions contained
     in this module. This module now only holds the data collection pipeline for the Scrapy spider and may be completely removed in the future.    
"""

global quakeData
quakeData = []

# pipeline to fill the items list
class QuakeCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        quakeData.append(item)
