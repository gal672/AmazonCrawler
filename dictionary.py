import sys
from operator import itemgetter

dictionaryList = []
StopWordList = ["of","in","for","to","and","the","a","you","or","from","is","are","be","on","if","i","my","amazon","this","your","with","it","0","1","2","3","4","5","6","7","8","9"]
counts = dict()

def init():
    dictionaryList.append("USB Powered")
    dictionaryList.append("Wall Mount Bracket")
    dictionaryList.append("LED Strip")
    dictionaryList.append("Stand")
    dictionaryList.append("Cable Charger")
    dictionaryList.append("Wall Mount")
    dictionaryList.append("Remote")
    dictionaryList.append("AC Power Supply")
    dictionaryList.append("Cable")
    dictionaryList.append("Power Cord")

def check_link(link_text):
    for word in dictionaryList:
        if (word in link_text):
            return False
    return True

def filterStopWord(occs):
    words = []
    for word in occs:
        if (word[0]  not in StopWordList):
                words.append(word)
    return words


def appendWord(occs):
    for i in occs:
        counts[i[0]] = counts.get(i[0], 0) + i[1]
    list = sorted(counts.items(), key=itemgetter(1))
    print(counts)
    print(list)


