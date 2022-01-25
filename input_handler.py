from constants import CANCEL, PROMPT
from getpass import getpass
from pyperclip import copy, paste

def yes_or_no(prompt_msg):
    a = input(prompt_msg)
    if a in ['y', 'Y']:
        return True
    elif a in ['n', 'N']:
        return False
    else:
        print(f'Invalid choice {a}')
        yes_or_no(prompt_msg)

def same_password(prompt_msg1 = 'Enter password: ', prompt_msg2 = 'Confirm password: '):
    password = getpass(prompt_msg1)

    # check for cancel flag
    if password == CANCEL:
        return password

    password_conf = getpass( prompt_msg2)

    while password != password_conf:
        print(f'Passwords don\'t match! Enter "{CANCEL}" to stop process.')
        password = getpass(PROMPT + prompt_msg1)

        # check for cancel flag
        if password == CANCEL:
            return password

        password_conf = getpass(prompt_msg2)

    return password

def copy_to_clipboard(value, feedback_msg=None):
    copy(value)
    paste()

    if (feedback_msg):
        print(feedback_msg)

def split_first(line, delimiter=' ', default_value = None):
    return line.split(delimiter, 1) if delimiter in line else (line, default_value)