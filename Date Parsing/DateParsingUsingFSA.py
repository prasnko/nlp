#-------------------------------------------------------------------------------
# Name:        NLP HW 1
# Purpose:	   HW 1
#
# Author:      PRASANNA
#
# Created:     20/09/2012
# Copyright:   (c) PRASANNA 2012
# Licence:     GPL
#-------------------------------------------------------------------------------
import re
class ExceptionFSM(Exception):

    """This is the FSM Exception class."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return `self.value`


def printDate(f):
  print '\n'
  print f.outputSymbol
  dateParts= f.outputSymbol.split()
  if len(dateParts)>=3:
    f.dates.append(f.outputSymbol)
##    f.current_state = f.initial_state

class FSM:

    """This is a Finite State Machine (FSM).
    """

    def __init__(self, initial_state, memory=None):

        """This creates the FSM. You set the initial state here. The "memory"
        attribute is any object that you want to pass along to the action
        functions. It is not used by the FSM. For parsing you would typically
        pass a list to be used as a stack. """

        # Map (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        # Map (current_state) --> (action, next_state).
        self.state_transitions_any = {}
        self.default_transition = None
        self.default_symbols =[]
        self.input_symbol = None
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.next_state = None
        self.action = None
        self.memory = memory
        self.outputSymbol = ""
        self.visited = []
        self.traverseComplete=0
        self.dates = []
    def reset (self):

        """This sets the current_state to the initial_state and sets
        input_symbol to None. The initial state was set by the constructor
        __init__(). """

        self.current_state = self.initial_state
        self.input_symbol = None


    def add_transition (self, input_symbol, state, action=None, next_state=None):

        """This adds a transition that associates:

                (input_symbol, current_state) --> (action, next_state)

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged.

        You can also set transitions for a list of symbols by using
        add_transition_list(). """

        if next_state is None:
            next_state = state
        self.state_transitions[(input_symbol, state)] = (action, next_state)

    def add_transition_list (self, list_input_symbols, state, action=None, next_state=None):

        """This adds the same transition for a list of input symbols.
        You can pass a list or a string. Note that it is handy to use
        string.digits, string.whitespace, string.letters, etc. to add
        transitions that match character classes.

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged. """

        if next_state is None:
            next_state = state
        for input_symbol in list_input_symbols:
            self.add_transition (input_symbol, state, action, next_state)

    def add_transition_any (self, state, action=None, next_state=None):

        """This adds a transition that associates:

                (current_state) --> (action, next_state)

        That is, any input symbol will match the current state.
        The process() method checks the "any" state associations after it first
        checks for an exact match of (input_symbol, current_state).

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged. """

        if next_state is None:
            next_state = state
        self.state_transitions_any [state] = (action, next_state)

    def set_default_transition (self, action, next_state):

        """This sets the default transition. This defines an action and
        next_state if the FSM cannot find the input symbol and the current
        state in the transition list and if the FSM cannot find the
        current_state in the transition_any list. This is useful as a final
        fall-through state for catching errors and undefined states.

        The default transition can be removed by setting the attribute
        default_transition to None. """

        self.default_transition = (action, next_state)

    def get_transition (self, input_symbol, state):

        """This returns (action, next state) given an input_symbol and state.
        This does not modify the FSM state, so calling this method has no side
        effects. Normally you do not call this method directly. It is called by
        process().

        The sequence of steps to check for a defined transition goes from the
        most specific to the least specific.

        1. Check state_transitions[] that match exactly the tuple,
            (input_symbol, state)

        2. Check state_transitions_any[] that match (state)
            In other words, match a specific state and ANY input_symbol.

        3. Check if the default_transition is defined.
            This catches any input_symbol and any state.
            This is a handler for errors, undefined states, or defaults.

        4. No transition was defined. If we get here then raise an exception.
        """
        if input_symbol.isdigit():
            if float(input_symbol)>0 and float(input_symbol)<32 and state != 'qf' and len(self.visited)<3:
                self.next_state='q2'
                self.action=None
            elif float(input_symbol)>1000 and float(input_symbol)<3000:
                self.next_state='qf'
                self.action=printDate
            elif 'q1' in self.visited:
              self.next_state='qf'
              self.action=printDate
            elif self.default_transition is not None:
                return self.default_transition
            return {self.action,self.next_state}
        if self.state_transitions.has_key((input_symbol, state)):
            return self.state_transitions[(input_symbol, state)]
        elif self.state_transitions_any.has_key (state):
            return self.state_transitions_any[state]
        elif not input_symbol.isdigit():
            if state=='q1' or state=='q2':
                self.next_state='qf'
                self.action=printDate
            return {self.next_state,self.action}
        elif self.default_transition is not None:
            return self.default_transition
##        else:
##            raise ExceptionFSM ('Transition is undefined: (%s, %s).' %
##                (str(input_symbol), str(state)) )

    def process (self, input_symbol):

        """This is the main method that you call to process input. This may
        cause the FSM to change state and call an action. This method calls
        get_transition() to find the action and next_state associated with the
        input_symbol and current_state. If the action is None then the action
        is not called and only the current state is changed. This method
        processes one complete input symbol. You can process a list of symbols
        (or a string) by calling process_list(). """

        self.input_symbol = input_symbol
##        print self.input_symbol
##        print self.current_state
        (self.action, self.next_state) = self.get_transition (self.input_symbol, self.current_state)

        if(self.current_state=='q0' and self.traverseComplete==1):
            del self.visited[:]
            self.visited.append('q0')
            self.traverseComplete = 0

        if self.next_state not in self.visited:
           self.visited.append(self.next_state)

        if(self.next_state=='qf'):
            if(self.current_state=='q1' or self.current_state=='q2'):
                if input_symbol.isdigit():
                    self.outputSymbol += input_symbol+' '

        if(self.next_state=='qf'):
            if(self.current_state=='q0'):
                self.outputSymbol = self.input_symbol

        if(self.next_state=='q1' or self.next_state=='q2'):
            self.outputSymbol += input_symbol+' '
        if self.action is not None:
            self.action (self)
        if(self.next_state != 'qf'):
            self.current_state = self.next_state
        else:
            self.current_state = self.initial_state
            self.outputSymbol=""
            self.traverseComplete=self.traverseComplete+1
            del self.visited[:]
        self.next_state = None

    def process_list (self, input_symbols):

        """This takes a list and sends each element to process(). The list may
        be a string or any iterable object. """

        for s in input_symbols:
            self.process (s)

    def getWords():
        p=open("C:\Prasanna\HW1-test.txt",'r')
        line=p.read()
        words= re.split('/W+',line)
        return words

def Error (fsm):
##    print 'That does not compute.'
## print str(fsm.input_symbol)
 default = []
 default.append(fsm)


def main():
    f = FSM ('q0', []) # "memory" will be used as a stack.
    months = ['Jan','January','Feb','February','Mar','March','Apr','April','May','May','Jun','June','Jul','July','Aug','August','Sep','September','Oct','October','Nov','November','Dec','December']
    datesJoined=['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th','31st']
##    holidays=['Christmas','Labor','Thanksgiving','Winter','Memorial','Independence']
##    day=['day','Day','holiday','Holiday']
    f.set_default_transition (Error, 'q0')
    f.add_transition_any  ('q0', None, 'q0')
    f.add_transition_list(months,'q0',None,'q1')
##    f.add_transition_list(holidays,'q0',printDate,'qf')
    f.add_transition_list(months,'q2',None,'q1')
    f.add_transition_list(datesJoined,'q0',None,'q2')
    f.add_transition_list(datesJoined,'q1',None,'q2')
    f.add_transition('of','q1',None,'q1')
    f.add_transition('of','q2',None,'q2')
    f.add_transition('th','q2',None,'q2')
    f.add_transition('st','q2',None,'q2')
    f.add_transition('nd','q2',None,'q2')
    f.add_transition('rd','q2',None,'q2')
    p=open(r'C:\Prasanna\HW1-test.txt','r')
    line=p.read()
    words= re.split('\W+',line)
    f.process_list(words)
    for date in f.dates:
       year=""
       day=""
       month=""
       dateParts= date.split()
       if len(dateParts)>=3:
        for datePart in dateParts:
            if months.count(datePart)>0:
                mIndex = months.index(datePart)
                if mIndex%2==0:
                  month = (mIndex/2)+1
                  continue
                else:
                  month = ((mIndex-1)/2)+1
                  continue
            if datePart.isdigit():
                if float(datePart)<32 and float(datePart)>0:
                    day = datePart
                    continue
                elif float(datePart)>1000 and float(datePart)<3000:
                    year = datePart
                    continue
        if day=="":
            for datePart in dateParts:
                if datesJoined.count(datePart)>0:
                    day = datePart[:-2]
                    break
        if str(year)!="" and str(month)!="" and str(day)!="":
            print str(year)+'-'+str(month)+'-'+str(day)
            break

if __name__ == '__main__':
    main()
