"""
  * astroGraph.py is a module containing functions pertaining to the setting of color themes in ShiroiNinja desktop apps.
  * It is originally developed for AstroNinja. It uses shelf Files created in the main app to determine which color themes
  * to set.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.75
   * Date Created:  01/23/18
   * Date Modified: 10/19/18
"""
"""
   * Changelog:
   * V 0.75: Added a scroll bar function for the Japan Theme
"""

# All the neccesary imports.
import re
import requests, bs4
import time, os
from datetime import date
import calendar
from dateutil import parser
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



#==============================================================================================================
# functions for default theme.
#==============================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def defaultTabs(a, b, d):

    d.setStyleSheet("""QTabBar::tab {
                                background: White;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: White;
                                }
                                QTabBar::tab:selected {
                                background: Darkslategray;
                                border-color: White;
                                border-bottom-color: Darkslategray;
                                color: White;
                                }""")

    a.setStyleSheet("QWidget { background-color: Darkslategray; color: white; }")
    b.setStyleSheet("QWidget { background-color: Darkslategray; color: white; }")
    #c.setStyleSheet("QWidget { background-color: Darkslategray; color: white; }")

# function for the scroll bar Themes.
# takes the scroll object as an arguement
def defaultScroll(d):

    d.setStyleSheet("""QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Darkslategray;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Darkslategray;
                                width: 3px;
                                height: 3px;
                                background: Darkslategray;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Darkslategray;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Darkslategray;
                                width: 3px;
                                height: 3px;
                                background: Darkslategray;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }""")

# A funtion for the menubar theme
# Takes the menubar objects as arguments
def defaultMenu(a):

    a.setStyleSheet("QMenu::item:selected { background-color: Darkslategray; }")
    a.setStyleSheet("""QMenuBar { background-color: white; }
                            QMenuBar::item:selected { background-color: Darkslategray; color: White; }""")

#========================================================================================================================
# Functions for the "SpaceX" Theme
#========================================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def spacexTabs(a, b, d):

    d.setStyleSheet("""QTabBar::tab {
                                background: White;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: White;
                                }
                                QTabBar::tab:selected {
                                background: Steelblue;
                                border-color: White;
                                border-bottom-color: Steelblue;
                                color: White;
                                }""")

    a.setStyleSheet("QWidget { background-color: Steelblue; color: white; }")
    b.setStyleSheet("QWidget { background-color: Steelblue; color: white; }")
    #c.setStyleSheet("QWidget { background-color: Steelblue; color: white; }")

# function for the scroll bar Themes.
# takes the scroll object as an arguement
def spacexScroll(d):

    d.setStyleSheet("""QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Steelblue;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Steelblue;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }""")

# A funtion for the menubar theme
# Takes the menubar objects as arguments
def spacexMenu(a):

    a.setStyleSheet("QMenu::item:selected { background-color: Steelblue; }")
    a.setStyleSheet("""QMenuBar { background-color: white; }
                            QMenuBar::item:selected { background-color: Steelblue; color: White; }""")

def spacexFrame(a):
    a.setStyleSheet(" QFrame { background: LightSlate Grey; color: Ivory }")


#==============================================================================================================
# functions for Japan theme.
#==============================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def japanTabs(a, b, d):

    d.setStyleSheet("""QTabBar::tab {
                                background: DimGray;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: DimGray;
                                }
                                QTabBar::tab:selected {
                                background: White;
                                border-color: White;
                                border-bottom-color: White;
                                color: black;
                                }""")

    a.setStyleSheet("QWidget { background-color: White; color: DimGray; }")
    b.setStyleSheet("QWidget { background-color: white; color: DimGray; }")
    #c.setStyleSheet("QWidget { background-color: white; color: DimGray; }")

# function for the scroll bar Themes.
# takes the scroll object as an arguement
def japanScroll(d):

    d.setStyleSheet("""QScrollBar:horizontal {
                                border: 2px solid white;
                                background: FireBrick;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid FireBrick;
                                width: 3px;
                                height: 3px;
                                background: FireBrick;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: white;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: FireBrick;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid FireBrick;
                                width: 3px;
                                height: 3px;
                                background: FireBrick;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }""")


# A funtion for the menubar theme
# Takes the menubar objects as arguments
def japanMenu(a):

    a.setStyleSheet("QMenu::item:selected { background-color: FireBrick; }")
    a.setStyleSheet("""QMenuBar { background-color: white; }
                            QMenuBar::item:selected { background-color: FireBrick; color: White; }""")

def japanFrame(a):
    a.setStyleSheet(" QFrame { background: FireBrick; color: White }")
