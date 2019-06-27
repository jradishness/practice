def sing_a_song():
    text = input('So, give me a word yo:\n')
    lyric = text[-3:-1]
    print(text * 2, "fo-fi", lyric * 3, text, "!")

sing_a_song()