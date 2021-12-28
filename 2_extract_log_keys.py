import os
import re
import base64
import project_legend

SEQUENCES = project_legend.SEQUENCES
DELIMITER = project_legend.DELIMITER
DATASET_FILE = './logs/cowrie_dataset_20210501'

seqs = os.listdir(SEQUENCES)


def process_log_messages(sequence):
    """
    Extracts the free parameters out of log messages,
    attempts on deobfuscating and stores the result as list
    of structure: [sequence_id, timestamp, log_key, free_parameter]
    if there is no free parameter, the entry is marked 'NaN'

    to do: add more free parameter extractions
    """
    with open(SEQUENCES + sequence, 'r') as r:
        content = r.read().splitlines()
        parsed_content = []

        for line in content:
            parsed_line = line.split(DELIMITER)
            if "base64" in str(parsed_line):
                parsed_line = decode_base64(parsed_line)

            #grep '[Mm]iner'
            #wget -q
            #$(which ls)
            if "echo" and '"' in parsed_line[1]:
                tag = '"'
                log_key, parameter = extract_parameter(parsed_line[1], tag, tag)
                log_data = [parsed_line[0], log_key, parameter]
            else:
                parameter = ["NaN"]
                log_data = [parsed_line[0], parsed_line[1], parameter]

            parsed_content.append(log_data)

    return parsed_content


def extract_parameter(log_message, opening_tag, closing_tag):
    free_params = re.findall(r'\"(.+?)\"', log_message)
    for text in free_params:
        new_log_message = log_message.replace('\"%s\"' % text, '%s%s' % (opening_tag, closing_tag))
    return new_log_message, free_params


def decode_base64(command_data):
    """
    Decodes the obfuscated part of the command, if present
    """
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


def write_to_data_set(processed_sequence, seq_id, target_file):
    datapoint = seq_id
    with open(target_file, 'a+') as f:
        for line in processed_sequence:
            datapoint += (DELIMITER + str(line))
        f.writelines(datapoint + '\n')


def process_all(sequences):
    for seq in sequences:
        processed_seq = process_log_messages(seq)
        for line in processed_seq:
            write_to_data_set(line, seq, target_file=DATASET_FILE)


