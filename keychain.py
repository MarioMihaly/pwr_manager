'''
    TODO
    -> look up function
        -> list all entries, way for user to select
        -> up and down arrows and enter for selection ?
    -> allow duplicates
'''

import config
from constants import PROMPT, HELP
from input_handler import split_first
from command_handler import command_handler
    
def main():
    try:
        if not config.init_keychain():
            print('Login failed!')
            exit()
           
        print(f'Welcome to your password manager. Enter "{HELP}" to display available commands.') 

        while True:
            command, config.arguments = split_first(input(PROMPT))

            command_handler(command)

    except KeyboardInterrupt:
        print('\nProgram interrupted, saving data and exiting.')
        exit()

if __name__ == '__main__':
    main()