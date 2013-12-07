#-------------------------------------------------------------------------------
# Name:        n-grams
# Purpose:    NLP HW2
#
# Author:      PRASANNA
#
# Created:     27/09/2012
# Copyright:   (c) PRASANNA 2012
# Licence:     GPL 
#-------------------------------------------------------------------------------

import re
import nltk
import locale
import sys
locale.setlocale(locale.LC_NUMERIC, "")

class Bigram:
    def __init__(self):
     self.unigramCount={}
     self.bigramCount={}
     self.frequencyCount = {}
     self.unigramProbability = {}
     self.bigramProbability = {}
     self.bigramProbabilityLS = {}
     self.bigramProbabilityGTD = {}

    def TrainUnigramCount(self,words):
        for word in words:
            if self.unigramCount.has_key(word):
                self.unigramCount[word]+=1
            else:
                self.unigramCount[word]=1

    def TrainBigramCount(self, words):
        iterWords = iter(words)
        next(iterWords)
        for word in iterWords:
         i= words.index(word)
         if self.bigramCount.has_key((word,words[i-1])):
          self.bigramCount[(word,words[i-1])]+=1
         else:
          self.bigramCount[(word,words[i-1])]=1
        ##if self.bigramCount.has_key[('<s>','</s>')]:
        self.bigramCount.pop(('<s>','</s>'))

    def TrainFrequencyCount(self,words):
       iterWords = iter(words)
       next(iterWords)
       for word in iterWords:
         i = words.index(word)
         if(self.bigramCount.has_key((word,words[i-1]))):
          if self.frequencyCount.has_key((self.bigramCount[(word,words[i-1])])):
           self.frequencyCount[self.bigramCount[(word,words[i-1])]]+=1
          else:
           self.frequencyCount[self.bigramCount[(word,words[i-1])]]=1

    def CalculateUnigramProbability(self,words):
        for word in words:
         if self.unigramCount.has_key(word):
            self.unigramProbability[word] = float(self.unigramCount[word])/float(len(words))


    def CalculateBigramProbability(self,words):
       bp=1
       iterWords = iter(words)
       next(iterWords)
       for word in iterWords:
        i = words.index(word)
        if self.bigramCount.has_key((word,words[i-1])):
         self.bigramProbability[(word,words[i-1])]= float(self.bigramCount[(word,words[i-1])])/(float(self.unigramCount[words[i-1]]))
        else:
         self.bigramProbability[(word,words[i-1])]=0
        bp = float( bp*self.bigramProbability[(word,words[i-1])])
       return bp

    def CalculateBigramProbabilityLaplaceSmoothing(self,words,V):
        bpLS=1
        iterWords = iter(words)
        next(iterWords)
        for word in iterWords:
         i=words.index(word)
         if self.bigramCount.has_key((word,words[i-1])):
          k = 1.0/(self.unigramCount[words[i-1]]+float(V))
          #self.bigramProbabilityLS[(word,words[i-1])]= float(self.bigramCount[(word,words[i-1])]+1)/(float(self.unigramCount[words[i-1]]+V))
          self.bigramProbabilityLS[(word,words[i-1])]=k
         else:
            self.bigramProbabilityLS[(word,words[i-1])] =float(1.0/float(V))
         bpLS = float(self.bigramProbabilityLS[(word,words[i-1])]*bpLS)
        return bpLS

    def CalculateBigramProbabilityGoodTuringDiscounting(self,words,rawLength):
        bpGTD=1
        iterWords = iter(words)
        next(iterWords)
        for word in iterWords:
         i=words.index(word)
         if self.bigramCount.has_key((word,words[i-1])) and self.frequencyCount.has_key((self.bigramCount[(word,words[i-1])]+1)):
          self.bigramProbabilityGTD[self.bigramCount[(word,words[i-1])]]= float(float((float(self.frequencyCount[(self.bigramCount[(word,words[i-1])])+1]))* (float(self.bigramCount[(word,words[i-1])]+1)))/float(float(self.frequencyCount[(self.bigramCount[(word,words[i-1])])])))/float(rawLength)
          bpGTD = self.bigramProbabilityGTD[self.bigramCount[(word,words[i-1])]]*bpGTD
        else:
          self.bigramProbabilityGTD[0]=self.frequencyCount[1]/float(rawLength)
          bpGTD = self.bigramProbabilityGTD[0]*bpGTD
        return bpGTD


    def GetDistinctWords(self,words):
        distinctWords=[]
        for word in words:
            if word not in distinctWords:
                distinctWords.append(word)
        return distinctWords

    def format_num(self,num):
     try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)
     except (ValueError, TypeError):
        return str(num)

    def get_max_width(self,table, index):
     return max([len(self.format_num(row[index])) for row in table])

    def pprint_table(self,out,table):
     col_paddings = []
     for i in range(len(table[0])):
        col_paddings.append(self.get_max_width(table, i))
     for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = self.format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out


def main():
    b = Bigram()
    preWords = []
    rawWords = []
    words = []
    p=open(r'C:\Prasanna\NLPCorpusTreebank2Parts.txt','r')
    text=p.read()
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(text)
    for sent in sents:
        preWords= re.split('\W+',sent)                                                 ## spliting text into a list of words
        preWords.insert(0,'<s>')
        preWords.append('</s>')
        preWords= filter(lambda a:a!='',preWords)
        for preWord in preWords:
            rawWords.append(preWord)
        del preWords[:]
    rawLength = len(rawWords)
    b.TrainUnigramCount(rawWords)
    b.TrainBigramCount(rawWords)
    V = len(b.GetDistinctWords(rawWords))
    words= filter(lambda a:a!='<s>',rawWords)
    words= filter(lambda a:a!='</s>',words)
    b.TrainFrequencyCount(words)
    del words[:]
    del preWords[:]
    p=open(r'C:\Prasanna\HW2Test.txt','r')
    text=p.read()
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(text)

    words2=[]
    for sent in sents:
        preWords= re.split('\W+',sent)                                           ## spliting text into a list of words
        preWords.insert(0,'<s>')
        preWords.append('</s>')
        preWords= filter(lambda a:a!='',preWords)
        preWords2 = []
        for word in preWords:
            words2.append(word)
        preWords2=preWords
        words.append(preWords2)
        preWords=[]
    l=1
    for word in words:
     print 'Sentence '+str(l)
     b.CalculateUnigramProbability(word)
    ## bp = b.CalculateBigramProbability(word)
     bpLS = b.CalculateBigramProbabilityLaplaceSmoothing(word,V)
    ## bpGTD = b.CalculateBigramProbabilityGoodTuringDiscounting(word,rawLength)
   ##  print 'Bigram Probability: '+ str(bp)
     print 'Bigram Probability with Laplace Smoothing: '+str(bpLS)
   ## print 'Bigram Probability with Good Turing Discounting: '+str(bpGTD)
     l+=1

## For printing bigram counts
    print '\n Printing Bigram counts for the two sentences.'
    table =[]
    title =[]
    subtitle=[]
    subtitleCopy =[]
    title.append(',')
    for word in words2:
     title.append(word)
    table.append(title)
    for otherWord in words2:
     subtitle.append(otherWord)
     for word in words2:
      if(b.bigramCount.has_key((word,otherWord))):
        subtitle.append( str( b.bigramCount[word,otherWord]))
      else:
        subtitle.append('0')
     subtitleCopy=subtitle
     table.append(subtitleCopy)
     subtitle=[]
    out = sys.stdout
    b.pprint_table(out, table)

    ## For printing bigram probabilities
    print '\n Printing Bigram Probabilities for the two sentences.'
    table =[]
    title =[]
    subtitle=[]
    subtitleCopy =[]
    title.append(',')
    for word in words2:
     title.append(word)
    table.append(title)
    for otherWord in words2:
     subtitle.append(otherWord)
     for word in words2:
      if(b.bigramProbability.has_key((word,otherWord))):
        subtitle.append( str( b.bigramProbability[word,otherWord]))
      else:
        subtitle.append('0')
     subtitleCopy=subtitle
     table.append(subtitleCopy)
     subtitle=[]
    out = sys.stdout
    b.pprint_table(out, table)

    ## For printing bigram probabilities with Laplace Smoothing
    print '\n Printing Bigram Probabilities with Laplace smoothing for the two sentences.'
    table =[]
    title =[]
    subtitle=[]
    subtitleCopy =[]
    title.append(',')
    for word in words2:
     title.append(word)
    table.append(title)
    for otherWord in words2:
     subtitle.append(otherWord)
     for word in words2:
      if(b.bigramProbabilityLS.has_key((word,otherWord))):
        subtitle.append( str( b.bigramProbabilityLS[word,otherWord]))
      else:
        subtitle.append('0')
     subtitleCopy=subtitle
     table.append(subtitleCopy)
     subtitle=[]
    out = sys.stdout
    b.pprint_table(out, table)

if __name__ == '__main__':
    main()
