import constants
from database import Database, TABLES
from mysql.connector.errors import DatabaseError, ProgrammingError
import encryption
from getpass import getpass

# Global variables
key_hash = None
encryptor = None
arguments = None
database = None

def init_keychain():
    global key_hash, encryptor, database

    # Connect to database
    while True:
        password = getpass('Enter master password: ')
        if password == constants.CANCEL:
            return False

        try:
            database = Database(constants.HOST, constants.DATABASE_USER, constants.DATABASE, password)
            key_hash = encryption.str_to_SHA(password)
            encryptor = encryption.AES_encryption(key_hash)

            if not database.exists(constants.TABLE, TABLES):
                database.new_table(constants.TABLE, constants.COLUMNS)

            return True

        # Invalid user or password
        except ProgrammingError as e:
            print('Connection to database failed!', e.__context__)
            continue
        
        # Invalid MySQL server host
        except DatabaseError as e:
            print('Invalid server host!', e.__context__)
            continue
