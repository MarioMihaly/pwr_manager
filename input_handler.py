from constants import *
import config

def yes_or_no(prompt_msg):
    a = input(prompt_msg)
    if a in ['y', 'Y']:
        return True
    elif a in ['n', 'N']:
        return False
    else:
        print(f'Invalid choice {a}')
        yes_or_no(prompt_msg)

def enter_master_key(prompt_msg):
    master_key_in = input(prompt_msg)
    while master_key_in != config.private_key_enc and master_key_in != CANCEL:
        print(f'Invalid master key! Type "{CANCEL}" to stop process.')
        master_key_in = input(prompt_msg)

    if master_key_in == config.private_key_enc:
        return True

    return False