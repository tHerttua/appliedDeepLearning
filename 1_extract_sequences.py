import pandas as pd
from pandasql import sqldf
import project_legend

"""
This script uses pandas' dataframe and pandas' SQL query to extract the needed data
from the semi structured log files that cowrie produces 
"""

PATH = './logs/'
TO_FILE = 'cowrie.json.cowrie-2021-05-01'

SEQUENCES = project_legend.SEQUENCES
DELIMITER = project_legend.DELIMITER

df = pd.read_json(PATH+TO_FILE, lines=True)
df = df.applymap(str)


def find_successful_commands():
    query = "SELECT timestamp, eventid, session, input " \
            "FROM df " \
            "WHERE eventid = 'cowrie.command.input'"
    output = sqldf(query)

    return output


def find_session_ids():
    query = "SELECT DISTINCT session " \
           "FROM new_df "
    output = sqldf(query)
    sessions_list = output["session"].tolist()

    return sessions_list


def find_sequence_by_id(session_id):
    query = "SELECT timestamp, input " \
            "FROM new_df " \
            "WHERE eventid = 'cowrie.command.input' " \
            "AND session = '{}'".format(session_id)
    output = sqldf(query)

    return output


def write_sequence_into_file(sequence_list, timestamp_list, session_id):
    for timestamp, command_entry in zip(timestamp_list, sequence_list):
        #SEQUENCES+session_id
        with open('logs/cowrie-2021-05-01', 'a+') as f:
            f.write(session_id + DELIMITER + timestamp + DELIMITER + command_entry + "\n")



new_df = find_successful_commands()
sessions = find_session_ids()

for session in sessions:
    print("Working on {}".format(session))
    sequence = find_sequence_by_id(session)
    seq_list = sequence["input"].tolist()
    ts_list = sequence["timestamp"].tolist()

    write_sequence_into_file(seq_list, ts_list, session)


