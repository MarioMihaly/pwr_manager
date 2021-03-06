PROMPT = '> '

##################
#    Commands
##################
EXIT = 'exit'
NEW = 'new'
UPDATE = 'update'
GET = 'get'
RESET = 'reset'
REMOVE = 'remove'
HELP = 'help'
LIST = 'list'

##################
#     Options
##################
MASTER = 'master'
PASSWORD = 'password'
USER_NAME = 'user'

##################
 #    Flags
##################
CANCEL = 'cancel'

##################
#   Data paths
##################
HELP_PATH = './data/help.txt'

##################
#    Database
##################
HOST = 'localhost'
DATABASE_USER = 'password_manager'
DATABASE = 'passwords'
TABLE = 'passwords'
COLUMNS = (('site', 'VARCHAR(20)'), ('user', 'BINARY(32)'), ('password', 'BINARY(32)'))
SITE_COL = 'site'
USER_COL = 'user'
PASSWORD_COL = 'password'
COLUMN_SELECTION = {'site': 0, 'user': 1, 'password': 2}