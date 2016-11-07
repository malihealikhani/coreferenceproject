################################################################################
#
# Sean Allen - U0021994
# Nick Sullivan -
#
# Natural Language Processing - CS 5340
# Term Project - Co-Reference Resolver
# coreference.py
#
################################################################################

import xml.etree.ElementTree as ET
import sys
import nltk
import os



################################################################################
#
# Main Function
#
# Parameters:
# Returns:
# Notes:
#
#
################################################################################


def main(files):

    listfile, responsedir = files

    # This grabs all the .crf files from the dev folder. We can iterate through these.
    # Just using one for testing though (a8.crf)

    for file in list(open(listfile)):
        file_path = os.path.splitext(file)[0]
        file_name = os.path.basename(file_path)
        response = responsedir + file_name + '.response'
        with open(response, 'w') as f:
            f.write(coreference(file.rstrip()))

    # coreference('./dev/b1.crf')


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
# Parameters:
# Returns:
# Notes: The slides on co-reference contain the following: Typical Co-reference
# Pipeline -Preprocessor: XML removal, tokenization, sentence and paragraph
# splitting -Part of Speech Tagging -Parsing -Named Entity Recognizer
# -Semantic Class Lookup (usualy via WordNet) -Candidate NP extraction
# -Supervised Learning -Clustering into Chains
#
##################################################################################

def coreference(f):

    # Create data structure
    tree = ET.parse(open(f))
    tree_root = tree.getroot()
    coref = create_coref(tree_root)
    notags = ET.tostring(tree_root, encoding='utf8', method='text')
    text = nltk.word_tokenize(notags)  # breaks up all the words into tokens and puts into a list
    sentences = nltk.sent_tokenize(notags)  # breaks corpus into sentences
    pos_tags = nltk.pos_tag(text)  # tags all the words in the corpus
    tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'WP', 'WP$']
    nouns = [noun for noun in pos_tags if noun[1] in tags]  # just the nouns, pronouns
    grammar = r'''
        NP: {(<NN><IN>)?<DT|PP$>?<JJ.*>*<NN.*>+<POS>?<NN.*>*}
            {<NN.+>+}
            {<PRP>}
            {<WP|WP$>}
    '''
    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(pos_tags)
    print chunked

    # check exact match in other corefs
    coref = checkExactMatch(coref)

    # check acronyms
    coref = checkAcronym(coref)

    cnt = 0
    for tag in coref:
        if len(tag) is 3:
            cnt += 1

    # check head noun match
    # check substring and partial match
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

    return format_output(coref)


def create_coref(root):
    coref = []  # I changed this to a list so we can keep the order
    for child in root:
        text = child.text

        # removes new lines in the middle of a string
        if text.__contains__("\n"):
            text = text[:text.index("\n")] + " " + text[text.index("\n")+1:]

        coref.append([str(child.get('ID')), text.lower()])
    return coref


def checkExactMatch(coref):
    cnt = 0
    for i in range(len(coref)):
        for j in range(i, -1, -1):
            if coref[i][1] == coref[j][1] and coref[i][0] != coref[j][0]:
                if len(coref[i]) is 2:
                    coref[i].append(coref[j][0])
                    cnt += 1
                    break
    return coref


def checkAcronym(coref):
    skip = ["and", "or", "in", "of", "&"]
    for i in range(len(coref)):
        if len(coref[i]) is 2:
            acr1 = ""
            acr2 = ""
            # This finds references from acronyms (FAA finds Federal Aviation Administration)
            if len(coref[i][1].split(" ")) is 1:
                for j in range(i, -1, -1):
                    if len(coref[j][1].split(" ")) is len(coref[i][1]):
                        for word in coref[j][1].split():
                            if word.lower() not in skip:
                                acr1 += word[0]
                            acr2 += word[0]
                        if acr1 is coref[i][1] or acr2 is coref[i][1]:
                            coref[i].append(coref[j][0])
            # This finds acronyms from references (Federal Aviation Administration finds FAA)
            else:
                for word in coref[i][1].split():
                    if word.lower() not in skip:
                        acr1 += word[0]
                    acr2 += word[0]
                for j in range(i, -1, -1):
                    if coref[j][1] is acr1 or coref[j][1] is acr2:
                        coref[i].append(coref[j][0])
    return coref


# Execution script
if __name__ == "__main__":
    main(sys.argv[1:])

