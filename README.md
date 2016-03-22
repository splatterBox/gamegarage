# gamegarage

A web browser is required to view the site. This guide assumes that you already have one pre-installed on your computer. 

You will need to do the following things to get gamegarage running on your computer:

1) install python2.7
    
    Download python from:
    https://www.python.org/downloads/release/python-2711/
    
    Installation instructions should be in the readme file.
    
    Note: Python3 is not compatible with our software.

2) install postgresql, psycopg2, flask, postgresql-contrib-9.3, and socketio packages.
    
    Linux installation commands are:
    
    sudo apt-get update
    sudo apt-get install postgresql
    sudo easy_install flask markdown
    sudo apt-get install python-psycopg2
    sudo apt-get install postgresql-contrib-9.3
    sudo easy_install flask-socketio

3) run 'git clone https://github.com/splatterBox/gamegarage.git' to get a copy of the latest source code.


4) Navigate to the gamegarage folder:

   cd / gamegarage
    
5) Start postgres server:

   sudo service postgresql start

6) Setup postgresql database application:

   A. Login and set username of root:

   sudo sudo -U rootusername psql
   (I think "U" is capitalized.  Try it out.)

   B. Set root user password:

   \password rootusername

   C. Create the "limited" username postgres user:

   create role limited with login;

   D. Create a password for limited user:

   \password limited
   (Use password "limited762*".)

   Note: Normally you log into postgres with this command:
   psql -U username postgres -h localhost

7) run the server.py file with python2 (usually 'python2 server.py'). 

8) if the server.py file runs successfully then open the hosted site in your browser.
