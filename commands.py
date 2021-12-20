import json
from constants import *
from input_handler import yes_or_no
import config
import sys


def exit():
    '''
        Function to handle exit command.
        -> save changes made to files
        -> exit CLI
    '''
    # Save data
    with open(data_path, 'w') as data_file:
        json.dump(config.data, data_file)

    # Save keys
    with open(keys_path, 'w') as keys_file:
        config.keys['keys']['public'] = config.public_key
        config.keys['keys']['private'] = config.private_key_enc
        json.dump(config.keys, keys_file)

    # Exit application
    sys.exit()

def new_password():
    # check if site_name and user_name combo already in database
    # prompt for possibility to update


    site_name = input(PROMPT + 'Enter site: ')

    # check if there is entry for site_name
    # ask if want to update or continue adding a new one

    user_name = input(PROMPT + 'Enter user name: ')
    password = input(PROMPT + 'Enter password: ')
    password_conf = input(PROMPT + 'Confirm password: ')

    while password != password_conf:
        print('Passwords don\'t match!')
        password = input(PROMPT + 'Enter password: ')
        password_conf = input(PROMPT + 'Confirm password: ')


    entry = {
        'site_name' : site_name,
        'user_name' : user_name,
        'password' : password
    }
    config.data['entries'].append(entry)
    
    

def update_password(arguments):
    # check if entry exist
    # if multiple entries, prompt for email or
    # list all of them and select with up and down keys ?

    site_name = arguments
    print(f'Password updated for {site_name}')

def update_key():
    pass

def reset():
    choice = yes_or_no('Are you sure you want to reset keychain? [Y, N] ')
    if choice == True:
        with open(data_path, 'r+') as f:
            data = json.load(f)
            data['entries'] = []
            print(data['entries'])
        print('Keychain reset.')
    else:
        print('Keychain reset cancelled.')

def remove(arguments):
    # check if there is an entry for a given site
    # if there are multiple entries, prompt for email
    site_name = arguments
    print(f'Entry for {site_name} removed')

def help():
    with open(help_path, 'r') as f:
        help_msg = f.read()
        print(help_msg)