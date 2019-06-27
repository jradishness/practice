### TOKENIZING
# from nltk.tokenize import sent_tokenize, word_tokenize

# tokenizing - word tokenizers and sentence tokenizers
# corpora - body of text
# lexicon - dictionary of terms

#example_text = 'Hello Mr. Smith, how are you doing today? The weather is great and Python is awesome. The sky is blue. You should not eat cardboard.'

#print(sent_tokenize(example_text))
#print(word_tokenize(example_text))

#for i in sent_tokenize(example_text):
#    print(i)
#STOPWORDS
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
#stop_words = set (stopwords.words('english'))

#words = word_tokenize(example_text)
#filtered_sent = []
#for w in words:
#    if w not in stop_words:
#        filtered_sent.append(w)
# OR
#filtered_sent = [w for w in words if not w in stop_words]
#print(filtered_sent)

### STEMMING
#I was taking a ride in the car.
#I was riding in the car.
#from nltk.stem import PorterStemmer
#from nltk.tokenize import word_tokenize

#ps = PorterStemmer()

#example_words = ['python', 'pythoner', 'pythoning', 'pythoned', 'pythonly']
#for w in example_words:        # Returns a stem per line of the items within [example_words]
#    print(ps.stem(w))

#new_text = 'It is very important to be pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once.'
#words = word_tokenize(new_text)

#for f in words:             # Prints the tokens from the above sentence
#    print(ps.stem(f))


### POS TAGGING
# import nltk
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer as pst
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
#
# custom_sent_tokenizer = pst(train_text)
#
# tokenized = custom_sent_tokenizer.tokenize(sample_text)
#
# def process_content():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#
#             print(tagged)
#
#     except Exception as e:
#         print(str(e))
#
# process_content()

### CHUNKING

import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer as pst
train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_sent_tokenizer = pst(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)

            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP><NN>?}"""
            chunkparser = nltk.RegexpParser(chunkGram)
            chunked = chunkparser.parse(tagged)
            print(chunked)




    except Exception as e:
        print(str(e))

process_content()
