# Assignment 3 - Delivery

## Introduction

This project tackles the problem of detecting bot generated commands from the ones created by naturals persons.
Under consideration are logs created by a honeypot systems, which gathered log data over two weeks in May 2021.
In short honeypots are fake filesystems that are exposed with weak credentials to allow adversaries to enter the system.
There are many different kinds of honeypots and here the honeypot was allowed ssh connections.

The problem with doing explorative analysis on honeypots is the sheer velocity of the log data. There are a lot of 
similar entries with a slight variance, and amidst all the bot generated log entries, it's hard to find out which
entries might've been created by natural persons. 

Bots have different goals such as downloading certain ransomware, or trying to harness the server's cpu for mining
purposes, and thus their behaviour is predetermined. This means that as long as we can learn their patterns we can
use deep learning to try and predict the next command in session sequence. If the next command is in the n-top 
candidates between different predictions, we can assume the user is either a bot (and at the very least something 
we are already familiar with, and don't care of). While using a command line is quite straight forward, natural persons
most likely could have different motives and execute the commands in more "random" order to reach their goals.

One problem we face already before attempting to implement such system are the new type of bots that might emerge.
However, this is not really a problem from cyber security perspective, if we can capture an all new type of bot attack.
Also, a solution to avoid these new type of command sequences from filling the new logs, is to introduce some sort of
novelty weight heuristic: after having seen similar sequence, it would be written to a retentive registry and labeled
as a bot.

Deep learning, is a boon to this sort of problems, namely log anomaly detection. In this project the intial idea
was to use transformers, as it would've provided some needed features such as embedding and runtime feedback ().
However, due to complexity the idea was scrapped and now the model is LSTM based.


## Preprocessing
The most hours were used in preprocessing part as there were many challenges.
The data itself was semi-structured and in JSON-format, and there were a lot of columns (which are shown for reference
in 'project_legend.py' file as a list), and so data manipulation was needed to create command sequences:

### 1. Extract sequences
one entry in the log contains only one sort of data labeled with eventID (these can be also seen for reference in 
'project_legend.py' file as a list). So one session has multiple events, and there can be multiple of the same sort of 
events: the first task was to use session id to extract all the entries of same session, that have command line input
in them to recreate the session as sequence. To achieve this, all the data was loaded into pandas dataframe and the 
code uses SQL queries to recreate the sessions. For just one day, there was over 280 000 entries in total, out of which
just over 29 000 were command line entries; over two weeks there was roughly four million entries but in this proof
of concept, we first attempted building the pipeline using one day's log.
The intermediate result is then saved as a csv file for the next step.

### 2. Extract log keys
After which, the command entries had to be cleaned. There were obfuscation of the code for example with base64,
and as it was the most common, it was the only form of obfuscation decoding used for in this implementation.
Other potential oddities to clean up are command flags and character case (Hendler et al, 2018).

When the cleaning is done, each log entry is parsed to log key and log parameter vectors. 
For example, in the command "echo 'hi'", [echo] is the log key and ['hi'] is the log parameter.
The intermediate result is then saved as a csv file for the next step.

### 3. Map commands
In this part the commands are indexed and mapped. 
All the cleaned commands are read, and out of them, the unique ones are listed. The list is used to write down a 
retentive list with commands simply mapped starting form 1 in order of appearance. 
Then, the mapping is used on data with structure: [sequence_id, timestamp, log_key, parameter, command_id]
to stitch together sequence of form: [sequence_id, command_id_1, ..., command_id_n].
And these sequences are then saved as our final dataset to be used for training the model.
(Interestingly enough, between over 29 000 command inputs, the list of unique commands was only 37.)

## The model training and prediction
The model is created and adapted after the deep log model described in Du's paper. It uses look back
to create features vectors that yield the output vector. So one for one sequence there is a matrix of steps
how to approach at outputs for example sequence full sequence [1 4 6 8 9] with look back 2 turns into:
      X   Y
    [1,4][6]
    [4,6][8]
    [6,8][9]
However, as the data is multiple independent sequences, it creates a problem on how to train an LSTM model
for it. Solution attempted for this problem was to train a model for each of the sequences and in the prediction step, 
use each of the models to predict an outcome, and the one with the highest score would be chosen.
This solution didn't get finalized because of the time constraints, and some bugs that were arduous to debug.
The LSTM model uses softmax activation, as it makes sense to scale the input into probabilities, and as loss function,
the model uses categorical entropy loss as this is type of multi-class classification problem.
The optimizer is 'adam' by default as it is popular adaptive learning rate optimizer.
 
More elegant way would've been Multiple Parallel Input and Multi-Step Forecast suggested by Halil Ertan. 
In the blog Ertan had the exact same problem at hand, except Ertan was trying to create one single model that would deal
with forecasting between many locations (Ertan, 2021). Because the problem was similar but slightly different, there
was no time to delve into it more and hack it to fit the purposes and needs of the problem at hand.

It was not implemented yet but:
Lastly, when the model finds abnormal entries, they're tracked by the session id and written into a special logs file.
The abnormal entries are considered based their novelty factor, if they should be indexed and mapped into known 
commands and mapped into the retentive memory. This way the model keeps track of all new bot attacks.

## Results
Unfortunately the project realization fell short due to lack of knowledge and lack of time.
The idea was to try out how different look back values in the training would affect the prediction; what is the
optimal amount of prior commands to consider. Also, testing out if Adam, the adaptime moment estimation optimizer
would've yielded better results over SGD optimizer. Also, finding out the optimum for other hyper parameters.

### Next time
This project taught a lot about feature engineering. It made me consider how to manipulate the data to make it useful
for my model. It also made delve into considering different approaches and gain better understanding of the pros and 
cons of certain models. 
If I had more time, I'd want ot finalize this approach using model checkpoints and then, being better equipped, 
try out the approach with transformers, as manipulating the data made me understand the data better.


### The amount of time spent on each task, according to work breakdown structure
- Preprocessing the data             - 30h 
- Technique research and selection   - 20h 
- Fine-tuning & results gathering    - 30h 
- Presentation and documentation     - 8h+ (on going)

All together the project took more time than anticipated. 
The preprocessing had to be tailored specifically for LSTM as sequences (and at for first transformers).
As the data was already in semi-structured format, the impression was that it would be quite straight forward,
but in reality it turned out that there were many challenges and decisions to consider when manipulating the data.


## Sources

Du M., Li F., Srikumar V., Zheng G. 2017 DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning.
School of Computing, University of Utah (Available: https://www.cs.utah.edu/~lifeifei/papers/deeplog.pdf)

Ertan, H. 2021, CNN-LSTM-Based Models for Multiple Parallel Input and Multi-Step Forecast. Towards Datascience.
(Available: https://towardsdatascience.com/cnn-lstm-based-models-for-multiple-parallel-input-and-multi-step-forecast-6fe2172f7668)

Hendler D., Kels S., Rubin A. 14.4.2018. Detecting Malicious PowerShell Commands using Deep Neural Networks.
(Available: https://arxiv.org/pdf/1804.04177.pdf)

