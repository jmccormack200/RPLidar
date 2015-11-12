#RPLidar Drivers in Python

##LidarPrint.py

The basic file just opens the Lidar and starts printing out to the command line. 
Unfortunately, this does not yet have all the error correction necessary. 
Where possible, LidarPrint.py should be used to test your setup, then follow
the instructions in the UDP section to actually use it. 

##UDP

The UDP folder has the most up to date drivers. After trying (and failing) at a 
couple different methods, this turned out to be the easiest way to get data to transmit
into Unity. There are two files, one to run on windows and one to run on linux. They
will require some tweaking on your part to get working (basically changing port/Ip combination. I hope this helps someone out. I am more than willing to answer any questions you may have. 


The two main files to use in this folder are:

- UDPLinux.py - for Linux computers
- UDPLidar.py - for Windows machines
- UDPLidarSingleFrame.py - To test one single run of the LIDAR

##Firebase

This was a brief test to see if I could use the Firebase platform to run the program.
It should still work but not at the speed we were looking for. 
This is left just in case someone needs to use it. If it is is something you need
feel free to reach out to me and I will look into getting it working again.

##Graph Tests

This was using some quick LIDAR scans with matplotlib to see what they
would look like. It doesnt add any functionality and was left here just in case I needed it.

## JSON

A brief look at how to send data as JSON in preparation for UDP. 

## Thread Tests

This was an attempt to practice how to use threads before I integrated them into the program. 
This is not a stand alone program.

## ZMQ

ZeroMQ was used to try to create a queue to store the Lidar data. This ended up being better
to implement in another part of the project. It is left here only for reference. 