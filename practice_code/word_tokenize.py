import nltk
from nltk.tokenize import word_tokenize
quote = input('What have you for me?')
tokens = word_tokenize(quote)
print(tokens)
print('There are ', len(tokens), 'in your string.')