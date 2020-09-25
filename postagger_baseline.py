#!/usr/bin/env python
import time
t1 = time.time()
from optparse import OptionParser
import os, logging
import utils
import collections, re

def create_model(sentences):
    token_unidict = collections.defaultdict(lambda: collections.defaultdict(int))   # This is the dictionary of words, with the tags and counts in the Lambda.
    tag_max = collections.defaultdict(str)              # This is the dictionary of max prob tag for each word.

    for sentence in sentences:                          # Iterate through sentences in a doc
        for token in sentence:                          # Iterate through tokens in a sentence
            token_unidict[token.word][token.tag] += 1   # Increment the count of the tag|word.

    for word, nestdict in token_unidict.iteritems():    # Iterate through word level of tag|word dictionary
        highest = 0                                     # Reset highest value to zero
        for tag, count in nestdict.iteritems():         # Iterate through tags and counts in nested half of tag|word dict
            if count > highest:                         # Check if the current tag is better than saved tag
                highest = count                         # Re-assign count to highest if it is a better tag
                tag_max[word] = tag                     # Re-assign tag to word in dict of best tags

    return tag_max

def predict_tags(sentences, model):
    for sentence in sentences:                          # Iterate through sentences in a doc
        for token in sentence:                          # Iterate through tokens in a sentence
            if token.word in model:                     # Check that best tag exists in dict
                token.tag = model[token.word]           # Re-assign tag to 'best guess'
            elif str(token.word[0]).isupper():          # If not in dict, check for capital letter
                token.tag = 'NNP'                       # Re-assign NNP tag to words starting with capital letters
            elif "-" in token.word:
                token.tag = 'JJ'
            elif token.word.endswith('ed'):
                token.tag = 'VBD'
            elif token.word.endswith('ing') and len(token.word) > 4:
                token.tag = 'VBG'
            elif token.word.endswith('er'):
                token.tag = 'JJR'
            elif token.word.endswith('s'):
                token.tag = 'NNS'
            elif re.search(r"\d", token.word):
                token.tag = 'CD'
            else:                                       # And if all else fails...
                token.tag = 'NN'                        # Assign most common tag

    return sentences

if __name__ == "__main__":
    usage = "usage: %prog [options] GOLD TEST"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    training_file = args[0]
    training_sents = utils.read_tokens(training_file)
    test_file = args[1]
    test_sents = utils.read_tokens(test_file)
    # print test_sents[2]           # My debugging
    model = create_model(training_sents)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(test_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(test_sents, predictions)
    print "Accuracy in testing [%s sentences]: %s" % (len(sents), accuracy)

    t3 = time.time()
    print 'Time to run: ', t3 - t1
