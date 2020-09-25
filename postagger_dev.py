#!/usr/bin/env python
import time
t1 = time.time()
from optparse import OptionParser
import os, logging
import utils
import collections, math, re

def create_model(sentences):
    token_unidict = collections.defaultdict(lambda: collections.defaultdict(int))   # This is the dictionary of words, with the tags and counts in the Lambda.
    tag_unidict = collections.defaultdict(int)  # This is the dictionary of counts of tags
    tag_bidict = collections.defaultdict(lambda: collections.defaultdict(int))  # This is the dictionary of tag bigrams and counts.
    trans_probs = collections.defaultdict(lambda: collections.defaultdict(float))   # This is the dictionary of transition probabilities. P(tag|prev_tag)
    emiss_probs = collections.defaultdict(lambda: collections.defaultdict(float))   # This is the dictionary of likelihood probabilities. P(word|tag)
    vocab = collections.defaultdict(int)                # keeping a vocab count in order to calculate unseen words later

    for sentence in sentences:
        prev_tag = "<S>"        # To start bigram counting in sentences with a <S>
        for token in sentence:
            vocab[token.word] += 1
            token_unidict[token.tag][token.word] += 1   # Increment the count of the word|tag. token_unidict[tag][word]
            tag_unidict[token.tag] += 1     # Increment the count of the tag                   tag_unidict[tag]
            tag_bidict[prev_tag][token.tag] += 1    # Increment the count of the tag|prev_tag  tag_bidict[prev_tag][tag]
            prev_tag = token.tag        # Reset the value of prev_tag to save for bigrams
        tag_unidict["<S>"] += 1         # To keep accurate counts of <S> tags

    for tag1, nestdict in tag_bidict.iteritems():      # Code from the Language Detector to get bigram probabilities
        for tag2, count in nestdict.iteritems():
            trans_probs[tag1][tag2] = math.log(float(count + 1) / float(tag_unidict[tag1] + float(len(tag_unidict.keys()))))

    for tag, nestdict in token_unidict.iteritems():   # Same as above, for emission probabilities
        for word, count in nestdict.iteritems():
            if count != 0 and count == tag_unidict[tag]:    # Code to deal with tags that only occur with one word and thus = 1/1 = 1 and math.log(1) = zero
                emiss_probs[tag][word] = -0.0000001
            else:
                emiss_probs[tag][word] = math.log(float(count) / float(tag_unidict[tag]))
    print "Training Complete: ", round(time.time() - t1, 2)
    return emiss_probs, trans_probs, vocab

def predict_tags(sentences, model):
    count = 0
    best_tag = ""
    emiss_probs, trans_probs, vocab = model
    tag_iter = [x for x in trans_probs.keys() if x != "<S>"]  # create a list of tags as a utility

    for sentence in sentences:  # Iterate through sentences in a doc
        viterbi = collections.defaultdict(lambda: collections.defaultdict(float))
        best_path = collections.defaultdict(lambda: collections.defaultdict(str))

        ### FILL VITERBI FOR COLUMN 1
        for tag in tag_iter:  # Iterate through tags in columns of outside dict for only the first word.
            if not vocab.has_key(sentence[0].word):            # if unseen
                # if ("-" in word):
                if sentence[0].word.endswith('ed'):
                    if tag == 'VBD':     # past particple or past tense
                        viterbi[tag][0] = trans_probs["<S>"][tag] + -0.00001
                    else:
                        pass
                elif sentence[0].word.endswith('ing'):  # present participle
                    if tag == 'VBG':
                        viterbi[tag][0] = trans_probs["<S>"][tag] + -0.00001
                    else:
                        pass
                elif sentence[0].word.endswith('er'):  # comparative
                    if tag == 'JJR':
                        viterbi[tag][0] = trans_probs["<S>"][tag] + -0.00001
                    else:
                        pass
                elif sentence[0].word.endswith('s'):  # plural
                    if tag == 'NNS':
                        viterbi[tag][0] = trans_probs["<S>"][tag] + -0.00001
                    else:
                        pass
                elif re.search(r"\d", sentence[0].word):
                    if tag == 'CD':  # past particple or past tense
                        viterbi[tag][0] = trans_probs["<S>"][tag] + -0.00001
                    else:
                        pass
                else:
                    if tag == 'NN':                         # When we come across the NN tag, we want to give it a good prob
                        viterbi[tag][0] = trans_probs["<S>"][tag] + -0.00001
                    else:           # every tag not 'NN' gets a 0.0 in viterbi
                        pass
            else:
                if emiss_probs[tag][sentence[0].word] == 0.0:
                    pass
                else:
                    viterbi[tag][0] = emiss_probs[tag][sentence[0].word] + trans_probs["<S>"][tag]

        ### FILL VITERBI AND BEST_PATH FOR COLUMNS AFTER 1
        for index in range(1, len(sentence)):                       # this is iterating through the rest of the words in the sentence
            if not vocab.has_key(sentence[index].word):                # if unseen
                if sentence[index].word.isupper():
                    emiss_probs['NNP'][sentence[index].word] = -0.00001         #  Proper nouns
                    vocab[sentence[index].word] += 1
                elif "-" in sentence[index].word:
                    emiss_probs['JJ'][sentence[index].word] = -0.0001      # adjectives
                    vocab[sentence[index].word] += 1
                elif sentence[0].word.endswith('ed'):               # past participles and past tense
                    emiss_probs['VBD'][sentence[index].word] = -0.0001
                    emiss_probs['VBN'][sentence[index].word] = -0.0001
                    vocab[sentence[index].word] += 1
                elif sentence[0].word.endswith('ing') and len(sentence[index].word) > 5:    # gerunds
                    emiss_probs['VBG'][sentence[index].word] = -0.00001
                    vocab[sentence[index].word] += 1
                elif sentence[0].word.endswith('er'):  # comparative
                    emiss_probs['JJR'][sentence[index].word] = -0.00001
                    vocab[sentence[index].word] += 1
                elif sentence[0].word.endswith('s'):  # plural
                    emiss_probs['NNS'][sentence[index].word] = -0.00001
                    vocab[sentence[index].word] += 1
                elif re.search(r"\d", sentence[index].word):        #numbers
                    emiss_probs['CD'][sentence[index].word] = -0.00001
                else:
                    emiss_probs['NN'][sentence[index].word] = -0.00001
                    vocab[sentence[index].word] += 1

            for curr_tag in tag_iter:       # iterate through the list of tags (in this column) to find each tag's best prev_tag and best_prob
                best_prob = -20000.00     # reset best-tag value to something ridiculously low
                for prev_tag in tag_iter:       # iterate through each tag possibility in the previous column, in order to find the best calc
                    if viterbi[prev_tag][index-1] == 0.0 or emiss_probs[curr_tag][sentence[index].word] == 0.0:     # dealing with uneven data because of logs
                        pass
                    else:
                        aux = viterbi[prev_tag][index-1] + emiss_probs[curr_tag][sentence[index].word] + trans_probs[prev_tag][curr_tag]   # calculate the value for this particular cell
                        if aux > best_prob:         # is this the best we've seen so far?
                            best_prob, best_tag, viterbi[curr_tag][index] = aux, prev_tag, aux             # if so, reset the aux to the new best
                    best_path[curr_tag][index] = best_tag           # this much seems to work
        final_tag, best_prob = "", -20000.0

        ### GET BEST TAG FOR FINAL WORD IN SENTENCE
        for key in tag_iter:           # iterate through the upper(tag) level of viterbi{}
            aux = viterbi[key][int(len(sentence)-1)] # grab the saved viterbi{} value for the last word in the sentence

            if aux == 0.0:                     # Zeroes in the data throw off the negative log probabilities
                pass
            elif aux > best_prob:               # if the current iteration is better than the saved max,
                best_prob, final_tag = aux, key                 # store it as the new max, and

        sentence[len(sentence) - 1].tag = final_tag         # re-assign final tag in sentence

        ### FINISH FILLING OUT LIST OF BEST TAGS
        for index in range(len(sentence) - 2, -1, -1):
            sentence[index].tag = best_path[final_tag][index+1]     # reassign each of the rest of the tags
            final_tag = sentence[index].tag

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
    model = create_model(training_sents)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy), 'TTR:', round(time.time() - t1, 2)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(test_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(test_sents, predictions)
    print "Accuracy in testing [%s sentences]: %s" % (len(sents), accuracy), "TTR:", round(time.time() - t1, 2)