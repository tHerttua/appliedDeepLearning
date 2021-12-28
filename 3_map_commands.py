from os import path
import project_legend

DATASET_FILE = './logs/cowrie_dataset_20210501'
COMMANDS_FILE = "./command_mappings/command_mapping.txt"
VECTORIZED_DATA = './dataset/cleaned20210501.csv'
DELIMITER = project_legend.DELIMITER


def load_data(path_to_file):
    parsed_data = []
    with open(path_to_file, 'r') as r:
        cowrie_data = r.read().splitlines()
    for aline in cowrie_data:
        new_line = aline.split(DELIMITER)
        parsed_data.append(new_line)
    return parsed_data


def get_unique_commands(dataset):
    all_commands = []
    for entry in dataset:
        all_commands.append(entry[2])
    set_of_cmd = set(all_commands)

    return set_of_cmd


def write_command_mapping(unique_commands, target_file):
    """
    Tries to initialize the command mappings from a file,
    otherwise creates a new list of command mappings
    """
    i = 1
    known_commands = []
    if path.exists(target_file):
        with open(target_file, 'r') as r:
            cmd = r.readlines()
            for line in cmd:
                known_commands.append(line)
        i = len(known_commands)

    if not path.exists(target_file):
        with open(target_file, 'a+') as f:
            for unique_command in unique_commands:
                f.write(unique_command + DELIMITER+(str(i)) + '\n')
                i += 1
            """
            todo: add support for new commands to be found: for example,
                  if commands are spread throughout many files,
                  new commands would be added to the current list of known commands.
            
            if len(known_commands) > 0:
                for known_command in known_commands:
                    if unique_command != known_command:
                        pass
                    else:
                        print("command not found")
                        f.write(unique_command + ", {}".format(str(i)) + '\n')
                        i += 1
            else:
            """


def assign_mapping_to_data(dataset, uniques):
    """
    Maps the data at hand using command - key mapping generated from write_command mapping,
    or maps the data using set from get_unique_commands method

    :param dataset: the preprocessed dataset from 2_extract_log_keys.py
    :param uniques: Can be either file or set
    :return: command key appended data
    """
    modified_data = []

    if type(uniques) == str:
        try:
            with open(uniques, 'r') as r:
                commands = r.readlines()
                commands = [cmd.split(DELIMITER) for cmd in commands]
                for entry in dataset:
                    for uniq_cmd in commands:
                        if uniq_cmd[0] == entry[2]:
                            entry.append(int(uniq_cmd[1].strip('\n')))
                    modified_data.append(entry)
        except NameError:
            print("Cannot open target file")
            quit()

    uniques = list(uniques)
    for entry in dataset:
        for uniq_cmd in uniques:
            if uniq_cmd == entry[2]:
                entry.append(uniques.index(uniq_cmd))
        modified_data.append(entry)
    return modified_data


def vectorize_mapped_data(mapped_data):
    """
    Uses the data with structure: [sequence_id, timestamp, log_key, parameter, command_id]
    to stitch together sequence of form: sequence_id, command_id_1 ... command_id_n
    """
    sequence_ids = []
    for datapoint in mapped_data:
        sequence_ids.append(datapoint[0])
    sequence_ids = list(set(sequence_ids))

    full_sequences = []
    for sequence_id in sequence_ids:
        sequence = []
        for datapoint in mapped_data:
            if sequence_id == datapoint[0]:
                sequence.append(datapoint[4])
        tmp = [sequence_id]
        for element in sequence:
            tmp.append(element)
        full_sequences.append(tmp)

    return full_sequences


def write_vectors_into_file(v_data):
    with open(VECTORIZED_DATA, 'w+') as f:
        for entry in v_data:
            data_string = entry[0]
            for element in entry[1:]:
                data_string += ", "+str(element)
            f.write(data_string+"\n")


def add_padding(target_file):
    """
    Incomplete.
    Make all vectorized commands fixed size
    """
    import csv
    longest_row = 0
    with open(VECTORIZED_DATA, newline='') as csvfile:
        dataset = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in dataset:
            if len(row) > longest_row:
                longest_row = len(row)
        for row in dataset:
            while len(row) < longest_row:
                row.append(-1)
        for row in dataset:
            print(row)


def map_commands():
    cowrie_data = load_data(DATASET_FILE)
    unique_commands = get_unique_commands(cowrie_data)
    write_command_mapping(unique_commands, COMMANDS_FILE)
    mapped_data = assign_mapping_to_data(cowrie_data, COMMANDS_FILE)
    vectorized_data = vectorize_mapped_data(mapped_data)
    write_vectors_into_file(vectorized_data)


#map_commands()

#add_padding(None)
