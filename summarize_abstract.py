def summarize_title(text):
    from eazymind.nlp.eazysum import Summarizer
    key = "b47b7ffea86caab6112d2cf190b0b5d6"
    sentence = str(text.encode('utf-8'))
    summarizer = Summarizer(key)
    i="i"
    while(i=="i" or i[0]=="<" or i[0]=="!"):
        i=summarizer.run(sentence)
    return i