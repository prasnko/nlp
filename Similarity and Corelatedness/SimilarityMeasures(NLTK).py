#-------------------------------------------------------------------------------
# Name:        Word Similarity and Relatedness
# Purpose:
#
# Author:      PRASANNA
#
# Created:     28/11/2012
# Copyright:   (c) PRASANNA 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import xlwt


def findMax(mensX,mensY,simType):
 maxSim = 0
 brown_ic = wordnet_ic.ic('ic-brown.dat')
 semcor_ic = wordnet_ic.ic('ic-semcor.dat')
 for wnx in wn.synsets(mensX,wn.NOUN)[0:10]:
  for wny in wn.synsets(mensY,wn.NOUN)[0:10]:
   if simType == 'path':
    sim = wnx.path_similarity(wny)
   elif simType=='lch':
    sim = wnx.lch_similarity(wny)
   elif simType=='wup':
    sim = wnx.wup_similarity(wny)
   elif simType =='res':
    sim = wnx.res_similarity(wny,brown_ic)
   elif simType =='jcn':
    sim = wnx.jcn_similarity(wny,brown_ic)
   elif simType == 'lin':
    sim = wnx.lin_similarity(wny,brown_ic)
    if sim>maxSim:
     maxSim = sim
 return maxSim

def main():
 p = open(r'C:\Prasanna\Fall12\NLP\HW5\ws353simrel\wordsim353_sim_rel\wordsim_similarity_goldstandard.txt','r')
 text = p.read()
 lines = []
 sentence = []
 sentences = []
 sentence0= []
 sentence1= []
 sentence2=[]
 pathSiml = []
 wupSiml =[]
 lchSiml=[]
 jcnSiml=[]
 resSiml=[]
 linSiml = []
 pathSim = {}
 lchSim={}
 wupSim={}
 resSim = {}
 jcnSim= {}
 linSim={}
 lines = text.split('\n')
 for line in lines:
    sentence = str.split(line)
    if len(sentence)>0:
     if sentence[0][0] is not'#':
      sentences.append(sentence)
      if not pathSim.has_key((sentence[0],sentence[1])):
        pathSim[(sentence[0],sentence[1])] = findMax(sentence[0],sentence[1],"path")
        lchSim[(sentence[0],sentence[1])] = findMax(sentence[0],sentence[1],"lch")
        wupSim[(sentence[0],sentence[1])] = findMax(sentence[0],sentence[1],"wup")
        resSim[(sentence[0],sentence[1])] = findMax(sentence[0],sentence[1],"res")
        jcnSim[(sentence[0],sentence[1])] = findMax(sentence[0],sentence[1],"jcn")
        linSim[(sentence[0],sentence[1])] = findMax(sentence[0],sentence[1],"lin")
        sentence0.append(sentence[0])
        sentence1.append(sentence[1])
        sentence2.append(sentence[2])
        pathSiml.append(str(pathSim[(sentence[0],sentence[1])]))
        wupSiml.append(str(wupSim[(sentence[0],sentence[1])]))
        lchSiml.append(str(lchSim[(sentence[0],sentence[1])]))
        resSiml.append(str(resSim[(sentence[0],sentence[1])]))
        jcnSiml.append( str(jcnSim[(sentence[0],sentence[1])]))
        linSiml.append( str(linSim[(sentence[0],sentence[1])]))

 print '\n'+"word 1"

 for sent in sentence0:
  print sent

 print '\n'+"word 2"

 for sent in sentence1:
  print sent

 print '\n'+"gold standard:"

 for sent in sentence2:
  print sent

 print '\n'+"path sim:"

 for sent in pathSiml:
  print sent

 print '\n'+"wup sim:"

 for sent in wupSiml:
  print sent

 print '\n'+"lch sim:"

 for sent in lchSiml:
  print sent

 print '\n'+"res sim:"

 for sent in resSiml:
  print sent

 print '\n'+"jcn sim:"

 for sent in jcnSiml:
  print sent

 print '\n'+"lin sim:"

 for sent in linSiml:
  print sent


if __name__ == '__main__':
    main()
