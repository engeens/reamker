#####################################################################
## SOME CONFIG PARAMETERS                                           #
#####################################################################

# Once the app have bee initialize, set init_app to False
INIT_APP = True
# Theme view. Note this app has multiple theme views setup.
CONFIG_THEME = 'default'
# Allow documentation on public side.
ALLOW_DOC_PUBLIC_SIZE = False

# If SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
HTTPS = False

# Setting UTC for the global time app
request.now = request.utcnow

# To know the user timezone, check layout y home controller
is_timezone_unknown = (session.user_timezone is None)
user_timezone = session.user_timezone or 'UTC'

#####################################################################
# DATABASE CONFIGURATION                                            #
#####################################################################
DATABASE_USER = None
DATABASE_PASS = None
DATABASE_HOST = None
DATABASE_DB = 'storage.sqlite'
DATABASE_CONNECTION = 'sqlite://%s' % DATABASE_DB
# To connect to MySQL
# DATABASE_CONNECTION = 'mysql://%s:%s@%s/%s' % (DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_DB)
