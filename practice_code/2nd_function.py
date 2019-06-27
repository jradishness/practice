def game():
    text = input('Shall we play a game?\n')    # because I've always wanted to
    if text[0] == 'y' or text[0] == 'Y':
        text2 = input('How about a nice game of chess?\n')
        if text2 != '':
            print("I'm sorry, but I can't play chess, actually.")
            text = input("What would you like to write instead?\n")
            name = text[0:6]                # this creates a var to be used for a filename from the text's beginning
            name = name.replace(" ", "_")   # this replaces any spaces in the filename with underscore
            name2 = name.lower() + '_new_file.txt'  # finish the name combination
            f = open(name2, 'w')    # create the new file with the var name
            print(text, file = f)   # write the text to file
        #else:
            #pass   #just in case I ever want to add anything
    else:
        print("Thank you. Please come again. -Apu Nahasapeemapetilon")

game()