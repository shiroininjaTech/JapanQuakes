#!/bin/sh

# A simple Bash shell script that installs packages depended on by JapanQuakes
# Created by: Tom Mullins
# Created: 11/18/2022
# Modified: 1/26/2023


# Testing for addition of an option to install on Fedora

# Getting which distro the user is running
if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME

#echo $OS

# If the user is running Fedora
if [ "$OS" = "Fedora Linux" ] ; then
  # First, we need to install the proper python 3 Libraries
  sudo dnf install -y python3-pip python3-qt5 python3-dateutil python3-setuptools python3-bs4

  # Next we install the libaries installed by pip
  python3 -m pip install matplotlib lxml requests

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.JapanQuakes
  mkdir /home/$USER/.JapanQuakes

  cp -r ./* /home/$USER/.JapanQuakes

  # moving the desktop shortcut to the desktop
  mv /home/$USER/.JapanQuakes/JapanQuakes.desktop /home/$USER/Desktop/

  # Making both the desktop file and AstroNinjaMain.py executable
  chmod +x /home/$USER/Desktop/JapanQuakes.desktop
  chmod +x /home/$USER/.JapanQuakes/JapanQuakes.py

else
  # First, we need to install the proper python 3 Libraries
  sudo apt-get install -y python3-pip python3-pyqt5 python3-dateutil python3-setuptools python3-bs4

  # Next we install the libaries installed by pip
  python3 -m pip install matplotlib lxml requests scrapy

  # removes the folder, then copies the files to a . folder.
  rm -rf /home/$USER/.JapanQuakes
  mkdir /home/$USER/.JapanQuakes

  cp -r ./* /home/$USER/.JapanQuakes

  # moving the desktop shortcut to the desktop
  mv /home/$USER/.JapanQuakes/JapanQuakes.desktop /home/$USER/Desktop/

  # Making both the desktop file and AstroNinjaMain.py executable
  chmod +x /home/$USER/Desktop/JapanQuakes.desktop
  chmod +x /home/$USER/.JapanQuakes/JapanQuakes.py

fi

  #echo $OS
  # If the user is running Linux Mint
  if [ "$OS" = "Linux Mint" ] ; then
      # Removing an uneeded package that causes formatting errors in Linux Mint
      sudo apt-get remove qt5ct ;
  fi





fi
