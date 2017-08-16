# Logs Analysis

## About

This is the third project for the Udacity Full Stack Nanodegree. In this project, a large database with over a million rows is explored by building complex SQL queries to draw business conclusions for the data. The project mimics building an internal reporting tool for a newpaper site to discover what kind of articles the site's readers like. The database contains newspaper articles, as well as the web server log for the site.


## Setup
1. Clone this repository
2. Download the data from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
3. You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the downloaded folder
## To Run

cd into the downloaded folder, Launch Vagrant VM by running "vagrant up", you can then log in with "vagrant ssh"

To load the data, use the command "psql -d news -f newsdata.sql" to connect a database and run the necessary SQL statements.

The database includes three tables:
- Authors table
- Articles table
- Log table

To execute the program, run "python project3.py" from the command line.
