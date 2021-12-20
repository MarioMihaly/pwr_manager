from constants import *
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
    attempt_max = 3
    attempt_count = 0

    master_key = input(PROMPT + 'Enter master key: ')
    
    if master_key != private_key_enc:
        print(f'Invalid master key! {attempt_max - attempt_count} attempt(s) remaining.')
        master_key = input(PROMPT + 'Enter master key: ')
        attempt_count += 1

        while attempt_count < attempt_max and master_key != private_key_enc:
            print(f'Invalid master key! {attempt_max - attempt_count} attempt(s) remaining.')
            master_key = input(PROMPT + 'Enter master key: ')
            attempt_count += 1

    if attempt_count == attempt_max:
        print('Login failed!')
        exit()

    # Load data
    with open(data_path, 'r') as data_file:
        data = json.load(data_file)

    print('Welcome to your password manager. Enter "help" to display available commands.')