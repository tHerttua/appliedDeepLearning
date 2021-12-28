import os
import codecs
import base64
import re
import pandas as pd

path_to_files = '../tty/'
TTY_FILES = os.listdir(path_to_files)
COMMANDS_FILE = '../commands_data/commands.csv'
DELIMITER = " -|::|- "
COMMON_COMMANDS = [ "chpasswd",
                    "Enter new UNIX password:",
                    "system scheduler",
                    "Enter: command not found",
                    "uname"
                   ]


def get_uncommon_commands():
    count = 0
    for tty_file in TTY_FILES:
        data_found = re.findall("[^\x00-\x1F\x7F-\xFF]{4,}", read_command(tty_file))
        flag = True

        for common_string in COMMON_COMMANDS:
            if common_string in str(data_found):
                flag = False
        if flag:
            count += 1
            tokenized_command = tokenize_command(data_found)
            write_command_to_file(tokenized_command)
    print(count)


def read_command(tty_file):
    file_name = path_to_files + tty_file
    with codecs.open(file_name, 'r', encoding='utf-8',
                     errors='ignore') as fdata:
        return fdata.read()


def split_commands(command_data):
    new_commands = []
    for command in command_data:
        commands = command.split()
        for entry in commands:
            new_commands.append(entry)
    return new_commands


def tokenize_command(data_found):
    if "base64" in str(data_found):
        split_command_list = decode_base64(data_found)
    else:
        split_command_list = split_commands(data_found)
    return split_command_list


def decode_base64(command_data):
    new_commands = []
    for command in command_data:
        commands = command.split()
        for idx, entry in enumerate(commands):
            if len(entry) > 30:
                base64_bytes = entry.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                message = message_bytes.decode('ascii')
                commands[idx] = message
        for processed_command in commands:
            new_commands.append(processed_command)
    return new_commands

def count_common_commands():
    """
    Results:
    chpasswd 9733
    Enter new UNIX password: 3884
    system scheduler 90
    Enter: command not found 3885

    uncommon commands yield 193 commands after getting rid of the useless and repeated entries,
    meaning just over one percent of the commands were "uncommon"

    It was decided to manually pick a few chpasswd commands and system scheduler commands and add them to the dataset
    """
    for common_string in COMMON_COMMANDS:
        count = 0
        for tty_file in TTY_FILES:
            data_found = re.findall("[^\x00-\x1F\x7F-\xFF]{4,}", read_command(tty_file))
            if common_string in str(data_found):
                count += 1
                print(data_found)
        print(common_string, count)


def write_command_to_file(command_data):
    index = 0
    last = len(command_data)
    with open(COMMANDS_FILE, 'a+') as f:
        for command in command_data:
            f.write(command)
            index += 1
            if index != last:
                f.write(DELIMITER)
        f.write('\n')


def read_data_set():
    dataset = pd.read_csv(COMMANDS_FILE, index_col=False, sep=DELIMITER)
    print(dataset[6])

#read_data_set()