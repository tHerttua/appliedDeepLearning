# Assignment 1 - Initiate

## Project Description
This project mixes computer security themes with deep learning. 
The topic of choice is Natural Language processing and the project type is a mix between "Bring Your Own Method"
and "Bring Your Own Data".

The idea for the project comes from my earlier explorative analyses on honeypot logs. A honeypot is
a system that has been exposed to the malicious users on purpose. There's a blogpost I wrote for Oulu University Secure Programming Group
for which the link can be found in the Sources section (Herttua et al, 2020). Since, I've done other explorative analyses on the topic
such as comparing the differences between geolocations of Tokyo, London and Fremont servers.

The goal of the project is to use Cowrie honeypot's log as dataset to train a model to classify 
shell commands, and label if they're malicious or neutral for supervised learning purposes. 
A stretch goal is to classify what type of malicious behaviour the command attempts to execute,
such as downloading malicious scrupts, joining botnet for Cryptomining or DDOS and so forth.
However, there is enough challenge in just creating a system that classifies command between malicious and benign.

There are only few similar projects on the topic I could find, but Hendler et al. had similar topic at hand. 
Their text "Detecting Malicious PowerShell Commands using Deep Neural Networks", where the idea
was to use NLP and CNN techniques (and ensemble of both) to detect the malicious commands (Hendler et al., 2018).
Another interesting text I could find was "Neural Classification of Malicious Scripts: A study with
JavaScript and VBScript", where scripts were analysed using LSTM and Max Pooling, and 
Convoluted Partitioning of Long Sequences (Agrawal, 2018). Either of the text isn't exactly the same
as this project, but they include interesting findings and methods, which can most definitely used.
There was very good point in the text by Hendler et al saying that for such detector to be practical,
it must have high True Positive rate and low False Positive rat because in the domain of Cyber Security 
there are a lot of events happening (Hendler et al., 2018).

All in all, this project will be more of a proof of concept due to my limited knowledge in deep learning,
and due to the vast amount of work required. Still, I'm being optimistic as the texts I found have shown 
results and I'm familiar with reading Cowrie logs.


## Dataset Description
As mentioned, the dataset is a Cowrie honeypot system's log. The filesystem was set up on CSC Pouta server,
which is provided by a Finnish non-profit state enterprise which is part of the national research system.
The dataset s network traffic data gathered in the time span of two weeks from the 1st of April in 2021 until the
14th of April 2021. The honeypot was configured to have port 22 open to expose it for ssh connections and it was also set
to have plenty of weak credentials. Whenever there was a network event happening, such as login attempt, it would be written
in the log. The data is high volume and it had high velocity. Over the two weeks it had logged over 17000 command line entries.
The data is semi-structured as the Cowrie logs are in JSON-format with one of the attributes containing full shell command,
if there was such for that certain event.

The amount of preprocessing of the data is huge. Some of the biggest challenges is labeling and normalizing the data.
As the honeypot was made vulnerable with several attack vectors exposed, large amount of the command line inputs are malicious,
with only a fraction of them being benign and useful. Therefore, a separate set of command line inputs must be gathered to
balance out the data. This also makes the labeling easier but great care must be taken with data leakage such as repeated commands,
command input length, and obfustacted commands. Even when labeling the data sets as explained and mixing them together, 
manual validation is needed. 

## Project Plan
It is not yet clear which portion of the dataset should be used and how it should be sampled. The project will begin with
explorative analysis on finding what portion of the commands are similar and what sort of preprocessing is needed for this task. 
Then appropriate techniques will be explored and selected, and after that the training can begin.

Roughly the plan is to use time with following plan:
- Preprocessing the data             - 3 weeks 
- Technique exploration & selection  - 5 weeks
- Fine tuning & results gathering    - 2 weeks
- Preparing for the presentation     - 2 weeks


## Sources

Agrawal R., McDonald G., Stokes J. 15.5.2018. Neural Classification of Malicious Scripts: A study with
JavaScript and VBScript. (Available: https://arxiv.org/pdf/1805.05603.pdf)

Hendler D., Kels S., Rubin A. 14.4.2018. Detecting Malicious PowerShell Commands using Deep Neural Networks.
(Available: https://arxiv.org/pdf/1804.04177.pdf)

Herttua T., Kettunen J., Jomppanen J., Rytinki S. 10.2.2020. Honeypots - Easy and Insightful. OUSPG 
(Available: https://medium.com/ouspg/honeypots-easy-and-insightful-9d98d2be01c0)
