import encryption
import constants
import input_handler
import config
import sys

INVALID_COMMAND_MSG = f'Invalid command. Type "{constants.HELP}" to see command usage.'

def exit():
    '''
        Function to handle exit command.
        -> save changes made to files
        -> exit CLI
    '''

    # Exit database
    config.database.exit()

    # Exit application
    sys.exit()

def new_password():
    site_name = config.arguments

    if site_name in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return

    entry_in_db = config.database.in_table(constants.TABLE, constants.SITE_COL, site_name)
    if entry_in_db:
        replace = input_handler.yes_or_no(f'{site_name} already in keychain. Do you want to replace it? [Y, N] ')
        
        if replace == False:
             return
        
        config.database.delete(constants.TABLE, site_name)

    user_name = input('Enter user name: ')
    password = input_handler.same_password()

    if password == constants.CANCEL:
        print(f'New entry cancelled for {site_name}.')
        return

    enrypted_user_name = config.encryptor.encrypt(user_name)
    enrypted_password = config.encryptor.encrypt(password)
    config.database.insert(constants.TABLE, (site_name, enrypted_user_name, enrypted_password))
    
    print(f'New entry added for {site_name}')

def get():
    if config.arguments in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return

    site_name, argument = input_handler.split_first(config.arguments)

    if argument in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return
    
    site_in_db = config.database.in_table(constants.TABLE, 'site', site_name)

    if not site_in_db and argument in {constants.USER_NAME, constants.PASSWORD}:
        choice = input_handler.yes_or_no(f'{site_name} not in keychain. Do you want to add it? [Y, N] ')
        if choice == True:
            config.arguments = site_name
            new_password()
        return

    if argument == constants.USER_NAME:
        get_user_name(site_name)

    elif argument == constants.PASSWORD:
        get_password(site_name)
    
    else:
        print(INVALID_COMMAND_MSG)

def get_password(site_name):
    enrypted_password = config.database.get_entry(constants.TABLE, 'site', site_name, 'password')
    password = config.encryptor.decrypt(bytes(enrypted_password))
    input_handler.copy_to_clipboard(password, f'Password for {site_name} copied to clipboard.')

def get_user_name(site_name):
    encrypted_user_name = config.database.get_entry(constants.TABLE, 'site', site_name, 'user')
    user_name = config.encryptor.decrypt(bytes(encrypted_user_name))
    input_handler.copy_to_clipboard(user_name, f'User name for {site_name} copied to clipboard.')

def update():
    # TODO
    # check new password is not the same as old one -> define function for it
    # if multiple entries, prompt for email or
    # list all of them and select with up and down keys ?

    if config.arguments in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return

    site_name, argument = input_handler.split_first(config.arguments)

    if site_name in {None, ''}:
        print(INVALID_COMMAND_MSG)
        return

    if site_name == constants.MASTER:
        update_master_key()
        return
    
    site_in_db = config.database.in_table(constants.TABLE, 'site', site_name)

    if not site_in_db and argument in {constants.USER_NAME, constants.PASSWORD}:
        choice = input_handler.yes_or_no(f'{site_name} not in keychain. Do you want to add it? [Y, N] ')
        
        if choice == True:
            config.arguments = site_name
            new_password()
        
        return

    if argument == constants.USER_NAME:
        update_user_name(site_name)

    elif argument == constants.PASSWORD:
        update_password(site_name)
    
    else:
        print(INVALID_COMMAND_MSG)

def update_master_key():
    '''
        TODO:
            set up interface to update password to database
            when updated, encrypt passwords with the new key
    '''
    new_master_key = input_handler.same_password('Enter new master key: ', 'Confirm new master key: ')
    
    if new_master_key != constants.CANCEL:
        config.database.change_password(new_master_key)
        new_key_hash = encryption.str_to_SHA(new_master_key)
        new_enryptor = encryption.AES_encryption(new_key_hash)

        sites = config.database.get_entries(constants.TABLE, (constants.SITE_COL,))
        
        for (site,) in sites:
            # TODO:
            # new function in database to change enryption of entry
            
            # decrypt user name using old key
            old_encryption = config.database.get_entry(constants.TABLE, constants.SITE_COL, site, constants.USER_COL)
            user_name = config.encryptor.decrypt(old_encryption)

            new_enrcyption = new_enryptor.encrypt(user_name)
            config.database.update(constants.TABLE, site, constants.USER_COL, new_enrcyption)

            # decrypt password using old key
            old_encryption = config.database.get_entry(constants.TABLE, constants.SITE_COL, site, constants.PASSWORD_COL)
            password = config.encryptor.decrypt(old_encryption)

            # encrypt entries using new key
            new_enrcyption = new_enryptor.encrypt(password)
            config.database.update(constants.TABLE, site, constants.PASSWORD_COL, new_enrcyption)
            
        
        config.key_hash = new_key_hash
        config.encryptor = new_enryptor

        print('New master key saved.')
        return
    
    print('Update to the master key cancelled.')
    
def update_user_name(site_name):
    user_name = input('Enter new user name: ')
    enrypted_user_name = config.encryptor.encrypt(user_name)
    config.database.update(constants.TABLE, site_name, constants.USER_COL, enrypted_user_name)
    print(f'User name updated for {site_name}.')

def update_password(site_name):
    # TODO
    # check new password is not the same as old one -> define function for it
    # if multiple entries, prompt for email or
    # list all of them and select with up and down keys ?

    password = input_handler.same_password('Enter new password: ', 'Confirm new password: ')

    if password == constants.CANCEL:
        print(f'Password update cancelled for {site_name}.')
        return

    enrypted_password = config.encryptor.encrypt(password)
    config.database.update(constants.TABLE, site_name, constants.PASSWORD_COL, enrypted_password)
    print(f'Password updated for {site_name}.')

def reset():
    choice = input_handler.yes_or_no('Are you sure you want to reset keychain? [Y, N] ')
    if choice == True:
        config.database.reset_table(constants.TABLE)
        print('Keychain reset.')
    else:
        print('Keychain reset cancelled.')

def remove():
    # TODO
    # if there are multiple entries, prompt for email or used arrows to select from list

    site_name = config.arguments

    if site_name in {None, ''}:
        print(f'Invalid command. Type "{constants.HELP}" to see command usage.')
        return

    site_in_db = config.database.in_table(constants.TABLE, constants.SITE_COL, site_name)
    if not site_in_db:
        choice = input_handler.yes_or_no(f'{site_name} not in keychain. Do you want to add it? [Y, N] ')
        if choice == True:
            new_password()
        return

    config.database.delete(constants.TABLE, site_name)
    print(f'Entry for {site_name} removed.')

def help():
    with open(constants.HELP_PATH, 'r') as f:
        help_msg = f.read()
        print(help_msg)

def list_entries():
    entries = config.database.get_entries(constants.TABLE, (constants.SITE_COL,))

    if len(entries) == 0:
        print('No entries in password manager.')
        return
    
    for entry in entries:
        print(entry[0])
    