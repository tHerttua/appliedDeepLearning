# Assignment 2 - Hacking

## Project Introduction

The initial goal of the project is to use Cowrie honeypot's log as dataset to train a model to classify 
shell commands, and label if they're malicious or neutral for supervised learning purposes.
However, it was changed to find which log entries are created by human user amongst the massive amount of
log messages created by bot activity.
In short the problem got simplified and became more concise, and became a log anomaly detection problem;
The assumption is that the logs will get filled by similar sequences of commands produced by bots, 
whereas human users would have more variation in their input sequences.

## Project Overview & Changes

The initial idea was to use transformers with multi-headed attention to detect anomalies in logs.
To achieve this, an input embedding must be made to map a command into a vector, and positional encoder to
give context info based on the position of the command in the sequence. Also, encoder block, that incorporates the
multiheaded attention layer to guide the attention, needs to be implemented. Then a feed forward network
to is needed to be applied to every attention vector to transform attention vectors for next encoder block. 
Finally, a decoder predicts the next command in a sequence (which includes self-attention block and encoder-decoder 
attention blocks) The idea and structure are made after the recent text by Guo et. Al in which the authors attempts 
to answer the drawbacks of known log anomaly detection techniques using a multi-head self-attention based sequential 
model to process log streams with sequential information (Guo et. Al, 2021).

As the idea above was in the making, it became apparent that it wouldn't get finalized and that it was too complex
of a system to be built and as there are no existing libraries to achieve the same for this problem at hand. 
This is because, after trying to preprocess the logs in meaningful way, it became apparent the aim of the preprocessing
the log entries is different: In the problem at hand the focus is on a full command entry, and in Guo et. Al text
the focus is at character level, meaning it would roughly double the amount of hours needed for preprocessing and
creating the input embedding.

Instead the focus was shifted at last minutes to LSTM approach; deep log by Duo et. Al. 
In the problem at hand, series of command line entries can be extracted from the logs and stitched together by their
session ID, to create sequence of commands. The assumption is that bots use predetermined set of commands and so, 
the LSTM model learns the common sequences and those, which differ from the normal, are deemed abnormal and possibly 
entered by a human adversary.
Each log entry is parsed to log key and log parameter vectors. For example, for command "echo 'hi'" 
[echo] is the log key and ['hi'] is the log parameter.
The trained model attempts to predict the next command in the sequence and if the next true command is not 
in the predicted n commands, the entry is deemed abnormal (Duo et. Al 2017).


### Preprocessing
The preprocessing part of the application is written in the scripts 1, 2 and 3. 
1. Extract sequences: uses SQL queries on pandas dataframe, which is made of the log entries, that are in JSON format
2. Extract log keys: separates the possible free parameters from log messages. Such as: 'echo hi' -> key:'echo' param:'hi'
3. Map commands: lists the unique commands and gives them unique id's, further creates sequences of commands for the model

### The model
The model is created and adapted after the deep log model described in Du's paper. It uses look back
to create features vectors that yield the output vector. So one for one sequence there is a matrix of steps
how to approach at outputs for example sequence full sequence [1 4 6 8 9] with look back 2 turns into:
      X   Y
    [1,4][6]
    [4,6][8]
    [6,8][9]
However, as the data is multiple independent sequences, it creates a problem on how to train an LSTM model
for it. One solution could be to train a model for each of the sequences and in the prediction step, 
use each of the models to predict an outcome, and the one with the highest score would be chosen.
In the paper, Du et. Al mention a density based clustering with co-occurence matrix for multivariate time series 
data anomaly detection problem (Du et. Al 2017) but it is uncertain how it would be implemented for this problem.

## Deliverables

### Results so far
The error metrics chosen for this task were FP and TP.
These metrics were chosen because of the similar reason Hendler talked about in his text, namely,
because in the domain of Cyber Security there are a lot of events happening (Hendler et al., 2018).
In this application, the data velocity is so high and only truly unique sequences would be of actual interest.

As the target metrics for this project the following were chosen: precision 0.90, recall 0.90, f-measure 0.90
The scores attained by deep log model by Du et. Al. were precision 0.95, recall 0.96, f-measure 0.96,
and it was decided that if this project's model could come even to close to the values of deep log,
it would be satisfactory.

In the end no error metrics could be gotten out of the current state of this project as I failed to stitch together
a working pipeline.

### The amount of time spent on each task, according to work breakdown structure
- Preprocessing the data             - 30h 
- Technique research and selection   - 20h 
- Fine tuning & results gathering    - 20h (on going)
- Preparing for the presentation     - not started


## Sources

Brownlee J. 21.7.2016. Time Series Prediction with LSTM Recurrent Neural Networks in Python with Keras. 
Machine Learning Mastery. (Available: https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/)

Du M., Li F., Srikumar V., Zheng G. 2017 DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning.
School of Computing, University of Utah (Available: https://www.cs.utah.edu/~lifeifei/papers/deeplog.pdf)

Guo Y., Lian Y., Jian C., Wan Y., Wen Y. 2021. Detecting Log Anomalies with Multi-Head Atention (LAMA). 
Huawei Technologies (Available: https://arxiv.org/pdf/2101.02392.pdf)

Hendler D., Kels S., Rubin A. 14.4.2018. Detecting Malicious PowerShell Commands using Deep Neural Networks.
(Available: https://arxiv.org/pdf/1804.04177.pdf)

