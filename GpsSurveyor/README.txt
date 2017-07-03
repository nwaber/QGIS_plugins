--------------GPS Surveyor Plugin---------------------
2017/07/03

This Plugin was designed to collect GPS data during archaeological survey.

The plugin depends on NMEA format GPS input.  It was initially designed for use with the gen1 Piksi RTK GPS (www.swiftnav.com), but will work with any GPS capable of sending NMEA data.


How to use:
1) Connect to a GPS using the GPS Information panel.
	-The GPS must be transmitting in NMEA format.
	-If using a Garmin GPS on Windows, use GPSGate as an intermediary between the GPS and computer.
	-GPS must transmit at BAUD 9600
2) Click the GPS Surveyor plugin icon to activate the plugin.
3) Select a point type from the pulldown menu.
4) Start surveying.
5) Don't forget to save!  The file is saved in memory until you actually create a file and click "save".


The point type pulldown menu may be edited to reflect different survey goals.
Simply edit line 384 to add/change/remove items from the combo box.   ...I think...