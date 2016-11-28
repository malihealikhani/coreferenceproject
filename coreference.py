################################################################################
#
# Sean Allen - U0021994
# Nick Sullivan - U0945150
#
# Natural Language Processing - CS 5340
# Term Project - Co-Reference Resolver
# coreference.py
#
################################################################################

import xml.etree.ElementTree as ET
import sys
import re
# import nltk
import os

################################################################################
#
# Main Function
#
# Parameters: File with the list of programs to use and directory where output should go
# Returns: Creates a response file for each file processed
# Notes: Loops through each file on the provided list and runs co-reference on it
#
################################################################################


def main(files):

    listfile, responsedir = files

    for file in list(open(listfile)):
        file_path = os.path.splitext(file)[0]
        file_name = os.path.basename(file_path)
        response = responsedir + file_name + '.response'
        with open(response, 'w') as f:
            f.write(coreference(file.rstrip()))


################################################################################
#
# Format Output
#
# Parameters: Data structure with tagged references, their coref id, and ref id
# Returns: Properly formatted string ready to write to file
# Notes:
#
################################################################################


def format_output(coref):

    output = '<TXT>\n'
    for c in coref:
        if len(c) is 2:
            output += r'<COREF ID="' + c[0] + '">' + c[1] + '</COREF>\n'
        elif len(c) is 3:
            output += r'<COREF ID="' + c[0] + '" REF="' + c[2] + '">' + c[1] + '</COREF>\n'
    return output + '</TXT>'


##################################################################################
#
# Co-Reference Method
#
# Parameters: The name of a .crf file to be processed
# Returns: Data structure with tagged references, their coref id, and ref id
# Notes: The slides on co-reference contain the following: Typical Co-reference
#        Pipeline -Preprocessor: XML removal, tokenization, sentence and paragraph
#        splitting -Part of Speech Tagging -Parsing -Named Entity Recognizer
#        -Semantic Class Lookup (usualy via WordNet) -Candidate NP extraction
#        -Supervised Learning -Clustering into Chains
#
##################################################################################

def coreference(f):

    # Create data structures
    with open(f, 'r') as file:
        unedited = file.read()
    tree = ET.parse(open(f))
    tree_root = tree.getroot()
    coref = create_coref(tree_root)
    notags = ET.tostring(tree_root, encoding='utf8', method='text')
    no_coref = re.sub('<.+>.+<.+>', '', unedited)

    #Nick's Version of no_coref
    notref = tree_root.text + str(tree_root.tail)
    for child in tree_root:
        notref+= str(child.tail)
    
    notref = notref.lower()
    
    # text = nltk.word_tokenize(notags)  # breaks up all the words into tokens and puts into a list
    # sentences = nltk.sent_tokenize(notags)  # breaks corpus into sentences
    # pos_tags = nltk.pos_tag(text)  # tags all the words in the corpus
    # tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'WP', 'WP$']
    # nouns = [noun for noun in pos_tags if noun[1] in tags]  # just the nouns, pronouns
    # grammar = r'''
    #     NP: {(<NN><IN>)?<DT|PP$>?<JJ.*>*<NN.*>+<POS>?<NN.*>*}
    #         {<NN.+>+}
    #         {<PRP>}
    #         {<WP|WP$>}
    # '''
    # cp = nltk.RegexpParser(grammar)
    # chunked = cp.parse(pos_tags)

    # check head noun match
    # check word overlap comparisons
    #
    # Check Lexical Similarity
    # i.e. Ford Motor Company = Ford Co. = Ford
    # i.e. Apple Computer = Apple
    # i.e. Federabl Bureau of Investigation = FBI

    # Look through candidate list of Nouns checking using
    # scoping heuristics and recency
    # number, person, and gender agreement
    # sytactic heuristics
    # semantic compatability

    
    #Order 1
    #coref = checkExactMatch(coref)
    #coref = checkUntagged(coref, unedited)
    #coref = checkAcronym(coref)
    #coref = checkPartialMatch(coref)
    #coref = checkExactMatchNoS(coref)
    #coref = check_appositive(coref)
    #coref = checkDateMatch(coref)
    #coref = addDefault(coref)
    
    #Order 2 has accuracy of 0.6259
    coref = checkExactMatch(coref)
    coref = checkAcronym(coref)
    coref = checkPartialMatch(coref)
    coref = checkExactMatchNoS(coref)
    coref = checkDateMatch(coref)
    coref = checkNotTagged(coref,notref)
    coref = check_appositive(coref)
    coref = addDefault(coref)

    return format_output(coref)

################################################################################
#
# Create coref
#
# Parameters: xml data structure with all the tagged references
# Returns: Data structure with tagged references and their coref id
# Notes: coref is the primary data structure for this program
#
################################################################################


def create_coref(root):
    coref = []
    for child in root:
        text = child.text

        # removes new lines in the middle of a string
        if "\n" in text:
            text = text[:text.index("\n")] + " " + text[text.index("\n")+1:]

        coref.append([str(child.get('ID')), text.lower()])
    return coref


################################################################################
#
# Check Exact Match
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and some ref id's
# Notes: This finds all the exact matches in a corpus and adds the ref id to coref
#        It searches for matches starting at the coref closest and moves out
#
################################################################################


def checkExactMatch(coref):
    cnt = 0
    for i in range(len(coref)):
        word1 = coref[i][1]
        a = 0
        # s = 1
        for j in range(len(coref)):
            if (i - a) < 0:
                k = i + a
                a += 1
            else:
                if j % 2 == 0:
                    k = i + a
                    a += 1
                else:
                    k = i + (a * -1)
                    
            if k > (len(coref) - 1):
                k = i + (a*-1)
                a += 1

            word2 = coref[k][1]
            
            if word1 == word2 and coref[i][0] != coref[k][0]:
                if len(coref[i]) is 2:
                    coref[i].append(coref[k][0])
                    cnt += 1
                    break       
    return coref


def checkUntagged(coref, unedited):
    cnt = 0
    for i in range(len(coref)):
        if len(coref[i]) == 2:
            if coref[i][1] in unedited:
                coref.append(['X'+str(cnt), coref[i][1]])

                cnt += 1
    return coref

################################################################################
#
# Check Exact Match no 's
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and some ref id's
# Notes: This finds all the exact matches in a corpus and adds the ref id to coref
#        It searches for matches starting at the coref closest and moves out
#
################################################################################


def checkExactMatchNoS(coref):
    cnt = 0
    for i in range(len(coref)):
        a = 0
        s = 1
        for j in range(len(coref)):
            if (i - a) < 0:
                k = i + a
                a += 1
            else:
            
                if j % 2 == 0:
                    k = i + a
                    a += 1
                else:
                    k = i + (a*-1)
                    
            if k > (len(coref) -1):
                k = i + (a*-1)
                a += 1

            word1 = coref[i][1]
            word2 = coref[k][1]
            
            # If the coref ends in 's, remove it before the comparison
            if word1[-2:] == "'s":
                word1 = word1[:-2]
            
            if word2[-2:] == "'s":
                word2 = word2[:-2]
            
            if word1 == word2 and coref[i][0] != coref[k][0]:
                if len(coref[i]) is 2:
                    coref[i].append(coref[k][0])
                    cnt += 1
                    break
            
    return coref


################################################################################
#
# Check Appositive Adjacent
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and some ref id's
# Notes:
#
################################################################################

def check_appositive(coref):
    for i in range(len(coref)):
        if len(coref[i]) == 2:
            if i+2 <= len(coref):
                if len(coref[i+1]) == 2:
                    coref[i].append(coref[i+1][0])
                    coref[i+1].append(coref[i][0])

    return coref


################################################################################
#
# Check Acronym
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and some ref id's
# Notes: This checks acronyms against all possible matches and adds ref id to coref
#
################################################################################


def checkAcronym(coref):
    skip = ["and", "or", "in", "of", "&"]
    for i in range(len(coref)):
        if len(coref[i]) is 2:
            acr1 = ""
            acr2 = ""
            # This finds references from acronyms (FAA finds Federal Aviation Administration)
            if len(coref[i][1].split(" ")) is 1:
                for j in range(len(coref)):  # for j in range(i, -1, -1):
                    if len(coref[j][1].split(" ")) is len(coref[i][1]):
                        for word in coref[j][1].split():
                            if word.lower() not in skip:
                                acr1 += word[0]
                            acr2 += word[0]
                        if acr1 == coref[i][1] or acr2 == coref[i][1]:
                            if coref[i][0] != coref[j][0]:
                                coref[i].append(coref[j][0])
            # This finds acronyms from references (Federal Aviation Administration finds FAA)
            else:
                for word in coref[i][1].split():
                    if word.lower() not in skip:
                        acr1 += word[0]
                    acr2 += word[0]
                for j in range(len(coref)):  # for j in range(i, -1, -1):
                    if coref[j][1] == acr1 or coref[j][1] == acr2:
                        coref[i].append(coref[j][0])
    return coref


################################################################################
#
# Check Partial Match
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and some ref id's
# Notes: This finds all the partial matches in a corpus and adds the ref id to coref.
#        This method makes a lot of mistakes, but makes more correct matches than
#        incorrect.
#
################################################################################


def checkPartialMatch(coref):
    #from nltk.corpus import stopwords
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
                    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
                    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    #stopwords = stopwords.words('english')
    for i in range(len(coref)):
        a = 0
        s = 1
        for j in range(len(coref)):
            if (i - a) < 0:
                k = i + a
                a += 1
            else:
            
                if j % 2 == 0:
                    k = i + a
                    a += 1
                else:
                    k = i + (a * -1)
                    
            if k > (len(coref) - 1):
                k = i + (a * -1)
                a += 1
                
            if i != k:
                
                words1 = coref[i][1].split(" ")
                words2 = coref[k][1].split(" ")

                # only proceed if at least one phrase is multiple words
                if len(words1) > 1 or len(words2) > 1:
                    # for each word in word1
                    for word1 in words1:
                        # only proceed if word is not a stopword
                        if not(word1 in stopwords):
                            for word2 in words2:
                                if word1 == word2:
                                    if len(coref[i]) == 2 and coref[i][0] != coref[k][0]:
                                        coref[i].append(coref[k][0])
    return coref


################################################################################
#
# Add Default
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and all ref id's
# Notes: This is the last resort. If a NP hasn't been resolved, then this will
#        add a ref id of a nearby NP. Suprisingly, this bumped our score by
#        about 5-7% No need to add reference to the X refs
#
################################################################################


def addDefault(coref):
    for i in range(len(coref)):
        if i > 1:
            if len(coref[i]) is 2:
                if coref[i][0][0] != "X":
                    j = coref[i-1][0]
                    coref[i].append(j)
    return coref







################################################################################
#
# Check Not Tagged
#
# Parameters: coref data structure (see create coref), 
# Returns: Data structure with tagged references, their coref id and all ref id's
# Notes: Checks the untagged text for a match
#            
#
################################################################################


def checkNotTagged(coref,notref):

    cnt = 1
    skip = ['what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
            'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    
    for i in range(len(coref)):
        found = False
        if len(coref[i]) is 2:
            words = coref[i][1]
            #print "words is: " + words
            words = words.split()
            #print len(words)
            if len(words) > 1:
                for word in words:
                    #print "word is: " + word
                    if not (word in skip):
                        inText = notref.find(word)

                        if inText > 0:
                            found = True
                
                if found == True:
                    coref.append(['X' + str(cnt), word])
                    coref[i].append('X' + str(cnt))
                    cnt = cnt + 1
            else:
                #print "just one word and it is: " + words
                if not (words in skip):
                        inText = notref.find(words[0])

                        if inText > 0:
                            coref.append(['X' + str(cnt), words[0]])
                            coref[i].append('X' + str(cnt))
                            cnt = cnt + 1

    return coref

################################################################################
#
# Check Date Match
#
# Parameters: coref data structure (see create coref)
# Returns: Data structure with tagged references, their coref id and all ref id's
# Notes: Right now this will pair up any two corefs that are both formatted as a date
#        regardless of whether they are the same date or not.    
#
################################################################################


def checkDateMatch(coref):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "today", "tomorrow",
            "yesterday"]
    for i in range(len(coref)):
        for j in range(len(coref)):
            if i != j:
                w1date = False
                w2date = False
                word1 = coref[i][1]
                word2 = coref[j][1]
                
                word1date = re.search(r'(\d{1,2})[/.-](\d{1,2})([/.-](\d{2,4}))?', word1)
                if word1date is not None:
                    w1date = True
                
                word1date = re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|'
                                      r'may|june|july|august|september|october|november|december).(\d)', word1)
                if word1date is not None:
                    w1date = True
                
                word2date = re.search(r'(\d{1,2})[/.-](\d{1,2})([/.-](\d{2,4}))?', word2)
                if word2date is not None:
                    w2date = True
                
                word2date = re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|'
                                      r'may|june|july|august|september|october|november|december).(\d)', word2)
                if word2date is not None:
                    w2date = True
                
                if word1 in days:
                    w1date = True
                    
                if word2 in days:
                    w2date = True
                
                if w1date and w2date:
                    if len(coref[i]) is 2:
                        coref[i].append(coref[j][0])
                        break
    return coref

# Execution script
if __name__ == "__main__":
    main(sys.argv[1:])

