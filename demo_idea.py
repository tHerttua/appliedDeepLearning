import sys
import argparse

"""
As I didn't get the full pipeline working, it makes more sense to keep the modules as scripts and instead 
explain the idea how the demo would work:

Code draft for command line interface:
"""


def preprocess(input_file, output_file):
    """
    The input file is raw cowrie log file.
    The sequences are extracted,
    the log keys are extracted,
    the commands are mapped,
    and the processed file is saved.
    No intermediate files between the modules.
    """
    print("preprocessed {} into {}".format(input_file, output_file))


def train_model(input_file, output_location, look_back=3, hidden_nodes=10, epochs=5):
    """
    The model is trained using a preprocessed file and user provided hyper-parameters,
    saves the models into user-defined location.
    """
    print("trained model using {}, saved to {}".format(input_file, output_location))



def predict(input_file, models_path):
    """
    Unseen data is fed to the array of models.
    After attempting to predict the steps of the sequence,
    makes decision on how abnormal the sequence is and
    if the sequence is abnormal, writes it down in a file.
    If the sequence is considered non-abnormal based on a
    novelty factor, it's indexed and mapped.
    """
    print("predicting using data {} and models {}".format(input_file, models_path))


parser = argparse.ArgumentParser()

parser.add_argument('--preprocess', type=str, nargs='+',
                    help='Input file must be raw cowrie file. The output is csv with commands as sequences')
parser.add_argument('--train_model', type=str, nargs='+',
                    help='Input file must be a file preprocessed with this program '
                         '[file, look_back, hidden_nodes, epochs]')
parser.add_argument('--predict', type=str, nargs='+',
                    help='Input file must be a file preprocessed with this program')


args = parser.parse_args()

try:
    if args.preprocess:
        preprocess(sys.argv[2], sys.argv[3])
    if args.train_model:
        train_model(sys.argv[2], sys.argv[3])
    if args.predict:
        predict(sys.argv[2], sys.argv[3])
except Exception as e:
    print("Make sure you've correct amount of variables")
    print(e)

