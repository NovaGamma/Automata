import os

import Int1_8_Table as Table        #importing the library to sidplay the transition table

from copy import deepcopy           #importing the deepcopy method to make duplicate of arrays

class Node():                       #creating Class Node, which correspond to a state in the automaton
    def __init__(self, name, isEntry = False, isOutput = False):
        self.isEntry = isEntry                                          #boolean to know if the state is an Entry and/or Terminal
        self.isOutput = isOutput
        self.name = name
        self.alphabet = ["%c"%x for x in range(97,97+size_alphabet)]    #creating an array containing all the letter in the alphabet of the automaton  "%c"%x is used to convert an integer (corresponding to an ASCII code here) to the corresponding character
        self.transitions = []                                           #the list that will contain the transitions of the state

    def __repr__(self):                   #magic method in python used to represent the object in a print(object) for example or just in the conversion to str : str(object)
        return "{}".format(self.name)

    def display(self):                     #function used to display a State, only used for debugging
        return "label : {}\n{}Transitions : {}\n\n".format(self.name,"Initial and Final\n" if self.isEntry and self.isOutput else "Initial\n" if self.isEntry else "Final\n" if self.isOutput else "",self.transitions if len(self.transitions) > 0 else "None")

    def __lt__(self, other):                #rewriting the comparator methods for Nodes to be able to sort a list of Nodes, using the .sort() method
        return self._name() < other._name() #telling it to just compare the names (in the form of a list to be able to compare fused states)
                                            #doing it for all comparator < <= == >= >
    def __le__(self,other):                 #comparator <=
        return self._name() <= other._name()
    def __eq__(self,other):                 #comparator ==
        return self._name() == other._name()
    def __ge__(self,other):                 #comparator >=
        return self._name() >= other._name()
    def __gt__(self,other):                 #comparator >
        return self._name() > other._name()

    def _name(self):                        #function used in the comparator, that return an array with the name decomposed
                                            #if the name is 1.2 will return ['1','2']
        if self.name == 'P':
            return ['P']
        return [number for number in str(self).split('.')]

    def __add__(self,other):                #another magic method used when you write a + b here used to combine to states in the automaton
        if self.name == '':                 #if the name is empty it mean that it's a placeholder, meaning that we do not have anything to combine
            return other
        elif other.name == '':
            return self
        #getting the name of the combined state and creating the corresponding Node
        sepS = self.name.split(".")     #equivalent to the _name method
        sepO = other.name.split(".")
        sep = sepS + sepO
        name = []

        #making the name composed of the two state to combine
        for t in sep:
            if t not in name:
                name.append(t)
        name.sort()
        name = ".".join(name)

        #creating the resulting Node
        result = Node(name, isOutput = True if self.isOutput or other.isOutput else False)
        result = self._fuseTransitions(other,result)     #fusing the normal transitions
        result = self._fuseAsync(other,result)           #fusing the epsilon transitions
        return result

    def _fuseTransitions(self,other,result):
        for letter in self.alphabet:#fusing all the transitions by going through all the letter in the alphabet of the automaton
            selfT = ''
            otherT = ''
            for t in self.transitions:#finding a transition corresponding to the letter in the first state
                if t[0] == letter:
                    selfT = t
            for t in other.transitions:#finding the transition in the second state
                if t[0] == letter:
                    otherT = t
            if otherT == '':#if we do not find one it means that there is no transition with that letter
                if selfT != '':#mean that only selfT has a transition for that letter
                    result.transitions.append(selfT)#thus for this letter only the first state has transition so no fusing necessary
            elif selfT == '':#same than above but the other way around
                if otherT != '':
                    result.transitions.append(otherT)
            elif not(otherT) == '' and not(selfT) == '':#mean that both contain a transition
                temp = selfT[1] + otherT[1]
                temp2 = []
                for t in temp:
                    if t not in temp2:
                        temp2.append(t)
                temp2.sort()#
                result.transitions.append([letter,temp2])
        return result

    def _fuseAsync(self,other,result):
        letter = '*'
        selfT = ''
        otherT = ''
        for t in self.transitions:#finding the transition corresponding to the epsilon transition
            if t[0] == letter:
                selfT = t
        for t in other.transitions:#finding the transition in the second state
            if t[0] == letter:
                otherT = t
        if otherT != '':
            if self in otherT[1]:
                otherT[1].pop(otherT[1].index(self))
        if selfT != '':
            if other in selfT[1]:
                selfT[1].pop(selfT[1].index(other))
        if otherT == '':            #if we do not find one it means that there is no epsilon transition
            if selfT != '':         #mean that only selfT has a transition for that letter
                result.transitions.append(selfT)#thus for this letter only the first state has transition so no fusing necessary
        elif selfT == '':           #same than above but the other way around
            if otherT != '':
                result.transitions.append(otherT)
        elif not(otherT) == '' and not(selfT) == '':#mean that both contain a transition
            temp = selfT[1] + otherT[1]
            temp2 = []
            for t in temp:
                if t not in temp2:
                    temp2.append(t)
            temp2.sort()#
            result.transitions.append([letter,temp2])
        return result

    def combine(self):      #combining transitions after laoding the automaton from a file
                            #because they can be in the form [['a',[0]],['a',[1]]] -> [['a',[0,1]]]
                            #to have only one object in the list corresponding to a letter in the alphabet
        new = []
        for letter in self.alphabet:
            #list comprehension, you can check the int1-8-Example.py file to see how they work
            temp = [t[1] for t in self.transitions if t[0]==letter] #getting all the transitions ['letter',[X]] from the list
            if len(temp)>0:         #if there is at least one we combine them
                temp.sort()         #first we sort them to avoid having [1,0]
                newT = [temp]
                newT.insert(0,letter)
                new.append(newT)

        #doing the same than above but for epsilon transitions represented by a *
        #because the * is not in the alphabet
        temp = [t[1] for t in self.transitions if t[0]=='*']
        if len(temp)>0:
            temp.sort()
            newT = [temp]
            newT.insert(0,'*')
            new.append(newT)
        self.transitions = new

    def isAsync(self):
        #to know if the automaton is async we just need to find one epsilon transitions
        for transition in self.transitions:
            #we got through all the transitions until we find one epsilon
            if transition[0] == '*':
                return True
        #if we haven't found any we return False
        return False


    def getEpsilon(self):
        #function to get the list of epsilon transitions
        for transition in self.transitions:
            if transition[0] == '*':
                #since the transitions have been combined (see combine() function) we have only one that contain all
                return transition[1]

        #if we haven't found any we return an empty list
        return []

class Automaton():          #the class that hold the tables, and the list of states -> States of Node objects
    def __init__(self,states = [],isNotDet = False,isAsync = False):
        self.states = states    #a list of Node object that come from the load() function
        self.combine()          #combining the transitions -> see the function to ahve more details
        self.isNotDet = isNotDet#we can check if it's deterministic while loading the automaton from the file
        self.alphabet = ["%c"%x for x in range(97,97+size_alphabet)] #see the Node class definition to see how it work

    def __repr__(self):     #magic method used to display all the states of the automaton (for debug purposes)
        output = "Alphabet : {}\n\n".format(self.alphabet)
        output2 = "".join(state.display() for state in self.states) #will call the display() function for all states in the automaton
        return output + output2

    def table(self,input = []):
        #function that uses the Table from Int1_8_Table, which Elvin has rewrote from the PTable python library
        #this library is also used by the group Int2-6 hence their function being similar, because it implements the same function
        #the code in the Table file is not commented because it's not part of the project, it's to be considered as a normal library
        #I (Elvin) rewrote it just for it to be easier for you to run it, avoiding the need to install the original library

        if input == []:#a default parameter meaning that we display the base automaton table
            input = self.states

        table = Table.Table() #initializing the Table object

        fields = [letter for letter in self.alphabet] #the fields are the names of the columns, it's composed of all the letters+ the * for epsilon transition if they exist
        asynchronous = False
        if isAsync(input):
            asynchronous = True
        if asynchronous:
            #if the table is asynchronous we add the field *
            fields.append('*')
        fields.insert(0,"States")
        table.field_names = fields

        for state in input:
            #each state will correspond to a row in the resulting table

            #we initialyse the row with empty characters, to have a placeholder for a non complete Automaton
            #for which there might be some non-existing transitions
            row = [' ' for i in range(len(self.alphabet) + 1*asynchronous)]
            state.transitions.sort()

            #a long ternary operator to determine if the state is an Entry, a Terminal state or both or nothing
            row.insert(0,"{}{}".format("<->" if state.isOutput and state.isEntry else " <-" if state.isOutput else " ->" if state.isEntry else "   ",state.name))
            for x in state.transitions:
                text = [str(t) for t in x[1]]
                index = fields.index(x[0])
                row[index] = " , ".join(text)
            table.add_row(row)
        return table

    def isDeterministic(self,table = ''):
        #to know if an automaton is deterministic we just have to check if a transition has multiple destinations
        #Example : [['a',[1,2]]] -> for the letter a there is multiple choice the state 1 or 2 -> the state is nonDeterministic
        if table == '':
            table = self.states
        for state in table:
            for transition in state.transitions:
                #in [['a',[1,2]]] correspong to this part
                #           ^
                if len(transition[1]) > 1:
                    return False
        return True

    def determinize(self,det_table = 'None'):
        if det_table == 'None':#first part of the algorithm
            if self.isNotDet:#mean that there is multiple entries
                init_entries = [entry for entry in self.states if entry.isEntry]#getting the list of states being entries in the automaton
                entries = deepcopy(init_entries)
                new_state = Node('')
                for i in range(0,len(entries)):
                    new_state = new_state + entries[i]
                new_state.isEntry = True
                det_table = [new_state]
            else:
                entry = [entry for entry in self.states if entry.isEntry]#here we have only one entry but get it in the form of a list because the way of searching is more efficient
                det_table = deepcopy(entry)
        #if we got here it means that either the det_table was empty and we filled it or it was already created
        added = True
        while added:
            added = False
            for state in det_table:
                for transition in state.transitions:
                    if len(transition[1]) > 1:#mean that we have a composite state to create
                        temp = [str(t) for t in transition[1]]
                        #removing duplicates in temp to have a clean name
                        temp2 = []
                        for t in temp:
                            temp3 = t.split(".")
                            for i in temp3:
                                if i not in temp2:
                                    temp2.append(i)
                        name = ".".join(temp2)
                        found = False
                        for s in det_table:
                            if str(s.name) == name:
                                transition[1] = [s]
                                found = True
                        if not(found):
                            added = True
                            new_state = Node('')
                            for i in range(0,len(transition[1])):
                                new_state = new_state + transition[1][i]
                            transition[1] = [new_state]
                            det_table.append(new_state)
                    else:#looking for primordial states that were not added to the det_table
                        for s in self.states:
                            if str(s.name) == transition[1][0].name:
                                if s not in det_table:
                                    s.isEntry = False
                                    det_table.append(deepcopy(s))
                                    added = True
        return det_table

    def isComplete(self,table = ''):
        if table == '':
            table = self.states
        for state in table:
            for letter in self.alphabet:
                found = False
                for transition in state.transitions:
                    if letter == transition[0]:
                        found = True
                if not found:
                    return False
        return True

    def complete(self,table = ''):
        if table == '':
            table = self.det_table
        complete = deepcopy(table)
        sink = Node('P')
        sink.transitions = [[letter,[sink]] for letter in self.alphabet]
        for state in complete:
            for letter in self.alphabet:
                found = False
                for transition in state.transitions:
                    if letter == transition[0]:
                        found = True
                if not found:
                    state.transitions.append([letter,[sink]])
            state.transitions.sort()
        complete.append(sink)
        return complete

    def combine(self):
        for state in self.states:
            state.combine()

    def recognize(self,word,table):
        entry = [entry for entry in table if entry.isEntry]
        pos = entry[0]
        for letter in word:
            found = False
            for transition in pos.transitions:
                if transition[0] == letter:
                    found = True
                    pos = transition[1][0]
            if not found:
                return False
        if pos.isOutput:
            return True
        return False

    def complementary(self,table):
        complement = deepcopy(table)
        for state in complement:
            if state.isOutput:
                state.isOutput = False
            else:
                state.isOutput = True
        return complement

    def isStandard(self):
        entries = [entry for entry in self.states if entry.isEntry]
        if len(entries) > 1:
            return 0
        for state in self.states:
            for transition in state.transitions:
                if entries[0] in transition[1]:
                    return 0
        return 1

    def standardize(self):
        states = deepcopy(self.states)
        new_state = Node('i')
        transitions = [state.transitions for state in states if state.isEntry]
        for state in states:
            if state.isEntry:
                state.isEntry = False
        t_comb = []
        for t in transitions:
            for t2 in t:
                t_comb.append(t2)
        transitions = t_comb
        new_state.isEntry = True
        new_state.transitions = transitions
        new_state.combine()
        # transform [['a', [[0, 1]]], ['b', [[2]]]] to [['a', [0, 1]], ['b', [2]]]
        for transition in new_state.transitions:
            combine = []
            for t in transition[1]:
                if len(t) > 1:
                    for t2 in t:
                        combine.append(t2)
                else:
                    combine.append(t[0])
            transition[1] = combine
        states.append(new_state)
        self.standard = states
        return states

    def minimize(self,data):
        states = deepcopy(data)
        #first part it to get the sub groups using the Terminal states
        T = [state for state in states if state.isOutput]
        groups = {}
        for state in states:
            type = ''
            for transition in state.transitions:
                if transition[1][0] in T:
                    type += 'T'
                else:
                    type += 'NT'
            if not type in groups.keys():
                groups[type] = [state]
            else:
                groups[type].append(state)

        groups = dict_names(groups)

        #Now we will iterate the function until we have the same set at the beginning and at the end
        previous = {}
        while previous != groups:
            previous = groups
            groups = {}
            for key,group in previous.items():
                if len(group) > 1:
                    for state in group:
                        type = ''
                        for transition in state.transitions:
                            for key,sub_group in previous.items():
                                if transition[1][0] in sub_group:
                                    type += key
                        if not type in groups.keys():
                            groups[type] = [state]
                        else:
                            groups[type].append(state)
                else:
                    groups[key] = group
            groups = dict_names(groups)

        #now we will rebuild the table based on the obtained dictionnary
        minimized = []
        for _,group in groups.items():
            if len(group) > 1:
                #fusing the states if it should be a fused state
                new_state = Node("")
                entry = False
                for state in group:
                    if state.isEntry:
                        entry = True
                    new_state = new_state + state
                if entry:
                    new_state.isEntry = True
                minimized.append(new_state)
            else:
                minimized.append(group[0])
        return minimized

    def synchronize(self):
        states = deepcopy(self.states)

        while True:
            position = []
            path = []

            for state in states:
                if state.isAsync():
                    position.append(state)
                    break
            if position == []:
                states = removeUselessStates(states)
                return states
            initial = position[0]
            empty = []
            while position != []:
                pos = position[0]
                epsilon = pos.getEpsilon()
                for direction in epsilon:
                    if not direction in path:
                        if direction.isAsync() and len(direction.transitions) == 1 and not direction.isOutput:
                            position.append(direction)
                            empty.append(direction)
                        else:
                            path.append(direction)
                position.remove(pos)

            new_transition = []
            for state in path:
                if not state.transitions == []:
                    for transition in state.transitions:
                        new_transition.append(transition)
                elif state.isOutput:
                    initial.isOutput = True

            letters = deepcopy(self.alphabet)
            letters.append('*')

            if initial.isAsync and len(initial.transitions) > 1:
                initial.transitions.remove(initial.getEpsilon())
                new_transition.append(initial.transitions)
            initial.transitions = async_combine(new_transition,letters)


            to_remove = []
            for state in empty:
                #we are going to find the states that point toward those to see if it has only one access
                found = 0
                for s in states:
                    if not s in empty:
                        for transition in s.transitions:
                            if state in transition[1]:
                                found += 1
                if found == 0:
                    to_remove.append(state)

            for state in to_remove:
                states.remove(state)

def dict_names(groups):
    new = {}
    for _,group in groups.items():
        temp = [str(state) for state in group]
        new_name = '|'.join(temp)
        new[new_name] = group
    return new

def isAsync(states):
    for state in states:
        for transition in state.transitions:
            if transition[0] == '*':
                return True
    return False

def async_combine(transitions,letters):
    new = []
    for letter in letters:
        temp = []
        for t in transitions:
            if t[0]==letter:
                for t2 in t[1]:
                    temp.append(t2)
        if len(temp)>0:
            temp.sort()
            newT = [temp]
            newT.insert(0,letter)
            new.append(newT)
    return new

def removeUselessStates(states):
    to_remove = []
    for state in states:
        #we are going to find the states that point toward those to see if it has an access
        if not state.isEntry:
            found = 0
            for s in states:
                for transition in s.transitions:
                    if state in transition[1]:
                        found += 1
            if found == 0:
                to_remove.append(state)

    for state in to_remove:
        states.remove(state)

    return states

def load(path):
    global size_alphabet
    with open(path,'r') as file:
        isNotDet = None
        size_alphabet = int(file.readline())
        n_state = int(file.readline())

        states = []
        for i in range(n_state):#initialize the list to put the states in order corresponding to their label
            states.append(Node(str(i)))

        initial = file.readline().rstrip('\n').split(':')#the rstrip removes the new line character at the end of the line that could cause issues
        if int(initial[0]) > 1:
            isNotDet = True
        initial.pop(0)
        for i in initial:
            states[int(i)].isEntry = True

        final = file.readline().rstrip('\n').split(':')
        final.pop(0)
        for i in final:
            states[int(i)].isOutput = True

        isAsync = False

        for i in range(int(file.readline())):#reading directly the number of transitions, no rstrip because the conversion to int type removes it
            t = file.readline().rstrip('\n').split(':')
            if not isAsync:
                if t[1] == '*':
                    isAsync = True
            states[int(t[0])].transitions.append([t[1],states[int(t[2])]])

    return Automaton(states,isNotDet,isAsync)
