'''
    TODO
    -> set up of master password
    -> reading entries (read into Pandas.DataFrame)
    -> look up function
        -> list all entries, way for user to select
        -> up and down arrows and enter for selection ?
    -> update_email for entrys
    -> allow duplicates
'''

import json
import pyperclip
from input_handler import *
from commands import *
from constants import *


'''
    Global variables
'''
public_key = None
private_key_enc = None
arguments = None

def command_handler(command, arguments):
    '''
    
    '''
    #global arguments
    

    if command == EXIT:
        exit()

    elif command == NEW:
        new_password()

    elif command == UPDATE:
        update_password(arguments)

    elif command == UPADATE_KEY:
        update_key()

    elif command == RESET:
        reset()

    elif command == REMOVE:
        remove(arguments)

    else:
        print('Invalid command')
    

def init_data():
    global public_key, private_key_enc

    # Initialise keys
    with open(keys_path, 'r') as f:
        keys = json.load(f)['keys']
        public_key = keys['public']
        private_key_enc = keys['private']

    print(f'Public key: {public_key}\nPrivate key: {private_key_enc}')
    #pyperclip.copy(public_key)
    #print('Public key coppied to clipboard.')
    
def main():
    init_data()

    while True:
        input_str = input(PROMPT)
        command, arguments = input_str.split(' ', 1) if ' ' in input_str else (input_str, None)

        command_handler(command, arguments)

if __name__ == '__main__':
    main()