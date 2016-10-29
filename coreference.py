########################################################
#
# Sean Allen - U0021994
# Nick Sullivan -
#
# Natural Language Processing - CS 5340
# Term Project - Co-Reference Resolver
# coreference.py
#
########################################################



import sys


################################################################################
#
# Main Function
#
# Parameters:
# Returns:
# Notes:
#
################################################################################


def main(files):

    g, s = files

    with open('parser.trace', 'w') as f:
        f.write( coreference() )


##################################################################################
#
# Co-Reference Method
#
# Parameters:
# Returns:
# Notes:
#
##################################################################################

def coreference():
    return "This needs to be updated\n"


# Execution script
if __name__ == "__main__":
    main(sys.argv[1:])

