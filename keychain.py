'''
    TODO
    -> reading entries (read into Pandas.DataFrame)
    -> look up function
        -> list all entries, way for user to select
        -> up and down arrows and enter for selection ?
    -> allow duplicates
'''

import config
from constants import PROMPT
from input_handler import split_first
from command_handler import command_handler
    
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