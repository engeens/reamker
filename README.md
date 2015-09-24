# reamker
Reamker is Single Sign On (SSO) web application

##Features:

1- Three roles: admin, editor, viewer and staff:
2- Support multiples LDAPs (Open Ldap, MS Active Directory, Notes Domino) or local database for authentication.
3- Can talk with SQLite, PostgreSQL, MySQL, MSSQL, FireBird, Oracle, IBM DB2, etc.
4- Full users accountability: open session, time zone and IPs request, etc.
5- Multi views for the back end frontend design.
6- Custom email templates for sending notification to the users.
7- Custom error pages...


## Screenshots:

![Image](https://github.com/engeens/reamker/blob/master/private/docs/front_cas.png?raw=true)
```
-
```
![Image](https://github.com/engeens/reamker/blob/master/private/docs/home_admin.png?raw=true)



## Installing

### Extra modules
```
pip install ConfigParser
pip install tzlocal
pip install html2text
```

To encode jpeg for App icons:
```
sudo apt-get install libjpeg-dev
sudo pip install -I pillow
```
### How to install the framework in Linux, windows or Mac:

1- Download the last web2py version and unzip:
```
cd /opt
wget http://www.web2py.com/examples/static/web2py_src.zip
unzip web2py_src.zip
```

2- Download the app from github and move it into web2py framework:
```
cd /opt/web2py/applications
git clone https://github.com/josedesoto/monitor.git cas
```

3- Run web2py and ready to use it!!!
```
python /opt/web2py/web2py.py
```

4- Open the URL: http://localhost:8000/cas

For more details how to make it works with Apache, Nginx, etc, please take a look here:

http://web2py.com/books/default/chapter/29/13/deployment-recipes

### Setting app the CAS server app:

Run: http://localhost:8000/cas/default/init

Once the app is installed modify the attribute INIT_APP from models/_settings.py
```
INIT_APP =  False
```
To access as Admin user:

```
Email: admin@test.com
Password: temporal
```

