from __future__ import unicode_literals

"""
    This is the module for Japan Quakes that scrapes the data necessary data for building graphs in the gui.
    It uses beautiful soup 4 and requests to do so. The data is then used in building the actual graph in
    the main file.

"""

""" Written By: Tom Mullins
    Created:  03/21/2018
    Modified: 1/26/2023
"""

import time, os
from datetime import date
from dateutil import parser
import re
from os.path import basename
import japanEarthquaker

# The function that pulls the data for the first graph in Japan Quakes.
# It converts the string data into usable Floats and get's the locations of the quakes.
def get_six():
    
    # Getting the dictionary of data from the list supplied by the pipeline.
    japansData = dict(japanEarthquaker.quakeData[0])
    quakeList = japansData['rawList']
    quakeStrengths = japansData['magnitudes']

    # Converting the strings to floats 
    global strengthFloats
    strengthFloats = []
    for item in quakeStrengths:
        strengthFloats.append(float(item))

    # Removing the date and time
    global finalLocation
    finalLocation = []
    for i in quakeList:
        finalLocation.append(re.sub('^(.*UTC)', '', i))       # removing everything before the location
    
    # Removing the country because we know it's Japan
    finalLocation2 = []
    for i in finalLocation:
        finalLocation2.append("".join(i.split("20", 2)[:2]).replace(', Japan', ''))

    global sixLocations
    sixLocations = []
    sixLocations.append(("".join(finalLocation2[0].split(".", 2)[:1]).replace(', ', ',\n')))    # adding the first six items to the global list
    sixLocations.append(("".join(finalLocation2[1].split(".", 2)[:1]).replace(', ', ',\n')))
    sixLocations.append(("".join(finalLocation2[2].split(".", 2)[:1]).replace(', ', ',\n')))
    sixLocations.append(("".join(finalLocation2[3].split(".", 2)[:1]).replace(', ', ',\n')))
    sixLocations.append(("".join(finalLocation2[4].split(".", 2)[:1]).replace(', ', ',\n')))
    sixLocations.append(("".join(finalLocation2[5].split(".", 2)[:1]).replace(', ', ',\n')))

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

        # Stripping the location down to just the prefecture.  
        prefecture = re.sub('^.*?(?=,)', '', quakeItem)
        prefecture2 = re.sub('^.*?, ', '', prefecture)
        prefecture3 = re.sub(',.*', '', prefecture2)

        if prefecture3 not in cityData:

            for x in finalLocation:
                if prefecture3 in x:
                    cityCount += 1
    
            cityData.append(prefecture3)
            cityData.append(cityCount)

        return
    while counter < len(finalLocation)-1:
        nihon_Count(counter)
        counter += 1


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
    return

#===========================================================================================
# Now we have functions for processing the earthquake Data for all of Asia
#===========================================================================================

# A function for getting the last six earthquakes in Asia and processing the
# data for visualization.
def get_asia_six():

    asiasData = dict(japanEarthquaker.quakeData[1])
    quakeList = asiasData['rawList']
    quakeStrengths = asiasData['magnitudes']

    # Converting the strings to floats 
    global asiaFloats
    asiaFloats = []
    for item in quakeStrengths:
        asiaFloats.append(float(item))


    global finalLocation
    finalLocation = []
    for i in quakeList:
        finalLocation.append(re.sub('^(.*UTC)', '', i))       # removing everything before the location

    # narrowing down the list to just the six we need
    iteratorInt = 0
    sixLocations = []
    while iteratorInt < 7:
        sixLocations.append(("".join(finalLocation[iteratorInt].split(".", 2)[:1])))
        iteratorInt += 1
    # Adding spaces after the commas
    global approvedSix
    approvedSix = []
    for i in sixLocations:
        approvedSix.append(re.sub(', ', ',\n', i))

    #print(sixLocations)
# A function that tallies earthquakes by country of origin
def asia_Graph():

    iteratorInt = 0
    countryData = []


    def asia_tally(counter):

        quakeItem = finalLocation[counter]
        countryCount = 0
        country = re.sub('^.*?(?=,)', '', "".join(quakeItem.split(".", 2)[:1]))
        country2 = re.sub('^.*?, ', '', country)
        country3 = re.sub('.*, ', '', country2)
    
        if "Xizang" in country3:
            country3 = re.sub('Xizang.*$', '', country3)

        if country3 not in countryData:
            if "-" not in country3:
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

    return

#get_six()
#nihon_Graph()
#get_asia_six()
#asia_Graph()
