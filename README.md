# cc-svds

This repository contains my solution to the SVDS coding challenge listed below.  Code for running the application (run.sh and execute_parselog.py) are located at the top level, along with test coverage statistics and package files.  The parselog applicaiton source is under the app/ folder while tests are under test/.  The data/ folder contains input and output files along with parselog's log, called parselog.log.  

SVDS coding challenge

Silicon Valley Data Science
Data Engineering Coding Challenge – 2015

"Using the following dataset https://github.com/silicon-valley-data-science/datasets/blob/master/access.log (schema info is here https://github.com/silicon-valley-data-science/datasets/blob/master/access_log_schema).  
Write a program that reads in the dataset (access.log), and writes to a file (access_log.out) the following:

date & time request was processed by the web server as epoch (from the file)

uri user click on (from the file)

referer (from the file)

ip address (from the file)

organization (from the ip address)

latitude (from the ip address)

longitude (from the ip address)

isp name (from the ip address)

HINT: google “ip lookup”.  

The code needs to run; it should contain unit test cases, exception handling, logging, and any optimizations. If coding in Java, please take into account Objected Oriented Programming principles. In short, even if you consider the problem to be simple, we want you to write the code as if it was going into production for a client and would need to be read, maintained, and extended in the future. "
