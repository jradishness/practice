import nltk
import string
from string import punctuation
from nltk import bigrams
from nltk.corpus import PlaintextCorpusReader as pcr
from nltk import word_tokenize

corpus_root = r'texts'   # assign the directory from which to find texts
# textin = (input("Which text?"))
# sample = pcr(corpus_root, ['mandarin.txt', 'sports.txt'])  # read the files into memory
study11 = pcr(corpus_root, ['mandarin.txt'])
study22 = pcr(corpus_root, ['sports.txt'])
# study1 = word_tokenize(study11)
# study2 = word_tokenize(study22)
# print(type(study2))
# print(study2[0:10])
reset1 = study11.words("bilinguals.txt")
reset2 = study22.words('sports.txt')
study1 = nltk.Text(study11.words("bilinguals.txt")) # create an NLTK text file from this text file
study2 = nltk.Text(study22.words('sports.txt'))
# print(type(study2))

resetlist = [] # this is my list of words
for x in reset1:
    resetlist.append(x)   # move all of the words from the NLTK text item into a list
# print(resetlist[0:8])
# print(type(resetlist))
str1 = ''
count1 = len(resetlist) # grab the token count before we convert to tuples
for x in resetlist:
    str1 += x + " "    # convert the list back to a string with spaces

# final1 = [x for x in str1 if x not in punctuation]        # Hopefully, this will finally strip punctuation.
# str1.rstrip(punctuation)     # strip away punctuation. I don't think it works
# print(str1)

resetlist = []      # do it all again for the next article
for x in reset2:
    # resetlist.rstrip(punctuation)         This doesnt work
    resetlist.append(x)
# print(resetlist[0:8])
# print(type(resetlist))
str2 = ''
count2 = len(resetlist)         # grab the token count before we convert to tuples
for x in resetlist:
    str2 += x + " "     # convert the list back to a string with spaces

# str2.rstrip(punctuation)     # strip away punctuation. I don't think it works
# print(str2)

# final2 = [x for x in str2 if x not in punctuation]   # to remove punctuation
def bigram_grab(papername):
    from nltk.tokenize import word_tokenize
    # text2 = []              # create empty list
    papername = word_tokenize(papername)        # word tokenize the string from above
    # for x in papername:     # iterate through chosen text
    #     x.split()
    #     text2.append(x)
    # print(type(papername))
    # print(text2[0:10])
    papername = [x for x in papername if x not in punctuation]   # this one finally worked
    bigramslist = list(bigrams(papername))
    # strippedlist = [x for x in bigramslist if x not in punctuation]     # cant do this to tuples
    # print(bigramslist[0:10])
    bidict = {}  # create a new dictionary to count frequencies
    for x in bigramslist:
        if x not in bidict:  # first time we've seen the bigram
            bidict[x] = 1  # set counter to 1
        else:  # we've seen the bigram before
            bidict[x] += 1  # Add one to counter

    word_freq = []      # we can sort a list!!!
    for key, value in bidict.items():   # so, for each key and value in our dict...
        word_freq.append((value, key))  # we're going to add them to our list, but backwards
    word_freq = (sorted(word_freq))   # now when we sort, we're sorting by freq count, not text
    word_freq.sort(reverse=True)    # this gets the sort to start at the top
    print("Top 15 bigrams from the text:", word_freq[0:15])


bigram_grab(str1)       # run the aforementioned strings through the bigram machine
bigram_grab(str2)

print("Text 1 is ", count1, " tokens long", "Text 2 is ", count2, " tokens long")

# freq1 = input("So, which bigram do you want to use? Just give me it's frequecy in the first text: ")
# freq2 = input("And... in the second text? ")
#
# freq1 = int(freq1)
# freq2 = int(freq2)
#
# N1 = count1 - freq1
# N2 = count2 - freq2
# Totalcd = N1 + N2
#
# E1 = N1 * (freq1 + freq2) / (N1 + N2)
# E2 = N2 * (freq1 + freq2) / (N1 + N2)
#
# # G2 = 2 * (( freq1 * ln ( freq1 / E1 )) + ( freq2 * ln ( freq2 / E2 ))) # Cannot use until I uncover the value of ln
#
# print("Log likelihood is ", G2,)
# print("The higher the G2 value, the more significant is the difference between two frequency scores. For these tables, a G2 of 3.8 or higher is significant at the level of p < 0.05 and a G2 of 6.6 or higher is significant at p < 0.01.")