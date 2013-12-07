#-------------------------------------------------------------------------------
# Name:        Viterbi Algorithm
# Purpose:     NLP HW3
#
# Author:      PRASANNA
#
# Created:     03/10/2012
# Copyright:   (c) PRASANNA 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

class ViterbiAlgo:

   def __init__(self):
    self.viterbi = {}
    self.backpointer={}
    self.a={}           ## transition probabilities
    self.b={}           ## emssion probabilities
    self.q={}
    self.o=[]           ## observation sequence
    self.vList = {}     ## used to find maximum of previous two states

   def populateData(self,sequence):
        self.q[1,1]= 1                  ##q[state,time]
        self.q[2,1]= 2
        self.q[1,2]= 1
        self.q[2,2]= 2
        self.q[1,3]= 1
        self.q[2,3]= 2
        self.q[1,4]= 1
        self.q[2,4]= 2
        self.q[1,5]= 1
        self.q[2,5]= 2
        self.q[1,6]= 1
        self.q[2,6]= 2
        self.q[1,7]= 1
        self.q[2,7]= 2
        self.q[1,8]= 1
        self.q[2,8]= 2
        self.q[1,9]= 1
        self.q[2,9]= 2
        self.q[1,10]= 1
        self.q[2,10]= 2

        del self.o[0:len(self.o)]
        if sequence==1:
         self.o.append('')
         self.o.append(3)
         self.o.append(1)
         self.o.append(2)
         self.o.append(3)
         self.o.append(1)
         self.o.append(2)
         self.o.append(3)
         self.o.append(1)
         self.o.append(2)
        else:
         self.o.append('')
         self.o.append(3)
         self.o.append(1)
         self.o.append(1)
         self.o.append(2)
         self.o.append(3)
         self.o.append(3)
         self.o.append(1)
         self.o.append(1)
         self.o.append(2)

        self.a[0,1] = 0.8
        self.a[0,2] = 0.2
        self.a[1,2] = 0.3
        self.a[2,1] = 0.4
        self.a[1,1] = 0.7
        self.a[2,2] = 0.6

        self.b[1,1] = 0.2
        self.b[2,1] = 0.4
        self.b[3,1] = 0.4
        self.b[1,2] = 0.5
        self.b[2,2] = 0.4
        self.b[3,2] = 0.1

        self.backpointer[1,1]=''
        self.backpointer[1,2]=''
        self.backpointer[2,1]=''
        self.backpointer[2,2]=''

   def getBestPath(self,N,T):
        ## viterbi and backpointer for start state
        for s in range(1,N+1):
            self.viterbi[s,1]=self.a[0,s]*self.b[self.o[1],s]
            self.backpointer[s,0]=''
            self.backpointer[s,1]=0

        ## viterbi and backpointer for other states
        for t in range(2,T+1):
            for s in range(1,N+1):
             for sd in range(1,N+1):
              self.vList[(self.viterbi[sd,t-1]*self.a[sd,s]*self.b[self.o[t],s])]= sd   ##storing state having maximum viterbi path probability as value for viterbi path probability as key
             self.viterbi[s,t]=max(self.vList.iterkeys())                               ## getting previous state with maximum viterbi value
             smax=self.vList[self.viterbi[s,t]]
             self.vList.clear()
             self.backpointer[s,t]=''
             self.backpointer[s,t]+= str(self.q[smax,t-1])                              ## storing the backpointer

        totalBackPointer = ''

        ## traversing from final to start state to find maximum probability path
        for t in range(T,1,-1):
            if t==T:                                                                    ## for final state(time slot)
                sb=int(self.backpointer[smax,t])
                totalBackPointer=str(smax)
                totalBackPointer+=self.backpointer[smax,t]
            else:                                                                       ## for other states (time slot)
                sb=int(self.backpointer[sb,t])
                totalBackPointer+=self.backpointer[sb,t]
        totalBackPointer+='0'
        s = totalBackPointer
        ## reversing string to get original order of states
        s = s[::-1]
        output=''
        for c in s:
            if int(c)==1:
                output+='Hot->'
            elif int(c)==2:
                output+='Cold->'
            else:
                output+='Start->'
        output=output[:-2]
        print output

    ##312312312
   def sequence1(self):
    self.populateData(1)
    self.getBestPath(2,9)

    ##311233112
   def sequence2(self):
    self.populateData(2)
    self.getBestPath(2,9)

def main():
    v = ViterbiAlgo()
    print 'Sequence 1 (312312312): '
    v.sequence1()
    print 'Sequence 2 (311233112): '
    v.sequence2()


if __name__ == '__main__':
    main()
