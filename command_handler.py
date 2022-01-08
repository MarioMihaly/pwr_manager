from commands import *
from constants import *
import config

COMMANDS = {
    EXIT: lambda: exit(),
    NEW: lambda: new_password(),
    UPDATE: lambda: update(),
    GET: lambda: get(),
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

    try:
        COMMANDS.get(command, lambda: print('Invalid command.'))()
    except KeyboardInterrupt:
        print('\nCommand cancelled.')
        pass