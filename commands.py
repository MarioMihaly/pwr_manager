from constants import *
from input_handler import *
import sys


def exit():
    '''
        Function to handle exit command.
        -> save changes made to files
        -> exit CLI
    '''
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

    print(f'Site: {site_name}\nUser name: {user_name}\nPassword:{password}')

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
        print('Keychain reset.')
    else:
        print('Keychain reset cancelled.')

def remove(arguments):
    # check if there is an entry for a given site
    # if there are multiple entries, prompt for email
    site_name = arguments
    print(f'Entry for {site_name} removed')