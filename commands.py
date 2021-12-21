# TODO
# option to type cancel at any point to interrupt
#   or handle interrupts to return to default state while handling command
# split on update using secondary key
#   new commands for update:
#   -> update <site name> password
#   -> update <site name> user
#   -> udate master
#   new commands for get
#   -> get <site name> passowrd
#   -> get <site name> user



import json
from constants import *
import input_handler
import config
import sys

INVALID_COMMAND_MSG = f'Invalid command. Type "{HELP}" to see command usage.'


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
    site_name = config.arguments

    # site name must be passed for command
    if site_name in {None, ''}:
        print(f'Invalid command. Type "{HELP}" to see command usage.')
        return

    # check if there is entry for site_name
    if site_name in config.data:
        replace = input_handler.yes_or_no(f'{site_name} already in keychain. Do you want to replace it? [Y, N] ')
        if replace == False:
             return

    user_name = input(PROMPT + 'Enter user name: ')
    password = input_handler.same_password()

    if password == CANCEL:
        print(f'New entry cancelled for {site_name}.')
        return

    confirmed = input_handler.enter_master_key(PROMPT + 'Enter master key to add new entry: ')

    if confirmed:
        config.data[site_name] = {
                'user_name' : user_name,
                'password' : password
            }
        print(f'New entry added for {site_name}.')

    else:
        print(f'New entry cancelled for {site_name}.')

def update():
    # TODO
    # check new password is not the same as old one -> define function for it
    # if multiple entries, prompt for email or
    # list all of them and select with up and down keys ?


    if config.arguments in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return

    option, argument = input_handler.split_first(config.arguments)

    if option in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return

    if option == MASTER:
        update_master_key()
        return
    
    elif option not in config.data and argument in {USER, PASS}:
        choice = input_handler.yes_or_no(f'{option} not in keychain. Do you want to add it? [Y, N] ')
        if choice == True:
            config.arguments = option
            new_password()
        return

    if argument == USER:
        update_user_name(option)

    elif argument == PASS:
        update_password(option)
    
    else:
        print(INVALID_COMMAND_MSG)

def update_master_key():
    confirmed = input_handler.enter_master_key('Enter current master key to allow update to the master key: ')
    if confirmed:
        new_master_key = input_handler.same_password('Enter new master key: ', 'Confirm new master key: ')

        if new_master_key != CANCEL:
            config.private_key_enc = new_master_key
            print('New master key saved.')
            return
    
    print('Update to the master key cancelled.')

def update_user_name(site_name):
    user_name = input(PROMPT + 'Enter new user name: ')

    confirmed = input_handler.enter_master_key(PROMPT + 'Enter master key to confirm user name update: ')

    if confirmed:
        config.data[site_name]['user_name'] = user_name
        print(f'User name updated for {site_name}.')

    else:
        print(f'User name update for {site_name} cancelled.')

def update_password(site_name):
    # TODO
    # check new password is not the same as old one -> define function for it
    # if multiple entries, prompt for email or
    # list all of them and select with up and down keys ?

    password = input_handler.same_password('Enter new password: ', 'Confirm new password: ')

    if password == CANCEL:
        print(f'Password update cancelled for {site_name}.')
        return

    confirmed = input_handler.enter_master_key(PROMPT + 'Enter master key to confirm password update: ')

    if confirmed:
        config.data[site_name]['password'] = password
        print(f'Password updated for {site_name}.')

    else:
        print(f'Password update for {site_name} cancelled.')

def get_password():
    site_name = config.arguments

    # site name must be passed for command
    if site_name in {None, ''}:
        print(f'Invalid command. Type "{HELP}" to see command usage.')
        return

    # check if entry exist
    if site_name not in config.data:
        choice = input_handler.yes_or_no(f'{site_name} not in keychain. Do you want to add it? [Y, N] ')
        if choice == True:
            new_password()
        return

    confirmed = input_handler.enter_master_key(PROMPT + f'Enter master key to retrieve password for {site_name}: ')

    if confirmed:
        password = config.data[site_name]['password']
        print(f'Password for {site_name} is: {password}')

    else:
        print(f'Password retrival for {site_name} cancelled.')

def get_user_name():
    site_name = config.arguments

    # site name must be passed for command
    if site_name in {None, ''}:
        print(f'Invalid command. Type "{HELP}" to see command usage.')
        return

    # check if entry exist
    if site_name not in config.data:
        choice = input_handler.yes_or_no(f'{site_name} not in keychain. Do you want to add it? [Y, N] ')
        if choice == True:
            new_password()
        return

    confirmed = input_handler.enter_master_key(PROMPT + f'Enter master key to retrieve user name for {site_name}: ')

    if confirmed:
        user_name = config.data[site_name]['user_name']
        print(f'User name for {site_name} is: {user_name}')

    else:
        print(f'User name retrival for {site_name} cancelled.')

def reset():
    choice = input_handler.yes_or_no('Are you sure you want to reset keychain? [Y, N] ')
    if choice == True:
        config.data = {}
        print('Keychain reset.')
    else:
        print('Keychain reset cancelled.')

def remove():
    # TODO
    # if there are multiple entries, prompt for email or used arrows to select from list

    site_name = config.arguments

    # site name must be passed for command
    if site_name in {None, ''}:
        print(f'Invalid command. Type "{HELP}" to see command usage.')
        return

    # check if entry exist
    if site_name not in config.data:
        choice = input_handler.yes_or_no(f'{site_name} not in keychain. Do you want to add it? [Y, N] ')
        if choice == True:
            new_password()
        return

    confirmed = input_handler.enter_master_key(PROMPT + f'Enter master key to remove entry for {site_name}: ')

    if confirmed:
        config.data.pop(site_name)
        print(f'Entry for {site_name} removed.')

    else:
        print(f'Removal of entry for {site_name} cancelled.')

def help():
    with open(help_path, 'r') as f:
        help_msg = f.read()
        print(help_msg)

def list_entries():
    entry_keys = config.data.keys()

    if len(entry_keys) == 0:
        print('No entries in password manager.')
        return
    
    for k in entry_keys:
        print(k)
    