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

from commands import *
from constants import *
from config import init_data


def command_handler(command, arguments):
    '''
        Function to handle calls to available commands.
    '''
    if arguments != None:
        arguments = arguments.strip()

    if command == EXIT:
        exit()

    elif command == NEW:
        new_password(arguments)

    elif command == UPDATE:
        update_password(arguments)

    elif command == UPADATE_KEY:
        update_key()

    elif command == RESET:
        reset()

    elif command == REMOVE:
        remove(arguments)

    elif command == HELP:
        help()

    else:
        print('Invalid command')
    
def main():
    try:
        init_data()

        while True:
            input_str = input(PROMPT)
            command, arguments = input_str.split(' ', 1) if ' ' in input_str else (input_str, None)

            command_handler(command, arguments)

    except KeyboardInterrupt:
        print('Program interrupted, saving data and exiting.')
        exit()

if __name__ == '__main__':
    main()