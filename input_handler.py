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

def enter_master_key3():
    '''
        Function to verify master key from initial + 3 attempts.
    '''

    # Prompt for master key, exit after 3 attemtps
    attempt_max = 3
    attempt_count = 0

    master_key = input(PROMPT + 'Enter master key: ')
    
    if master_key != config.private_key_enc:
        print(f'Invalid master key! {attempt_max - attempt_count} attempt(s) remaining.')
        master_key = input(PROMPT + 'Enter master key: ')
        attempt_count += 1

        while attempt_count < attempt_max and master_key != config.private_key_enc:
            print(f'Invalid master key! {attempt_max - attempt_count} attempt(s) remaining.')
            master_key = input(PROMPT + 'Enter master key: ')
            attempt_count += 1

    if attempt_count >= attempt_max:
        return False

    return True

def same_password(prompt_msg1 = 'Enter password: ', prompt_msg2 = 'Confirm password: '):
    # TODO: handle case when wish to cancel

    password = input(PROMPT + prompt_msg1)

    # check for cancel flag
    if password == CANCEL:
        return password

    password_conf = input(PROMPT + prompt_msg2)

    while password != password_conf:
        print(f'Passwords don\'t match! Enter "{CANCEL}" to stop process.')
        password = input(PROMPT + prompt_msg1)

        # check for cancel flag
        if password == CANCEL:
            return password

        password_conf = input(PROMPT + prompt_msg2)

    return password

def split_first(line, delimiter=' ', default_value = None):
    return line.split(delimiter, 1) if delimiter in line else (line, default_value)