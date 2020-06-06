def summarize(text):
    # importing libraries
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize

    nltk.download('punkt')
    nltk.download('stopwords')
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq



    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    average = int(sumValues / len(sentenceValue))
    i=0
    summary=[]
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (0.1 * average) and i<10):
            i+=1
            summary.append(sentence)
    return summary

print(summarize('''A planned memorial was underway for George Floyd in Raeford, N.C., on Saturday morning, as demonstrations in his memory and against police brutality began in cities nationwide. Hundreds of thousands of people were expected to take to the streets nationwide, including Washington, D.C., and other major cities, as well as in countless smaller cities and towns in between. Peter Newsham, the chief of police in Washington, expected the demonstration to be “one of the largest” the city has seen.'''))
