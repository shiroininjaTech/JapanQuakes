#! /usr/bin/env python3

"""
   This is the source file for the Japanese Earthquake tracking app for the Linux Desktop. It scrapes data from
   earthquaketrack.com and displays it in an interactive GUI using beautiful soup and PyQt5.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.75
   * Date Modified: 11/29/22
"""
"""
   * Changelog:
   *
   * V 0.50: The first functional GUI working with 2 buttons and an exit option in a cascading menu.
   * V 0.55: Formatting error fixes. Optimization of scraping, getting whole sections instead of just lines. Addition
     of an about section in the menu.
   * V 0.60: A complete rebuild of the GUI, using PyQt5, involving a complete re-writing. This brought multiple appearence changes
     and reformatting. Buttons were also removed and replaced with framed QLabels.
   * V 0.65: Minor chages to file menu labels, changes to window positions, added a reload option in the Menu that deletes and reloads widgets.
   * V 0.70: Added Theme settings, using astroThemes module and .config files to allow saveable theme settings by the user. Also added the Japan Data tab, containing
     two graphs, one showing the strengths of the last six earthquakes and the other showing total earthquake counts by prefecture.
"""


# Imports needed for PyQt5
import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time, os
from datetime import date
import calendar
from dateutil import parser
import sys
from configparser import SafeConfigParser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as mtick
import numpy as np
import astroThemes
import japanGraph
import japanEarthquaker

# Setting up the GUI window class and methods.

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        #self.setGeometry(0, 0, 0, 0)
        self.setWindowTitle('Japan Quakes')
        self.setWindowIcon(QIcon(os.path.expanduser("~/.JapanQuakes/japan-flag.png")))
        self.setStyleSheet("QMainWindow { background-color: White; color: Black; }")
        #qtRectangle = self.frameGeometry()
        #centerPoint = QDesktopWidget().availableGeometry().center()
        #qtRectangle.moveCenter(centerPoint)
        #self.move(qtRectangle.center())


        self.initUI()
        #self.show()


    # The the method to setup the window.
    def initUI(self):

        # The about button function
        def clickMethod(self):
            aboutBox = QMessageBox()
            aboutBox.setIcon(QMessageBox.Question)
            aboutBox.setWindowTitle("About Japan Quakes")
            aboutBox.setText("Version 0.75 TESTING\nCreated By: Solid Ground Technologies")
            aboutBox.exec_()

        # The functions to change the themes in the settings menu
        def Default():
            themeConfig.set('theme', 'key1', 'default')

            with open(os.path.expanduser("~/.JapanQuakes/config.ini"), 'w') as f:
                themeConfig.write(f)


        def Spacex():
            themeConfig.set('theme', 'key1', 'spaceX')

            with open(os.path.expanduser("~/.JapanQuakes/config.ini"), 'w') as f:
                themeConfig.write(f)

        def japan():
            themeConfig.set('theme', 'key1', 'japan')

            with open(os.path.expanduser("~/.JapanQuakes/config.ini"), 'w') as f:
                themeConfig.write(f)

        # Set the central widget
        central_widget = QWidget(self)          # Create a central widget
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(self)         # Create a QGridLayout
        central_widget.setLayout(grid_layout)   # Set Layout to central widget

        # Setting fonts
        fontVar = QFont("Apple Garamond Regular", 15)        # Create a QFont instance
        fontVar.setBold(True)

        smallerFont = QFont()                                # A smaller Font
        smallerFont.setBold(True)

        #=================================================================================================
        # Setting up the theme config file
        #=================================================================================================

        # initialize
        # Checking if the config file is present, and making one if it isnt. This prevents the configuration from being over written.

        if not os.path.isfile(os.path.expanduser("~/.JapanQuakes/config.ini")):
            themeConfig = SafeConfigParser()
            themeConfig.read(os.path.expanduser("~/.JapanQuakes/config.ini"))
            themeConfig.add_section('theme')
            themeConfig.set('theme', 'key1', 'default')
            themeSelected = themeConfig.get('theme', 'key1')

            with open(os.path.expanduser("~/.JapanQuakes/config.ini"), 'w') as f:
                themeConfig.write(f)
        elif os.path.isfile(os.path.expanduser("~/.JapanQuakes/config.ini")):
            themeConfig = SafeConfigParser()
            themeConfig.read(os.path.expanduser("~/.JapanQuakes/config.ini"))
            themeSelected = themeConfig.get('theme', 'key1')
        #=================================================================================================
        # Creating tabs in the UI
        #=================================================================================================

        # Initilizing tabs
        self.tabs = QTabWidget()

        self.japanTab = QWidget()
        self.asiaTab = QWidget()

        if themeSelected == 'default':
            astroThemes.defaultTabs(self.japanTab, self.asiaTab, self.tabs)     # TESTING the function for the tab themes
        if themeSelected == 'spaceX':
            astroThemes.spacexTabs(self.japanTab, self.asiaTab, self.tabs)
        if themeSelected == 'japan':
            astroThemes.japanTabs(self.japanTab, self.asiaTab, self.tabs)

        self.tabs.addTab(self.japanTab, "Japan")
        self.tabs.addTab(self.asiaTab, "Asia")

        #=====================================================================================================================
        # The functions used to build the UI
        #=====================================================================================================================

        # A function for building frames in the UI
        # takes the container the frame is to be added to as home
        # takes x axis coordinate as x
        # takes y axis coordinate as y
        # set the width with width
        def frameBuilder(home, x, y, width):

            self.frame = QFrame()
            self.frame.setFrameShape(QFrame.WinPanel)
            # Reading which theme is selected and applying it to the frame
            if themeSelected == 'spaceX':
                astroThemes.spacexFrame(self.frame)
            if themeSelected == 'japan':
                astroThemes.japanFrame(self.frame)
            home.addWidget(self.frame, x, y)
            global frameLayout
            frameLayout = QHBoxLayout()
            self.frame.setLayout(frameLayout)
            frameLayout.setSpacing(0)
            home.setColumnMinimumWidth(1, width)


        # A function for building Graph frames in the UI
        # takes the container the frame is to be added to as home
        # takes x axis coordinate as x
        # takes y axis coordinate as y
        # set the width with width
        def gframeBuilder(home, x, y, width):

            self.frame = QFrame()
            self.frame.setFrameShape(QFrame.WinPanel)
            # Reading which theme is selected and applying it to the frame
            if themeSelected == 'spaceX':
                astroThemes.spacexFrame(self.frame)
            if themeSelected == 'japan':
                astroThemes.japanFrame(self.frame)
            home.addWidget(self.frame, x, y)
            global frameLayout
            frameLayout = QGridLayout()
            self.frame.setLayout(frameLayout)
            frameLayout.setSpacing(0)
            home.setColumnMinimumWidth(1, width)

        # A function for building labels in the UI
        # Gets a message variable as message
        # Gets the container it is to be placed in as home
        # (width) is the Maximum Width the label is to be
        def labelMaker(message, home, width):

            self.label = QLabel(message)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setFont(smallerFont)
            self.label.adjustSize()
            self.label.setWordWrap(True)
            self.label.setMaximumWidth(width)
            home.addWidget(self.label)

        # A function for creating scroll objects
        # gets the tab/location the scroll is to be inserted as location
        # gets the x and y coordinates as x and y
        global scroll
        def scrollBuilder(location, x, y):
            global scroll
            scroll = QScrollArea(self)

            # Creating the style sheet for the scroll bar colors.

            if themeSelected == 'default':
                astroThemes.defaultScroll(scroll)    # TESTING the function for the default scroll theme
            if themeSelected == 'spaceX':
                astroThemes.spacexScroll(scroll)
            if themeSelected == 'japan':
                astroThemes.japanScroll(scroll)
            location.addWidget(scroll, x, y)
            scroll.setWidgetResizable(True)
            #scroll.setMinimumHeight(50)
            scrollContent = QWidget(scroll)
            scroll.layout = QGridLayout(scrollContent)
            scrollContent.setLayout(scroll.layout)

            scroll.setWidget(scrollContent)

        # A function that builds headers
        # (message) is the message string
        # (x) is the first position variable
        # (y) is the second position variable
        # (home) is the layout that the label is to be added to
        # (height) is the fixed height for the header
        def headerBuild(message, x, y, home, height):

            self.header = QLabel(message, self)
            self.header.setAlignment(QtCore.Qt.AlignCenter)
            self.header.setFixedHeight(height)
            self.header.setWordWrap(True)
            self.header.setFont(fontVar)
            #self.greeting.setStyleSheet("QLabel{ background-color: white; color: black; }")
            home.addWidget(self.header, x, y)

        # A function that adds verticle margins to layouts
        # (size) as size deminsions
        # (home) as the container the spacers are to go in
        # (firstCoord) as the first spacer's Location
        # (secondCoord) as the second spacer's Location
        def vert_Spacer(size, home, a, b):
            verticalSpacer = QSpacerItem(size, size, QSizePolicy.Maximum, QSizePolicy.Expanding)
            home.addItem(verticalSpacer, 2, a)
            home.addItem(verticalSpacer, 2, b)

        # A function to add verticle margins to frame objects
        def interior_Spacer(size, home):
            intSpacer = QSpacerItem(size, size, QSizePolicy.Maximum, QSizePolicy.Expanding)
            home.addItem(intSpacer)
        #=====================================================================================================================
        # The Japan Tab.
        #=====================================================================================================================

        # setting the layout for the Tab
        self.japanTab.layout = QGridLayout()
        # A welcome message to the user.
        jGreeting = "Welcome To Japan Quakes!"
        headerBuild(jGreeting, 0, 0, self.japanTab.layout, 30)

        # Adding a most recent quake message
        #
        # A function to setup the most recent quake in japan message.
        def get_recent():
            japanEarthquaker.mostRecent()
            japanEarthquaker.recentItem.append('Ah')
            recentMessage = "The Most Recent Quake Was At: \n %s" % japanEarthquaker.recentItem[0]
            self.mostRecent = QLabel(recentMessage, self)
            self.mostRecent.setAlignment(QtCore.Qt.AlignCenter)
            self.mostRecent.resize(30, 30)
            self.mostRecent.setWordWrap(True)
            self.japanTab.layout.addWidget(self.mostRecent, 1 ,0)

        # Creating a frame for japanese counts.
        scrollBuilder(self.japanTab.layout, 2, 0)
        frameBuilder(scroll.layout, 0, 1, 600)
        interior_Spacer(200, frameLayout)
        # Header for japanese quake counts
        jcountMessage = "Earthquake Counts for Japan"
        labelMaker(jcountMessage, frameLayout, 300)

        # A function for getting the quake count for Japan
        def japan_count():
            japanEarthquaker.japanQuakes()
            japanEarthquaker.quakeList.append('argh')
            message1 = "\n{} \n".format(japanEarthquaker.quakeList[0])
            labelMaker(message1, frameLayout, 300)

        # japan_count() must be run before japan_strengths() or it will appear
        # in the strengths frame
        japan_count()
        interior_Spacer(200, frameLayout)
        # Creating a frame for japanese Magnitudes.
        frameBuilder(scroll.layout, 1, 1, 600)
        interior_Spacer(200, frameLayout)

        #Header for Japanese Magnitudes
        jstrengthMessage = "Strongest Earthquakes by Magnitude For Japan"
        labelMaker(jstrengthMessage, frameLayout, 350)

        # A function to get the earthquake strengths from japanEarthquaker
        def japan_strengths():
            japanEarthquaker.quakeStrengths()
            japanEarthquaker.strengthList.append('yo')
            message2 = "\n {} \n".format(japanEarthquaker.strengthList[0],)
            labelMaker(message2, frameLayout, 350)

        get_recent()

        # adding a verticle spacer
        vert_Spacer(225, scroll.layout, 0, 3)
        japan_strengths()
        interior_Spacer(100, frameLayout)

        gframeBuilder(scroll.layout, 2, 1, 600)

        #self.jgraphTab.layout = QGridLayout()

        japanGraph.get_six()
        japanGraph.floatSix.append('Ah')
        japanGraph.sixLocations.append('Ah')
        # building the widget for the graph
        self.figure = plt.figure(figsize=(10,5))
        self.canvas = FigureCanvas(self.figure)
        frameLayout.addWidget(self.canvas, 0, 0)

        # x-coordinates
        xItems = 6
        ind = np.arange(xItems)

        # heights of bars, also the amounts to plot.
        height = [japanGraph.floatSix[0], japanGraph.floatSix[1], japanGraph.floatSix[2], japanGraph.floatSix[3], japanGraph.floatSix[4], japanGraph.floatSix[5]]
        p1 = plt.bar(ind, height) #setting the plot

        # The function that builds the graph and plots the data to it.
        def plot():
            #plt.cla()
            #axes = self.figure.add_plot(211)
            plt.ylabel('Strength (By Magnitude)')
            plt.xlabel('Earthquake Locations')
            plt.title('Japan\'s Last Six EarthQuakes Over 4 Magnitude')
            plt.xticks(ind, (japanGraph.sixLocations[0], japanGraph.sixLocations[1], japanGraph.sixLocations[2], japanGraph.sixLocations[3], japanGraph.sixLocations[4], japanGraph.sixLocations[5]))
            #plt.yticks(height)
            #fig, ax = plt.subplots()
            #plt.yticks.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
            plt.ylim(3.0,8.0)
            #plt.yticks(np.arange(25))
            for a,b in zip(ind, height):
                plt.text(a, b, str(b), ha='center')

            self.canvas.draw()

        plot()

        # The second graph, showing earthquake counts by prefecture.
        #=============================================================================================

        japanGraph.nihon_Graph()
        # building the widget for the graph
        self.figure2 = plt.figure(figsize=(10,5))
        self.canvas2 = FigureCanvas(self.figure2)
        frameLayout.addWidget(self.canvas2, 1, 0)

        # x-coordinates
        xItems2 = len(japanGraph.prefectureName)
        ind2 = np.arange(xItems2)

        # heights of bars, also the amounts to plot.
        height2 = japanGraph.prefectureCounts
        p2 = plt.bar(ind2, height2) #setting the plot

        # The function that builds the graph and plots the data to it.
        def plot2():

            plt.ylabel('Total Earthquakes')
            plt.xlabel('Prefectures')
            plt.title('Earthquake Counts By Prefecture for Last 30 Quakes')
            plt.xticks(ind2, (japanGraph.prefectureName), fontsize = 8)
            plt.yticks(np.arange(15))
            for a,b in zip(ind2, height2):
                plt.text(a, b, str(b), fontdict=dict(fontsize=8, ha='center', va='bottom'))

            self.canvas2.draw()

        plot2()

        self.japanTab.setLayout(self.japanTab.layout)

        #======================================================================================================
        # The Asia tab
        #======================================================================================================

        self.asiaTab.layout = QGridLayout()

        # Getting the most recent quake in asia.
        def get_asia_recent():
                japanEarthquaker.mostasiaRecent()
                japanEarthquaker.asiarecentList.append('Ah')
                asiarecentMessage = "The Most Recent Quake In Asia Was: \n %s" % japanEarthquaker.asiarecentList[0]
                self.asiaRecent = QLabel(asiarecentMessage, self)
                self.asiaRecent.setAlignment(QtCore.Qt.AlignCenter)
                #self.asiaRecent.resize(30, 30)
                self.asiaTab.layout.addWidget(self.asiaRecent, 0 ,0)


        # Creating a frame for Asian counts..
        scrollBuilder(self.asiaTab.layout, 1, 0)
        frameBuilder(scroll.layout, 0, 1, 600)
        interior_Spacer(200, frameLayout)
        # Header for Asian quake counts
        acountMessage = "Earthquake Counts for Asia"
        labelMaker(acountMessage, frameLayout, 300)

        # Function for creating the recent asian quakes label
        def asia_get_quakes():
            japanEarthquaker.asiaQuakes()
            japanEarthquaker.asia_quakeList.append('argh')
            asia_message1 = "\n{} \n".format(japanEarthquaker.asia_quakeList[0])
            labelMaker(asia_message1, frameLayout, 300)

        asia_get_quakes()
        interior_Spacer(200, frameLayout)

        # Creating a frame for Asian Magnitudes.
        frameBuilder(scroll.layout, 1, 1, 600)
        interior_Spacer(200, frameLayout)

        #Header for Asian Magnitudes
        amagMessage = "Strongest Earthquakes by Magnitude For Asia"
        labelMaker(amagMessage, frameLayout, 400)

        # The function to create Asian Magnitude record label
        def asia_get_strengths():
            japanEarthquaker.asiaStrengths()
            japanEarthquaker.asia_strengthList.append('argh')
            asia_message2 = "\n {} \n".format(japanEarthquaker.asia_strengthList[0])
            labelMaker(asia_message2, frameLayout, 400)

        get_asia_recent()
        vert_Spacer(225, scroll.layout, 0, 2)
        asia_get_strengths()
        interior_Spacer(200, frameLayout)

        gframeBuilder(scroll.layout, 2, 1, 600)

        #self.jgraphTab.layout = QGridLayout()

        japanGraph.get_asia_six()
        japanGraph.floatSix.append('Ah')
        japanGraph.approvedSix.append('Ah')
        # building the widget for the graph
        self.figure = plt.figure(figsize=(10,5))
        self.canvas = FigureCanvas(self.figure)
        frameLayout.addWidget(self.canvas, 0, 0)

        # x-coordinates
        xItems = 6
        ind = np.arange(xItems)

        # heights of bars, also the amounts to plot.
        height = [japanGraph.floatSix[0], japanGraph.floatSix[1], japanGraph.floatSix[2], japanGraph.floatSix[3], japanGraph.floatSix[4], japanGraph.floatSix[5]]
        p1 = plt.bar(ind, height) #setting the plot

        # The function that builds the graph and plots the data to it.
        def plot():
            #plt.cla()
            #axes = self.figure.add_plot(211)
            plt.ylabel('Strength (By Magnitude)')
            plt.xlabel('Earthquake Locations')
            plt.title('Asia\'s Last Six EarthQuakes Over 4 Magnitude')
            plt.xticks(ind, (japanGraph.approvedSix[0], japanGraph.approvedSix[1], japanGraph.approvedSix[2], japanGraph.approvedSix[3], japanGraph.approvedSix[4], japanGraph.approvedSix[5]), fontsize = 8)
            #plt.yticks(height)
            #fig, ax = plt.subplots()
            #plt.yticks.set_major_formatter(FormatStrFormatter('%.2f'))
            plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
            plt.ylim(3.0,8.0)
            #plt.yticks(np.arange(25))
            for a,b in zip(ind, height):
                plt.text(a, b, str(b), ha='center')

            self.canvas.draw()

        plot()

        # The second graph, showing earthquake counts by Country/Region.
        #=============================================================================================

        japanGraph.asia_Graph()
        # building the widget for the graph
        self.figure2 = plt.figure(figsize=(10,5))
        self.canvas2 = FigureCanvas(self.figure2)
        frameLayout.addWidget(self.canvas2, 1, 0)

        # x-coordinates
        xItems2 = len(japanGraph.countryName)
        ind2 = np.arange(xItems2)

        # heights of bars, also the amounts to plot.
        height2 = japanGraph.countryCounts
        p2 = plt.bar(ind2, height2) #setting the plot

        # The function that builds the graph and plots the data to it.
        def plot2():
            #plt.cla()
            #axes = self.figure.add_plot(211)
            plt.ylabel('Total Earthquakes')
            plt.xlabel('Countries')
            plt.title('Earthquake Counts By Country for Last 30 Quakes')
            plt.xticks(ind2, (japanGraph.countryName), fontsize = 8)
            #plt.yticks(height)
            #fig, ax = plt.subplots()
            #plt.yticks.set_major_formatter(FormatStrFormatter('%.2f'))
            #plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
            #plt.ylim(3.0,8.0)
            plt.yticks(np.arange(15))
            for a,b in zip(ind2, height2):
                plt.text(a, b, str(b), ha='center')

            self.canvas2.draw()

        plot2()


        self.asiaTab.setLayout(self.asiaTab.layout)


        grid_layout.addWidget(self.tabs)


        #=============================================================================================
        # Adding options to the menubar
        #=============================================================================================

        iconList = [os.path.expanduser("~/.JapanQuakes/exit.png"), os.path.expanduser("~/.JapanQuakes/about.png"), os.path.expanduser("~/.JapanQuakes/refresh.png")]

        # The menu item builder
        # takes an image from iconLst as image
        # toggles icons off with iconToggle
        # takes the tool tip as statusTip
        # gets the item's name as menuName
        # method is the function to be run when clicked
        def buildMenuItemAction(image, iconToggle, statusTip, menuName, method):

            if iconToggle is True:
                item = QAction(QIcon(image), menuName, self)
                item.setStatusTip(statusTip)
                item.triggered.connect(method)
                return item
            else:
                item = QAction(menuName, self)
                item.setStatusTip(statusTip)
                item.triggered.connect(method)
                return item

        # Adding a quit option to the menubar.

        toggler = True
        exitAct = buildMenuItemAction(iconList[0], toggler, "Exit Application", "&Exit", qApp.quit)
        aboutAct = buildMenuItemAction(iconList[1], toggler, "Build Information", "&About", clickMethod)
        toggler = False                                                                                                        # The rest of the options have no icons
        defaultAct = buildMenuItemAction(iconList[0], toggler, "The Default Theme", "&Default", Default)                       # Default Theme
        spacexAct = buildMenuItemAction(iconList[0], toggler, "A Theme based On SpaceX", "&SpaceX", Spacex)                    # SpaceX Theme
        japanAct = buildMenuItemAction(iconList[0], toggler, "A Theme based On Japan's National Flag", "&Japan", japan)        # Japan Theme

        # The function for the Refresh menu option
        def refreshMethod():
            #self.update()
            #QApplication.processEvents()
            self.asiaMags.deleteLater()
            self.asiaCounts.deleteLater()
            self.asiaRecent.deleteLater()
            self.mostRecent.deleteLater()
            self.japanMags.deleteLater()
            self.japanCounts.deleteLater()
            get_asia_recent()
            asia_get_quakes()
            asia_get_strengths()
            get_recent()
            japan_count()
            japan_strengths()

        # Adding the Refresh option to the menu. Refreshes all the widgets.
        refreshAct = QAction(QIcon(os.path.expanduser("~/.JapanQuakes/refresh.png")), '&Refresh', self)
        refreshAct.setStatusTip('Refreshes Earthquake Data')
        refreshAct.triggered.connect(refreshMethod)

        self.statusBar()
        self.showMaximized()


        # Adding a menubar.
        menubar = self.menuBar()
        if themeSelected == 'default':
            astroThemes.defaultMenu(menubar)    # TESTING the function for the default menubar theme
        if themeSelected == 'spaceX':
            astroThemes.spacexMenu(menubar)
        if themeSelected == 'japan':
            astroThemes.japanMenu(menubar)
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(refreshAct)
        fileMenu.addAction(aboutAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        # Adding a Settings menu to the menu bar.
        settingsMenu = menubar.addMenu('&Settings')
        themeMenu = settingsMenu.addMenu('&Themes')
        themeMenu.addAction(defaultAct)
        themeMenu.addAction(spacexAct)
        themeMenu.addAction(japanAct)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
