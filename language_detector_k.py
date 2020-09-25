#!/usr/bin/env python
import time
t1 = time.time()
from optparse import OptionParser
import os, logging, re
import collections
import math
import string


def preprocess(line):
    line = line.rstrip()
    line = line.lower()
    line = re.sub("[^a-z ]", '', line)

    tokens = line.split()
    tokens = ['$$'+token+'$$' for token in tokens]          # uni/bigram processing
    return tokens

# python language_detector_public/language_detector_final_kelly.py language_detector_public/data/train/en/all_en.txt language_detector_public/data/train/es/all_es.txt language_detector_public/data/test/

def create_model(path):
    unigrams = collections.defaultdict(int)
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))
    trigrams = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    bicalc = collections.defaultdict(lambda: collections.defaultdict(float))
    tricalc = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(float)))

    alpha = string.ascii_lowercase
    for char in alpha:
        for bigr in alpha:
            bigrams[char][bigr] = 0
            for trig in alpha:
                trigrams[char][bigr][trig] = 0

    f = open(path, 'r')
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
            for index in range(0, len(token)-2):
                unigrams[token[index]] += 1                 # increment unigrams
                bigrams[token[index]][token[index + 1]] += 1
                trigrams[token[index]][token[index + 1]][token[index + 2]] += 1  # increment trigrams

    for char1, value in bigrams.iteritems():
        for char2, count in value.iteritems():
            bicalc[char1][char2] = math.log(float((bigrams[char1][char2]) + 1) / float(unigrams[char1] + 27))

    for char1, value in trigrams.iteritems():
        for char2, value2 in value.iteritems():
            for char3, count in value2.iteritems():
                tricalc[char1][char2][char3] = math.log(float((trigrams[char1][char2][char3]) + 1) / float(bigrams[char1][char2] + 729))
    # print bicalc['a']['b']                # debugging
    # print tricalc['a']['b']['a']
    return bicalc, tricalc

def predict(file, model_en, model_es):
    en_bicalc, en_tricalc = model_en
    es_bicalc, es_tricalc = model_es
    en_prob = 0.0
    es_prob = 0.0
    f = open(file, 'r')
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
            for index in range(0, len(token) - 2):
                en_prob += en_tricalc[token[index]][token[index + 1]][token[index + 2]]
                es_prob += es_tricalc[token[index]][token[index + 1]][token[index + 2]]
                # en_prob += en_bicalc[token[index]][token[index + 1]]                  # Comment out line for Trigram-only model
                # es_prob += es_bicalc[token[index]][token[index + 1]]                  # Comment out line for Trigram-only model

    if en_prob > es_prob:
        return "English", en_prob, es_prob
    else:
        return "Spanish", en_prob, es_prob

def main(en_tr, es_tr, folder_te):
    model_en = create_model(en_tr)
    model_es = create_model(es_tr)

    folder = os.path.join(folder_te, "en")
    print "Prediction for English documents in test:"
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        prediction, en_prob, es_prob = predict(f_path, model_en, model_es)
        print "%s\t%s" % (f, prediction)
        print "English score: ", en_prob
        print "Spanish score: ", es_prob
        print "Marg. of Prob: ", en_prob - es_prob
    
    folder = os.path.join(folder_te, "es")
    print "\nPrediction for Spanish documents in test:"
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        prediction, en_prob, es_prob = predict(f_path, model_en, model_es)
        print "%s\t%s" % (f, prediction)
        print "Spanish score: ", es_prob
        print "English score: ", en_prob
        print "Marg. of Prob: ", es_prob - en_prob

    t3 = time.time()
    print 'Time to run: ', t3-t1

if __name__ == "__main__":
    ## DO NOT CHANGE THIS CODE

    usage = "usage: %prog [options] EN_TR ES_TR FOLDER_TE"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    main(args[0], args[1], args[2])

