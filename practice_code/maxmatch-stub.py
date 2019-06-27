
import nltk
#   from nltk.corpus import words # (unneccesary)
wordlist = nltk.corpus.words.words()

## Input 2: test strings - read in from file

teststrings = open('test-strings-maxmatch.txt').readlines()
# print("Test strings read in from file:",teststrings)

teststrings = [s.strip() for s in teststrings]
# print("New version of test strings",teststrings)

### B. for a given string, perform segmentation



def maxmatch(sent):
    orig = sent
    result = []
    remainder = "12"
    pointer = len(sent)
    firstword = sent[:pointer]
    while len(remainder) >= 1:
        if firstword in wordlist:
            result.append(firstword)
            interval = len(firstword)
            remainder = sent[interval:]
            # print('remainder is:',remainder,'--Newly-stored word is:', firstword, '-if loop')
            firstword = remainder
            sent = remainder
            pointer = len(sent)

        else:
            if len(remainder) == 1:
                firstword = firstword[1:]
                result.append(remainder)
                # print('appending a small item')

            else:
                pointer -= 1
                firstword = sent[:pointer]
                # print(pointer, remainder, result, "-else loop")
    # print("Line:", orig)
    print("Result:", result)


            # return list[firstword, maxmatch(remainder)]
#         else:
#             i -= 1
#             firstword = sent[:i+1]
#             remainder = sent[i:]
#             return list[firstword, maxmatch(remainder)]
#
# maxmatch(teststrings)
for line in teststrings:
    maxmatch(line)
# maxmatch(teststrings[2])
