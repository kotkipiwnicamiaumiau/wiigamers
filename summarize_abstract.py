def summarize_title(text):
    from eazymind.nlp.eazysum import Summarizer
    key = "b47b7ffea86caab6112d2cf190b0b5d6"
    sentence = str(text.encode('utf-8'))
    summarizer = Summarizer(key)
    i="i"
    while(i=="i" or i[0]=="<" or i[0]=="!"):
        i=summarizer.run(sentence)
    return i
print(summarize_title('''A planned memorial was underway for George Floyd in Raeford, N.C., on Saturday morning, as demonstrations in his memory and against police brutality began in cities nationwide. Hundreds of thousands of people were expected to take to the streets nationwide, including Washington, D.C., and other major cities, as well as in countless smaller cities and towns in between. Peter Newsham, the chief of police in Washington, expected the demonstration to be “one of the largest” the city has seen.'''))
