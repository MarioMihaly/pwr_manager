import constants
from database import Database
from mysql.connector.errors import DatabaseError, ProgrammingError
import input_handler
import encryption
import json
from os.path import exists

# Global variables
key_hash = None
data = None
arguments = None
database = None


def init_data():
    '''
        Function to initialise data used by the password manager.
    '''

    global key_hash, data

    # Check for existing configuration
    if not exists(constants.key_bin):
        print('Wellcome to your new password manager. Set up your master password to get started.')
        password = input_handler.same_password('Enter master password: ', 'Confirm master password: ')
        key_hash = encryption.str_to_SHA(password)
        data = {}
        print(f'Master password is set. Enter "{constants.HELP}" to display available commands.')

    else:

        # Load configuration
        with open(constants.key_bin, 'rb') as key_f:
            key_hash = key_f.read()

        # Prompt for master key, exit after intial + 3 attemtps
        login_success = input_handler.enter_master_key3()
        
        if login_success == False:
            print('Login failed!')
            exit()

        # Load data
        with open(constants.data_bin, 'rb') as data_file:
            encoder = encryption.AES_encryption(key_hash)
            in_d = data_file.read()
            data = json.loads(encoder.decrypt(in_d))

        print(f'Welcome to your password manager. Enter "{constants.HELP}" to display available commands.')

def init_keychain():
    '''
        TODO:
        ->create database and table if first use
        ->set up password
    '''
    global key_hash, database

    # Connect to database
    while True:
        password = input('Enter master password: ')
        if password == constants.CANCEL:
            return False

        try:
            database = Database(constants.HOST, constants.USER, constants.DATABASE, password)
            key_hash = encryption.str_to_SHA(password)
            return True

        # Invalid user or password
        except ProgrammingError as e:
            print('Connection to database failed!', e.__context__)
            continue
        
        # Invalid MySQL server host
        except DatabaseError as e:
            print('Invalid server host!', e.__context__)
            continue
