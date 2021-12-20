from constants import *
import input_handler
import json

#Global variables
keys = None
public_key = None
private_key_enc = None
data = None

def init_data():
    '''
        Function to initialise data used by the password manager.
    '''
    global public_key, private_key_enc, data, keys

    # Initialise keys
    with open(keys_path, 'r') as keys_file:
        keys = json.load(keys_file)
        public_key = keys['keys']['public']
        private_key_enc = keys['keys']['private']

    # Prompt for master key, exit after 3 attemtps
    login_success = input_handler.enter_master_key3()
    
    if login_success == False:
        print('Login failed!')
        exit()

    # Load data
    with open(data_path, 'r') as data_file:
        data = json.load(data_file)

    print(f'Welcome to your password manager. Enter "{HELP}" to display available commands.')