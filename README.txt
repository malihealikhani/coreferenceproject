Sean Allen - U0021994
Nick Sullivan - U0945150
Natural Language Processing - CS 5340
Term Project - Co-Reference Resolver
coreference.py


I used lab1-5 to do my testing.

We use 9 passes through the data and can achieve 65.15% score with all of the data that we have been given. We wrote all the code; no external algorithms were used.
 - First pass matches NP's exactly
 - Second pass matches related pronouns that are used together (he/his,we/our,etc) 
 - Third pass matches acronyms
 - Fourth pass matches partial NP's
 - Fifth pass removes "'s" from Nouns and then checks for exact matches
 - Sixth pass matches dates in different formats
 - Seventh pass looks to add anchors and match corefs to text that is not already tagged
 - Eighth pass looks to match appositives
 - Ninth pass is the default pass and finds all the unmached NP's and finds a nearby NP to match with it.

We didn't use any external software. 

We also didn't use any machine learning or external data files except we did find a list of stopwords on the
nltk site http://www.nltk.org/book/ch02.html under section 4.2. This was used in a few of the passes.

Our system takes almost no time at all to run on the CADE lab machines, and there is no instructions to "teach"
our system since there is no machine learning. Our system should not crash as long as the input is exactly as
described in the assignment requirements.

The arguments in the shell script assume the program is in a folder with a filelist.txt document and a folder
called "responses". This folder must already exist, the program does not create one.
