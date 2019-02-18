from __future__ import unicode_literals

"""
    This is the module for Japan Quakes that scrapes the data necessary data for building graphs in the gui.
    It uses beautiful soup 4 and requests to do so. The data is then used in building the actual graph in
    the main file.

"""

""" Written By: Tom Mullins
    Created:  03/21/2018
    Modified: 10/20/2018
"""

import requests, bs4
import time, os
from datetime import date
from dateutil import parser
import re
from os.path import basename
import japanEarthquaker


# The function that pulls the data for the first graph in Japan Quakes.
# It converts the string data into usable Floats and get's the locations of the quakes.
def get_six():

    recentSite = requests.get('https://www.earthquaketrack.com/p/japan/recent')
    recentSite.raise_for_status()

    recentSoup = bs4.BeautifulSoup(recentSite.text, "html.parser")
    recentData = recentSoup.find_all(class_="text-warning")
    global recentJap
    recentJap = [] # List to be filled with the text form of data from site
    for x in recentData:
        recentJap.append(x.text)

    #print(recentJap[2])                       # TESTING

    recentSix = []
    recentSix.append(recentJap[3])
    recentSix.append(recentJap[5])
    recentSix.append(recentJap[7])
    recentSix.append(recentJap[9])             # building the list with the wanted magnitudes
    recentSix.append(recentJap[11])            # Have to skip every other item because the scraper
    recentSix.append(recentJap[13])            # returns doubles of the items for some reason.

    #print(recentSix)                          # TESTING

    slicedSix = []                             # A List to be filled with slices of the recentSix items
    for i in recentSix:
        slicedSix.append(i[0:3])               # slicing down to the magnitude

    #print(slicedSix)                          # TESTING
    global floatSix
    floatSix = []
    for i in slicedSix:
        floatSix.append(float(i))              # Converting the items from recentSix to float types and
                                               # building the global list for the graph
    #print(floatSix)

    # Now to get the data for the location labels on the graph
    locationData = recentSoup.find_all(class_="quiet row")
    global locateJap
    locateJap = []
    for x in locationData:
        locateJap.append(x.text)

    locationStrings = []
    for i in locateJap:
        locationStrings.append(str(i))        # Converting to strings

    #print(locationStrings)                   # TESTING
    global stripLocation
    stripLocation = []
    for i in locationStrings:
        stripLocation.append(re.sub( '\s+', ' ', i).strip())
    global finalLocation
    finalLocation = []
    for i in stripLocation:

        finalLocation.append(re.sub('^(.*depth)', '', i))       # removing everything before the location
    finalLocation2 = []
    for i in finalLocation:
        finalLocation2.append(i.replace(', Japan', ''))

    global sixLocations
    sixLocations = []
    sixLocations.append(finalLocation2[0])    # adding the first six items to the global list
    sixLocations.append(finalLocation2[1])
    sixLocations.append(finalLocation2[2])
    sixLocations.append(finalLocation2[3])
    sixLocations.append(finalLocation2[4])
    sixLocations.append(finalLocation2[5])

    #print(sixLocations) # TESTING
    return


# The function that gets and processes the data for the earthquake count by City graph
# it uses the recentJap list from get_six() to get the city names and count the quakes they have
def nihon_Graph():
    finalLocation.append('ah')
    counter = 0                 # Counter used in itering over the items in recentJap
    cityData = []

    # The function that takes counter and processes the data for adding to the cityData List
    def nihon_Count(y):
        quakeItem = finalLocation[y]
        cityCount = 0
        #city = re.sub('^(.*depth)', '', quakeItem)
        prefecture = re.sub('^.*?(?=,)', '', quakeItem)
        prefecture2 = re.sub('^.*?, ', '', prefecture)
        prefecture3 = re.sub(',.*', '', prefecture2)
        if prefecture3 not in cityData:
            #print(city)        # TESTING
            for x in finalLocation:
                if prefecture3 in x:
                    cityCount += 1
            #print(cityCount)             # Testing
            cityData.append(prefecture3)
            cityData.append(cityCount)
            #print(cityData)            # TESTING
        return
    while counter < len(finalLocation)-1:
        nihon_Count(counter)
        counter += 1
    #print(cityData)
    nameScrape = 0
    countScrape = 1
    global prefectureName
    prefectureName = []
    global prefectureCounts
    prefectureCounts = []
    # separating the prefecture names into their own list
    while nameScrape < len(cityData)-1:
        prefectureName.append(cityData[nameScrape])
        nameScrape += 2
    # separating the counts into their own list.
    while countScrape < len(cityData):
        prefectureCounts.append(cityData[countScrape])
        countScrape += 2
    #print(prefectureName)
    #print(prefectureCounts)
    return

#===========================================================================================
# Now we have functions for processing the earthquake Data for all of Asia
#===========================================================================================

# A function for getting the last six earthquakes in Asia and processing the
# data for visualization.
def get_asia_six():

    recentSite = requests.get('https://www.earthquaketrack.com/v/asia/recent')
    recentSite.raise_for_status()

    recentSoup = bs4.BeautifulSoup(recentSite.text, "html.parser")
    recentData = recentSoup.find_all(class_="text-warning")

    global recentAsia
    recentAsia = [] # List to be filled with the text form of data from site
    for x in recentData:
        recentAsia.append(x.text)

    # now we have to iterate through the recent Asia list to remove duplicates
    # of data and get just the six we need
    iteratorInt = 3
    recentSix = []
    while iteratorInt != 15:
        recentSix.append(recentAsia[iteratorInt])
        iteratorInt += 2

    #print(recentSix)                       # TESTING

    slicedSix = []                             # A List to be filled with slices of the recentSix items
    for i in recentSix:
        slicedSix.append(i[0:3])               # slicing down to the magnitude

    #print(slicedSix)                          # TESTING
    global floatSix
    floatSix = []
    for i in slicedSix:
        floatSix.append(float(i))              # Converting the items from recentSix to float types and
                                               # building the global list for the graph

    # Now to get the data for the location labels on the graph
    locationData = recentSoup.find_all(class_="quiet row")
    locateAsia = []
    for x in locationData:
        locateAsia.append(x.text)

    locationStrings = []
    for i in locateAsia:
        locationStrings.append(str(i))        # Converting to strings

    stripLocation = []
    for i in locationStrings:
        stripLocation.append(re.sub( '\s+', ' ', i).strip())

    global finalLocation
    finalLocation = []
    for i in stripLocation:
        finalLocation.append(re.sub('^(.*depth)', '', i))       # removing everything before the location

    # narrowing down the list to just the six we need
    iteratorInt = 0
    sixLocations = []
    while iteratorInt < 7:
        sixLocations.append(finalLocation[iteratorInt])
        iteratorInt += 1
    # Adding spaces after the commas
    global approvedSix
    approvedSix = []
    for i in sixLocations:
        approvedSix.append(re.sub(', ', ',\n', i))

# A function that tallies earthquakes by country of origin
def asia_Graph():
    finalLocation.append('Ah')
    iteratorInt = 0
    countryData = []

    def asia_tally(counter):

        quakeItem = finalLocation[counter]
        countryCount = 0
        #city = re.sub('^(.*depth)', '', quakeItem)
        country = re.sub('^.*?(?=,)', '', quakeItem)
        country2 = re.sub('^.*?, ', '', country)
        country3 = re.sub('.*, ', '', country2)
        if "Xizang" in country3:
            country3 = re.sub('Xizang.*$', '', country3)
            #country3 = re.sub('?.*?(?=Xizang)', '', country3)
            print(country3)

        if country3 not in countryData:
            #print(city)        # TESTING
            for x in finalLocation:
                if country3 in x:
                    countryCount += 1
            #print(cityCount)             # Testing
            countryData.append(country3)
            countryData.append(countryCount)
            #print(countryData)            # TESTING

        return

    while iteratorInt < len(finalLocation)-1:
        asia_tally(iteratorInt)
        iteratorInt += 1

    nameScrape = 0
    countScrape = 1
    global countryName
    countryName = []
    global countryCounts
    countryCounts = []
    # separating the prefecture names into their own list
    while nameScrape < len(countryData)-1:
        if "Xizang" in countryData[nameScrape]:
            countryData[nameScrape] = "Tibet"
        if "Taiwan" in countryData[nameScrape]:
            countryData[nameScrape] = "Taiwan"
        countryName.append(countryData[nameScrape])
        nameScrape += 2
    # separating the counts into their own list.
    while countScrape < len(countryData):
        countryCounts.append(countryData[countScrape])
        countScrape += 2
    #print(countryName)
    #print(countryCounts)
    return

#get_six()
#nihon_Graph()
#get_asia_six()
#asia_Graph()
