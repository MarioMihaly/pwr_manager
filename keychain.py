'''
    TODO
    -> set up of master password
    -> reading entries (read into Pandas.DataFrame)
    -> look up function
        -> list all entries, way for user to select
        -> up and down arrows and enter for selection ?
    -> update_email for entrys
    -> allow duplicates
    -> add better command handler
        -> dict -> map to functions
        -> introduce global variables for command and arguments
'''

from commands import *
from constants import *
import config
from input_handler import split_first

COMMANDS = {
    EXIT: lambda: exit(),
    NEW: lambda: new_password(),
    UPDATE: lambda: update_password(),
    GET_PASSWORD: lambda: get_password(),
    GET_USER_NAME: lambda: get_user_name(),
    UPDATE_KEY: lambda: update_master_key(),
    RESET: lambda: reset(),
    REMOVE: lambda: remove(),
    HELP: lambda: help(),
    LIST: lambda: list_entries()
}

def command_handler(command):
    '''
        Function to handle calls to available commands.
    '''
    if config.arguments != None:
        config.arguments = config.arguments.strip()

    COMMANDS.get(command, lambda: print('Invalid command.'))()
    
    
def main():
    try:
        config.init_data()

        while True:
            command, config.arguments = split_first(input(PROMPT))

            command_handler(command)

    except KeyboardInterrupt:
        print('Program interrupted, saving data and exiting.')
        exit()

if __name__ == '__main__':
    main()