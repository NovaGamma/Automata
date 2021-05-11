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
    def __init__(self,states = [],isNotDet = False):
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
        if self.isNotDet:
            return False
        if table == '':
            table = self.states
        for state in table:
            for transition in state.transitions:
                #in [['a',[1,2]]] correspong to this part
                #           ^
                if len(transition[1]) > 1:
                    return False
        return True

    def determinize(self,table = None):
        if table is None:
            table = self.states
        if self.isNotDet:#mean that there is multiple entries
            init_entries = [entry for entry in table if entry.isEntry]#getting the list of states being entries in the automaton
            entries = deepcopy(init_entries)

            #fusing the entries to obtain the entry state for the determinisic table
            new_state = Node('')
            for i in range(0,len(entries)):
                new_state = new_state + entries[i]
            new_state.isEntry = True
            det_table = [new_state]
        else:
            entry = [entry for entry in table if entry.isEntry]#here we have only one entry but get it in the form of a list because the way of searching is more efficient
            det_table = deepcopy(entry)

        #here we will add all the fused states that need to be created, or the primordial one to be added
        added = True
        while added:
            added = False
            #we will check for each state in the det_table
            for state in det_table:
                for transition in state.transitions:
                    if len(transition[1]) > 1:#mean that we have a composite state to create
                        temp = [str(t) for t in transition[1]]
                        #removing duplicates in temp to have a clean name

                        #creating the name of the resulting state
                        temp2 = []
                        for t in temp:
                            temp3 = t.split(".")
                            for i in temp3:
                                if i not in temp2:
                                    temp2.append(i)
                        name = ".".join(temp2)

                        #then we check if this state already exists in the det_table
                        found = False
                        for s in det_table:
                            if str(s.name) == name:
                                transition[1] = [s]
                                found = True
                        #if we did not find it we will create it and add it to the table
                        if not found:
                            added = True
                            new_state = Node('')
                            #fusing all the states that composed the combined state
                            for i in range(0,len(transition[1])):
                                new_state = new_state + transition[1][i]
                            transition[1] = [new_state]
                            #adding it to the table
                            det_table.append(new_state)
                    else:#looking for primordial states that were not added to the det_table
                        for s in self.states:
                            #we check for each existing primordial state
                            if str(s.name) == transition[1][0].name:
                                if s not in det_table:
                                    #if it's not in the det_table we add it, but remove the isEntry to avoir having two entries in a determniistic automaton
                                    s.isEntry = False
                                    det_table.append(deepcopy(s))
                                    added = True
        return det_table

    def isComplete(self,table = ''):
        #to check if the table is complete we just have to check if there exists a transitions for each letter in the alphabet
        if table == '':
            table = self.states
        for state in table:
            for letter in self.alphabet:
                found = False
                #we check if there exist one transitions corresponding to the letter
                for transition in state.transitions:
                    if letter == transition[0]:
                        found = True
                if not found:
                    #if we did not found it it means that the automaton isn't complete
                    return False
        return True

    def complete(self,table = ''):
        #to complete the automaton we just need to set the missing transitions to a sink state P
        if table == '':
            table = self.det_table
        complete = deepcopy(table)
        #creating the sink state P
        sink = Node('P')
        #setting it's transitions to itself for each letter in the alphabet
        sink.transitions = [[letter,[sink]] for letter in self.alphabet]

        #then we go trough each state to find the missing transitions
        for state in complete:
            for letter in self.alphabet:
                found = False
                for transition in state.transitions:
                    if letter == transition[0]:
                        found = True
                if not found:
                    #if we didn't found the transition corresponding to the letter we add one to P
                    state.transitions.append([letter,[sink]])
            state.transitions.sort()
        complete.append(sink)
        return complete

    def combine(self):
        #method for the automaton class used to call the combine method of the Node class
        #for all states in the automaton
        for state in self.states:
            state.combine()

    def recognize(self,word,table):
        #to recognize a word, we first get the word and the table and which we will try to recognize
        entry = [entry for entry in table if entry.isEntry] #we get the entry of the automaton
        pos = entry[0]                                      #and we set our starting position at this entry
        for letter in word:                                 #then we will try to go trough the automaton following the letter in the word
            found = False
            for transition in pos.transitions:              #in all the transitions of the state where we currently are
                                                            #we will try to find a a transitions corresponfing to the letter of the word
                if transition[0] == letter:
                    found = True
                    pos = transition[1][0]
            if not found:
                return False
        if pos.isOutput:
            return True
        return False

    def complementary(self,table):
        #to do the complementary we just flip the value of isOutput for each state in the automaton
        complement = deepcopy(table)
        for state in complement:
            if state.isOutput:
                state.isOutput = False
            else:
                state.isOutput = True
        return complement

    def isStandard(self,table = ''):
        #there is two ways for an automaton to not be standard
        if table == '':
            table = self.states
        entries = [entry for entry in table if entry.isEntry]
        #the first one is having multiple entries so we get the list of entries and check it's length
        #if it's greater than 1 it mean that the automaton is not standard
        if len(entries) > 1:
            return False
        #the other way is for the automaton to have transitions that goes back to the netry state
        #so we check for each transitions in each state if there is a transition that goes back to the entry
        for state in table:
            for transition in state.transitions:
                if entries[0] in transition[1]:
                    return False
        return True

    def standardize(self, table = ''):
        if table == '':
            table = self.states
        states = deepcopy(table)
        #to standardize we will create a new state that will be the fusion of all the entry states
        new_state = Node('i')
        #we get the transitions of all the entry states
        transitions = [state.transitions for state in states if state.isEntry]
        #we set all to entry states to not be entries anymore
        for state in states:
            if state.isEntry:
                state.isEntry = False
        #then we combine the transitions for i, and we remove the duplicate transtitions
        t_comb = []
        for t in transitions:
            for t2 in t:
                t_comb.append(t2)
        transitions = t_comb
        #we set the i state to be an entry and it's transitions to be the list of the transitions of the previous entries
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
        return states

    def minimize(self,data):
        states = deepcopy(data)
        #first part it to get the sub groups using the Terminal states

        #we get the list of terminal states
        T = [state for state in states if state.isOutput]
        groups = {}
        #we check for each state if it point toward a terminal state or not
        #we build a type using this
        for state in states:
            type = ''
            for transition in state.transitions:
                if transition[1][0] in T:
                    #mean that it's a terminal state so we add T to the type
                    type += 'T'
                else:
                    #else NT
                    type += 'NT'
            #we check if there already exists states which posess this type else we create it
            if not type in groups.keys():
                groups[type] = [state]
            else:
                groups[type].append(state)

        #we rename the subgroups
        #see the method for more info
        groups = dict_names(groups)

        #Now we will iterate the function until we have the same set at the beginning and at the end
        previous = {}
        iter = 0
        #setting an iter to avoid looping problems
        while not previous == groups and iter < 100:
            previous = groups
            groups = {}
            #we check for each state of each subgoup to which subgroup it's transitions point to
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
            iter += 1

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

        for state in minimized:
            for transition in state.transitions:
                for i,destination in enumerate(transition[1]):
                    #if the destination isn't already a fused state
                    if not destination in minimized:
                        name = str(destination)
                        for state_name in minimized:
                            names = str(state_name).split('.')
                            if name in names:
                                transition[1][i] = state_name
                temp2 = []
                for temp in transition[1]:
                    if not temp in temp2:
                        temp2.append(temp)
                transition[1] = temp2
        return minimized

    def synchronize(self):
        states = deepcopy(self.states)

        while True:
            position = []
            path = []

            #we get the first state that has epsilon transitions in the list of states
            for state in states:
                if state.isAsync():
                    position.append(state)
                    break

            #if we didn't found any state with epsilon transitions it mean that the automaton is synchronous
            if position == []:
                #we remove the useless states -> those that will never be accessed
                states = removeUselessStates(states)
                #and we return the automaton
                return states

            #we start from the state having epsilon transitions
            initial = position[0]
            empty = []
            #we will traverse the automaton trough the epsilon transitions
            while position != []:
                pos = position[0]
                epsilon = pos.getEpsilon()
                for direction in epsilon:
                    if not direction in path:
                        #if check if the state were it's pointing is async and has transition and is not the terminal state
                        if direction.isAsync() and len(direction.transitions) == 1 and not direction.isOutput:
                            #if yes it mean that we can continue in this direction
                            position.append(direction)
                            empty.append(direction)
                        else:
                            #otherwise we stop here and now that the initial state will point directly toward this one
                            path.append(direction)
                position.remove(pos)

            #then after finding each non async state where the initial can point toward
            #we create the new transitions for the initial state
            new_transition = []
            for state in path:
                if not state.transitions == []:
                    #we add in a list all the transitions of those states
                    for transition in state.transitions:
                        new_transition.append(transition)
                #and if it point toward the terminal state, it mean that it will be terminal aswell
                elif state.isOutput:
                    initial.isOutput = True

            letters = deepcopy(self.alphabet)
            letters.append('*')

            #getting the transitions of the initial state if the state is async and there non epsilon transitions
            if initial.isAsync() and len(initial.transitions) > 1:
                #we get and remove the epsilon transitions and then add the remaining transitions to the list
                for transition in initial.transitions:
                    if transition[0] == '*':
                        to_remove = transition
                initial.transitions.remove(to_remove)
                new_transition.append(initial.transitions)
            #we fuse all the epsilon transitions into one
            initial.transitions = async_combine(new_transition,letters)

            #equivalent to the removeUselessStates method but just for the empty list
            to_remove = []
            for state in empty:
                #we check for each state to see if one has a transition going to the state to remove
                found = 0
                for s in states:
                    if not s in empty:
                        for transition in s.transitions:
                            if state in transition[1]:
                                found += 1
                if found == 0:
                    #if it doesn't have one we add it to the list
                    to_remove.append(state)

            #and then we remove it from the list of states
            for state in to_remove:
                states.remove(state)

def dict_names(groups):
    #this function is used to change the name of the groups in the minimization
    #we set the names to be composed of the names of the states that are in the group
    new = {}
    for _,group in groups.items():#see the Example file to have example of the .items() method
        #we go trough the entire group which is a dictionnary that contain the other subgroups
        #and for each subgroup we get the name of each state and then create a string from it
        temp = [str(state) for state in group]
        new_name = '|'.join(temp)
        #and we set it as the new name of the subgroup
        new[new_name] = group
    return new

def isAsync(states):
    #a second method used to know if the automaton is async
    #it's juste calling the isAsync method of each state
    for state in states:
        if state.isAsync():
            return True
    return False

def async_combine(transitions,letters):
    #here we combine the epsilon transitions as we would to in the combine method
    #it works the same way so check the comments in this method
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

        for i in range(int(file.readline())):#reading directly the number of transitions, no rstrip because the conversion to int type removes it
            t = file.readline().rstrip('\n').split(':')
            states[int(t[0])].transitions.append([t[1],states[int(t[2])]])

    return Automaton(states,isNotDet)
