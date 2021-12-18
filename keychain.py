import sys
import json
import pyperclip

PROMPT = '> '
'''
    Commands
'''
EXIT = 'exit'
NEW = 'new'
UPDATE = 'update'
UPADATE_KEY = 'update_key'
RESET = 'reset'

'''
    Data paths
'''
keys_path = './data/keys.json'
data_path = '.data/data.json'

'''
    Global variables
'''
public_key = None
private_key_enc = None


def command_handler(command, arguments):
    '''
    
    '''

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

    else:
        print('Invalid command')
    


def exit():
    '''
        Function to handle exit command.
        -> save changes made to files
        -> exit CLI
    '''
    sys.exit()

def new_password():
    site_name = input(PROMPT + 'Enter site: ')
    user_name = input(PROMPT + 'Enter user name: ')
    password = input(PROMPT + 'Enter password: ')
    password_conf = input(PROMPT + 'Confirm password: ')

    while password != password_conf:
        print('Passwords don\'t match!')
        password = input(PROMPT + 'Enter password: ')
        password_conf = input(PROMPT + 'Confirm password: ')

    print(f'Site: {site_name}\nUser name: {user_name}\nPassword:{password}')

def update_password(arguments):
    site_name = arguments
    print(f'Password updated for site {site_name}')

def update_key():
    pass

def reset():
    a = input('Are you sure you want to reset keychain? [Y, N] ')
    if a in ['y', 'Y']:
        print('Keychain reset.')
    elif a in ['n', 'N']:
        print('Keychain reset cancelled.')
    else:
        print(f'Invalid choice {a}')
        reset()

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
        #print(f'Command: {command}')
        #print(f'Arguments: {arguments}')

        command_handler(command, arguments)

if __name__ == '__main__':
    main()