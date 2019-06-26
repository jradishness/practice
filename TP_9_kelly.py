# Exercise 9.1
with open("words.txt") as fin:
    for word in fin:
        if len(word) > 20:
            print(word)

# Exercise 9.1
def has_no_e(word):
    """"Function to determine if a word has no 'e'."""
    for letter in word:
        if letter == 'e':
            return False
    return True

# Exercise 9.2
with open("words.txt") as fin:
    for word in fin:
        if len(word) > 20:
            if not word.__contains__("e"):
                print(word)

# Exercise 9.2
e_counter, non_counter = 0, 0
with open("words.txt") as wordlist:
    for word in wordlist:
        if word.__contains__("e"):
            e_counter += 1
        else:
            non_counter += 1
total_words = e_counter + non_counter
print("Word's with E: " + str(e_counter))
print("Word's without E: " + str(non_counter))
print("Total: " + str(total_words))
print("Percentage: {:.2%}".format(e_counter / total_words))

# Exercise 9.3
def avoid(word, string):
    """Function for inputting a word and a string and determining
    if any of the characters in the string appear in the word."""
    for x in string:
        if x in word:
            return False
    return True

# Exercise 9.3
def corpus_avoid():
    """Function to search the wordlist for the count of
    words that don't contain a desired string"""
    wordcount, wordlist, string = 0, [], input("What letters are you avoiding?")
    with open("words.txt") as fname:
        for word in fname:
            wordcount += 1
            for x in string:
                if word.__contains__(x):
                    wordlist.append(word)
    print("\nThere are " + str(wordcount - (
        len(set(wordlist)))) + " words which do not \ncontain any of the letters in your \nchosen string: " + str(
        string))

# Exercise 9.6
def is_abecedarian(word):
    """Function to determine if a word is abecedarian."""
    for x in range(len(word) - 1):
        if word.lower()[x] > word.lower()[x + 1]:
            return False
        else:
            continue
    return True

# Exercise 9.7
with open("words.txt") as wordlist:
    for word in wordlist:
        for x in range(len(word) - 5):
            if word[x] == word[x + 1] and word[x + 2] == word[x + 3] and word[x + 4] == word[x + 5]:
                print(word)
            else:
                continue

# Exercise 9.8
for x in range(100000,1000000):
    if str(x)[5] == str(x)[2] and str(x)[4] == str(x)[3]:
        if str(x+1)[5] == str(x+1)[1] and str(x+1)[4] == str(x+1)[2]:
            if str(x+2)[1] == str(x+2)[4] and str(x+2)[3] == str(x+2)[2]:
                if str(x+3)[0] == str(x+3)[5] and str(x+3)[1] == str(x+3)[4]and str(x+3)[2] == str(x+3)[3]:
                    print(str(x))
