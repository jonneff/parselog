The concepts demonstrated in this code include test driven development, logging, cacheing and multithreading with geolocation of IP addresses.  

This repository contains my solution to the coding challenge listed below.  Code for running the application (run.sh and execute_parselog.py) are located at the top level, along with test coverage statistics and package files.  The parselog applicaiton source is under the app/ folder while tests are under test/.  The data/ folder contains input and output files along with parselog's log, called parselog.log.  

Coding challenge

Using the following dataset data/access.log, write a program that reads in the dataset and writes to a file (access.log.out) the following:

date & time request was processed by the web server as epoch (from the file)

uri user click on (from the file)

referer (from the file)

ip address (from the file)

organization (from the ip address)

latitude (from the ip address)

longitude (from the ip address)

isp name (from the ip address)

HINT: google “ip lookup”.  

The code needs to run; it should contain unit test cases, exception handling, logging, and any optimizations. If coding in Java, please take into account Objected Oriented Programming principles. In short, even if you consider the problem to be simple, we want you to write the code as if it was going into production for a client and would need to be read, maintained, and extended in the future. 
