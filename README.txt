Sean Allen - U0021994
Nick Sullivan - U0945150
Natural Language Processing - CS 5340
Term Project - Co-Reference Resolver
coreference.py


I used lab1-17 to do my testing.

We use 4 passes through the data and can achieve 62.23% score. We wrote all the code; no external algorithms were used.
 - First pass matches NP's exactly
 - Second pass matches acronyms
 - Third pass matches partial NP's
 - Fourth pass is the default pass and finds all the unmached NP's and finds a nearby NP to match with it.

The fourth pass seemed trivial, but it ended up getting us a 7% boost in performance.

We didn't use any external software. We were using nltk for python, and had a lot of data structures, but found
we were getting a pretty high return rate out of the methods we were using. We plan on using the nltk for the
second part of the assignment to get our percentage (hopefully much) higher.

We also didn't use any machine learning or external data files except we did find a list of stopwords on the
nltk site http://www.nltk.org/book/ch02.html under section 4.2. This was used in the partial match pass.

Our system take almost no time at all to run on the CADE lab machines, and there is no instructions to "teach"
our system since there is no machine learning. Our system should not crash as long as the input is exactly as
described in the assignment requirements.

The arguments in the shell script assume the program is in a folder with a filelist.txt document and a folder
called "responses". This folder must already exist, the program does not create one.