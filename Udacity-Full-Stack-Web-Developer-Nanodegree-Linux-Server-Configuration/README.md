# Linux-Server-Configuration-UDACITY

## The IP address and SSH port so your server can be accessed by the reviewer.
    54.201.40.18       SSH port: 2200

## The complete URL to your hosted web application.
   You can visit http://54.201.40.18 for the website deployed.

## A summary of software you installed and configuration changes made.


## connect Mac terminal with Amazon Lightsail
1. download your default private key from the Account page.
2. chmod 600 LightsailDefaultPrivateKey-us-west-2.pem
3. ssh ubuntu@54.201.40.18 -p 22 -i LightsailDefaultPrivateKey-us-west-2.pem

## Update all currently installed packages
1.sudo apt-get update
2.sudo apt-get upgrade

## Create a new user named grader
1. sudo adduser grader
2. sudo adduser grader sudo
3. sudoedit /etc/ssh/sshd_config (PasswordAuthentication -> yes)
4. sudo service ssh restart

## Set ssh login using keys
1. ssh-keygen
2. log in as grader: ssh grader@54.201.40.18 -p 22
3. mkdir .ssh     
4. touch .ssh/authorized_keys
5. exit
6. sudo cp /home/ubuntu/.ssh/server.pub  /home/grader/.ssh/authorized_keys
7. sudo chown grader:grader /home/grader/.ssh/authorized_keys
8. ssh grader@54.201.40.18 -p 22 -i ~/.ssh/server (log in as server using key)
9. sudoedit /etc/ssh/sshd_config (PasswordAuthentication -> no)
10.sudo service ssh restart
	

## Change the SSH port from 22 to 2200
1. sudoedit /etc/ssh/sshd_config (port 22 -> port 2200)
2. sudo service ssh restart

## Configure the Uncomplicated Firewall (UFW)

Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)

1.sudo ufw default deny incoming
2.sudo ufw default allow outgoing
3.sudo ufw allow 2200/tcp
4.sudo ufw allow 80/tcp
5.sudo ufw allow 123/udp
6.sudo ufw enable 
 
## Configure the local timezone to UTC
1. sudo dpkg-reconfigure tzdata
2. chose UTC.

## Install and configure Apache to serve a Python mod_wsgi application
1. Install Apache:    sudo apt-get install apache2
2. Install mod_wsgi:  sudo apt-get install python-setuptools libapache2-mod-wsgi
3. Restart Apache:    sudo service apache2 restart

## Install and configure PostgreSQL
1. Install PostgreSQL:  sudo apt-get install postgresql
2. Check if no remote connections are allowed:  sudo vim /etc/postgresql/9.5/main/pg_hba.conf
3. Login as user "postgres”:  sudo su - postgres
4. Get into postgreSQL shell:  psql
5. Create a new database named catalog  and create a new user named catalog in postgreSQL shell
	postgres=# CREATE DATABASE catalog;
	postgres=# CREATE USER catalog;

6. Set a password for user catalog
	postgres=# ALTER ROLE catalog WITH PASSWORD 'password';

7. Give user "catalog" permission to "catalog" application database
	postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;

7. Quit postgreSQL: postgres=# \q
8. Exit from user "postgres”: exit
 

## Install git, clone and setup your Catalog App project.
1. Install Git using: sudo apt-get install git
2. move to the /var/www directory: cd /var/www 
3. Create the application directory: sudo mkdir FlaskApp
4. Move inside this directory using: cd FlaskApp
5. Clone the Catalog App to the virtual machine: git clone https://github.com/caofang92/Item-Catalog.git
6. Rename the project's name: sudo mv ./Udacity-Full-Stack-Web-Developer-Nanodegree-Projects-Item-Catalog ./FlaskApp
7. Move to the inner FlaskApp directory: cd FlaskApp
8. Rename “server.py” to “__init__.py”: sudo mv server.py __init__.py
9. Edit “database_setup.py”, “server.py” and “lotsofitems.py” and change “engine = create_engine('sqlite:///itemcatalogwithusers.db')” to “engine = create_engine('postgresql://catalog:password@localhost/catalog')”
10. Install pip:  sudo apt-get install python-pip
11. install dependencies
12. Install psycopg2:  sudo apt-get -qqy install postgresql python-psycopg2
13. Create database schema: sudo python database_setup.py
14. add data to database: sudo python lotsofitems.py

## Configure and Enable a New Virtual Host
1. Create FlaskApp.conf to edit: sudo nano /etc/apache2/sites-available/FlaskApp.conf
2. Add the following lines of code to the file to configure the virtual host. 
	
	```
	<VirtualHost *:80>
		ServerName 54.201.40.18
		ServerAdmin cao.677@osu.edu
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
	```
3. Enable the virtual host with the following command: sudo a2ensite FlaskApp

## Create the .wsgi File
1. Create the .wsgi File under /var/www/FlaskApp: 
	
	cd /var/www/FlaskApp
	
	sudo nano flaskapp.wsgi 
	
2. Add the following lines of code to the flaskapp.wsgi file:
	
	#!/usr/bin/python
	import sys
	import logging
	logging.basicConfig(stream=sys.stderr)
	sys.path.insert(0,"/var/www/FlaskApp/")

	from FlaskApp import app as application
	application.secret_key = 'super_secret_key'

## Restart Apache
1. Restart Apache: sudo service apache2 restart
