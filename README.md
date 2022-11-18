# JapanQuakes
JapanQuakes is a simple app written in Python and uses Pqyqt5 for a GUI. The app scrapes Earthquake data from the web using Beautiful Soup and dispays it to the user in a clean UI with graphs from MatPlotLib.


## Installation

### Debian-based Distros And Fedora
Linux Mint/Ubuntu/Pop!OS

- Open the terminal and clone this repository to your directory of choice:
```bash
cd ~/Downloads/
git clone https://github.com/shiroininjaTech/JapanQuakes.git
cd JapanQuakes/
```
- Use chmod to change the permissions of the installation file and run it:
```bash
chmod +x install.sh
./install.sh
```

- Change username to your username in "icon" and "application" lines in the AstroNinja.desktop file using nano or a text editor:

```bash
nano ~/Desktop/JapanQuakes.desktop
```


### Use AstroNinja
Ubuntu and Pop users: right-click on JapanQuakes desktop icon and click "Allow Launching".
- It can also be launched from the terminal:

```bash
python3 JapanQuakes.py
```
## License

This software is licensed under the GPLv3 license. 

