from __future__ import unicode_literals

""" This is the module file for an app that tracks Earthquakes in Japan.
    It uses BeautifulSoup to parse HTML and scrape data from earthquaketrack.com. It then checks for earthquakes and
    displays the data in a GUI via PyQt5.
"""

""" Written By: Tom Mullins
    Version: 0.75
    Modified: 11/18/22
"""
"""* Changelog:
   * V 0.5. The initial completed library, with two modules.
   * V 0.55. Formatting error fixes. Optimization of scraping, getting whole sections instead of just lines. Addition
     of an about section in the menu.
   * V 0.60 : Minor formatting fixes, correcting spelling errors in the scraped strings.
"""

import requests, bs4
import time, os
from datetime import date
from dateutil import parser
import re
from os.path import basename

dateToday = date.today()
global quakeSite
quakeSite = requests.get('https://www.earthquaketrack.com/p/japan/recent')

# The function that gets the earthquake count for Japan.

def japanQuakes():

    quakeSite.raise_for_status()
    # Now the website is loaded. Now let's parse this fucker.

    #print("Japan has had:\n")
    quakeSoup = bs4.BeautifulSoup(quakeSite.text, "html.parser")
    quakeData = quakeSoup.find_all(class_="col col-lg-4 col-md-6 col-sm-12 col-12")
    quakeSelect = quakeData[0].getText()
    quakeString = str(quakeSelect)                            # Slicing and stripping the data for formatting.
    strippedCount = re.sub( '\s+', ' ', quakeString).strip()

    # Making the string properly formatted by replacing some parts.

    countReplaced = strippedCount.replace('had: ', 'had: \n\n')
    countReplaced2 = countReplaced.replace('hours ', 'hours \n')
    countReplaced3 = countReplaced2.replace('days ', 'days \n')
    countReplaced4 = countReplaced3.replace(') ', ') \n\n')


    # Creating a global List so it can be used by the Main Script

    global quakeList
    quakeList = [countReplaced4]
    return

def quakeStrengths():

    strengthSoup = bs4.BeautifulSoup(quakeSite.text, "html.parser")
    testStrength = strengthSoup.find_all(class_="col col-lg-5 col-md-6 col-sm-12 col-12")

    # Getting each individual line of earthquake strength data

    testData = testStrength[0].getText()
    testString = str(testData)                                 # Convert the HTML object to a string we can work with
    strippedData = re.sub( '\s+', ' ', testString).strip()     # Stripping the excess spaces from the strings
    strengthReplaced = strippedData.replace('this ', '\nthis ')
    strengthReplaced2 = strengthReplaced.replace('Japan: ', 'Japan: \n\n')
    strengthReplaced3 = strengthReplaced2.replace('earthquake', 'earthquakes')


    # Creating a Global list so that it may be used by the main script

    global strengthList
    strengthList = [strengthReplaced3]
    return

# The function for the opening line of JapanQuakes.

def mostRecent():

    recentSoup = bs4.BeautifulSoup(quakeSite.text, "html.parser")
    recentData = recentSoup.find_all(class_="quake-info-container")

    japanRecent = str(recentData[0].getText())
    #print(japanRecent)

    japanrecentlyStripped = re.sub( '\s+', ' ', "2022".join(japanRecent.split("2022", 2)[:2])).strip()
    #print(japanrecentlyStripped)

    finalStrip = ".".join(japanrecentlyStripped.split(".", 2)[:2])[:-1]

    global recentItem
    recentItem = [finalStrip]
    return
#---------------------------------------------------------------------------------------------------------------------
# Functions for the Asia tab.
#---------------------------------------------------------------------------------------------------------------------

global asiarecentSite
asiarecentSite = requests.get('https://earthquaketrack.com/v/asia/recent')

# the function for the opening line of the Asia tab. same as mostRecent()

def mostasiaRecent():

    asiarecentSite.raise_for_status()

    asiarecentSoup = bs4.BeautifulSoup(asiarecentSite.text, "html.parser")
    asiarecentData = asiarecentSoup.find_all(class_="quake-info-container")

    asiarecentItem = asiarecentData[0].getText()
    asiarecentString = str(asiarecentItem)
    asiarecentlyStripped = re.sub( '\s+', ' ', "2022".join(asiarecentString.split("2022", 2)[:2])).strip()
    finalStrip = ".".join(asiarecentlyStripped.split(".", 2)[:2])[:-1]
    global asiarecentList
    asiarecentList = [finalStrip]

    return

# The function for the earthquake counts for Asia

def asiaQuakes():


    #print("Japan has had:\n")
    asia_quakeSoup = bs4.BeautifulSoup(asiarecentSite.text, "html.parser")
    asia_quakeData = asia_quakeSoup.find_all(class_="col col-lg-4 col-md-6 col-sm-12 col-12")
    asia_quakeSelect = asia_quakeData[0].getText()
    asia_quakeString = str(asia_quakeSelect)                        # Slicing and stripping the data for formatting.
    asia_strippedCount = re.sub( '\s+', ' ', asia_quakeString).strip()

    # Making the string properly formatted by replacing some parts.

    asia_countReplaced = asia_strippedCount.replace('had: ', 'had: \n\n')
    asia_countReplaced2 = asia_countReplaced.replace('hours ', 'hours \n')
    asia_countReplaced3 = asia_countReplaced2.replace('days ', 'days \n')
    asia_countReplaced4 = asia_countReplaced3.replace(') ', ') \n\n')


    # Creating a global List so it can be used by the Main Script

    global asia_quakeList
    asia_quakeList = [asia_countReplaced4]
    return

# The function to retreive the magnitude data for asia.

def asiaStrengths():

    asia_strengthSoup = bs4.BeautifulSoup(asiarecentSite.text, "html.parser")
    asia_testStrength = asia_strengthSoup.find_all(class_="col col-lg-5 col-md-6 col-sm-12 col-12")

    # Getting each individual line of earthquake strength data

    asia_testData = asia_testStrength[0].getText()
    asia_testString = str(asia_testData)                        # Convert the HTML object to a string we can work with
    asia_strippedData = re.sub( '\s+', ' ', asia_testString).strip()    # Stripping the excess spaces from the strings

    asia_strengthReplaced = asia_strippedData.replace('this', '\nthis')
    asia_strengthReplaced2 = asia_strengthReplaced.replace('Asia: ', 'Asia: \n\n')
    asia_strengthReplaced3 = asia_strengthReplaced2.replace('earthquake', 'earthquakes')


    # Creating a Global list so that it may be used by the main script
    #print(asia_testStrength)

    global asia_strengthList
    asia_strengthList = [asia_strengthReplaced3]
    return

#==========================================================================================================
# Functions for the News Tab.
#==========================================================================================================

# The function to get Tsunami warning data. Scrapes data from  The Japan Meteology Agency website.
def getTsunami():

    #print('Initializing getTsunami... \n')

    get_tsunamiSite = requests.get('http://www.jma.go.jp/en/tsunami/#explain')
    #print('Checking Status...\n')
    get_tsunamiSite.raise_for_status()

    # Parsing for img data.
    imgList = []
    tsunamiSoup = bs4.BeautifulSoup(get_tsunamiSite.text, "html.parser")

    for link in tsunamiSoup.select("#info > img:nth-of-type(1)"):
        lnk = link["src"]
        lnk2 = "http://www.jma.go.jp/en/tsunami/"
        lnk3 = lnk2 + lnk

        with open('tsunami.png',"wb") as f:
            f.write(requests.get(lnk3).content)


        #print(lnk3)




#asiaStrengths()
