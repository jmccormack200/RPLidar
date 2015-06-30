#RPLidar Drivers in Python

##LidarPrint.py

The basic file just opens the Lidar and starts printing out to the command line. 
Unfortunately, this does not yet have all the error correction necessary. 
I should have time shortly to fix the problem.

##UDP

The UDP folder has the most up to date drivers. After trying (and failing) at a 
couple different methods, this turned out to be the easiest way to get data to transmit
into Unity. There are two files, one to run on windows and one to run on linux. They
will require some tweaking on your part to get working (basically changing port/Ip combination. I hope this helps someone out. I am more than willing to answer any questions you may have. 


The two main files to use in this folder are:

-UDPLinux.py - for linux computers
-UDPLidar.py - for windows machines
