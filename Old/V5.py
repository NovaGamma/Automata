import os
try:
    from prettytable import PrettyTable
except ModuleNotFoundError:
    a = input("A library is missing (PrettyTable/PTable) do you want to install it ? (y/n)\nif you don't install it the programm will not work properly\nYou can install it on your own by running 'pip install PTable' in your cmd\n")
    if a == 'y':
        os.system('cmd /c "pip install PTable"')#installing the library used to display the table in a pretty way if it's not found by the program
        _ = os.system('cls')#cleanign the screen after the installation
        from prettytable import PrettyTable
    else:
        raise Exception("The program cannot run properly, missing library(PTable)")
from copy import deepcopy

class Node():
    def __init__(self,name,isEntry = False,isOutput = False):
        self.isEntry = isEntry
        self.isOutput = isOutput
        self.name = name
        self.alphabet = ["%c"%x for x in range(97,97+size_alphabet)]#creating an array containing all the letter in the alphabet of the automaton  "%c"%x is used to convert an integer (corresponding to an ASCII code here) to the corresponding character
        self.transitions = {}

    def __repr__(self):#magic method in python used to represent the object in a print(object) for example or just in the conversion to str : str(object)
        return "{}".format(self.name)

    def display(self):
        return "label : {}\n{}Transitions : {}\n\n".format(self.name,"Initial and Final\n" if self.isEntry and self.isOutput else "Initial\n" if self.isEntry else "Final\n" if self.isOutput else "",self.transitions if len(self.transitions) > 0 else "None")

    def __lt_(self, other):#rewriting the comparator methods for Nodes to be able to sort a list of Nodes, using the .sort() method
        return str(self).split('.') < str(other).split('.')#telling it to just compare the names (in the form of a list to be able to compare fused states)
        #doing it for all comparator < <= == >= >
    def __le__(self,other):
        return str(self).split('.') <= str(other).split('.')
    def __eq__(self,other):
        return str(self).split('.') == str(other).split('.')
    def __ge__(self,other):
        return str(self).split('.') >= str(other).split('.')
    def __gt__(self,other):
        return str(self).split('.') > str(other).split('.')

    def __add__(self,other):#another magic method used when you write a + b here used to combine to states in the automaton
        if self.name == '':#if the name is empty it mean that it's a placholder, meaning that we do not have anything to combine
            return other
        elif other.name == '':
            return self
        #getting the name of the combined state and creating the corresponding Node
        result = Node("{}.{}".format(self.name,other.name), isOutput = True if self.isOutput or other.isOutput else False)
        for letter in self.alphabet:#then fusing all the transitions by going through all the letter in the alphabet of the automaton
            selfT = ''
            otherT = ''
            if letter in self.transitions.keys():
                selfT = self.transitions[letter]#finding the transition corresponding to the letter in the first state
            if letter in other.transitions.keys():#finding the transition in the second state
                otherT = other.transitions[letter]
            if otherT == '':#if we do not find one it means that there is no transition with that letter
                if selfT != '':#mean that only selfT has a transition for that letter
                    result.transitions[letter] = selfT#thus for this letter only the first state has transition so no fusing necessary
            elif selfT == '':#same than above but the other way around
                if otherT != '':
                    result.transitions[letter] = otherT
            elif not(otherT) == '' and not(selfT) == '':#mean that both contain a transition
                temp = selfT[1] + otherT[1]#thus we fuse the transitions calling another __add__ method
                temp.sort()#
                result.transitions[letter] = [temp]
        return result

    def combine(self):
        new = []
        for letter in self.alphabet:
            temp = [t[1] for t in self.transitions if t[0]==letter]
            if len(temp)>0:
                temp.sort()
                newT = [temp]
                newT.insert(0,letter)
                new.append(newT)
        self.transitions = new

class Automaton():
    def __init__(self,states = [],isNotDet = None):
        self.states = states
        #self.combine()
        self.isNotDet = isNotDet
        self.alphabet = ["%c"%x for x in range(97,97+size_alphabet)]
        #self.table()

    def __repr__(self):
        output = "Alphabet : {}\n\n".format(self.alphabet)
        output2 = "".join(state.display() for state in self.states)
        return output + output2

    def table(self,input = []):
        if input == []:#mean that it's not for the deterministic or complete automaton
            input = self.states
        table = PrettyTable()
        fields = [letter for letter in self.alphabet]
        fields.insert(0,"States")
        table.field_names = fields
        for state in input:
            row = []
            for letter in self.alphabet:
                if letter in state.transitions.keys():
                    state.transitions[letter].sort()
                    text = [t.name for t in state.transitions[letter]]
                else:
                    text = ''
                row.append(" , ".join(text))
            row.insert(0,"{}{}".format("<->" if state.isOutput and state.isEntry else " <-" if state.isOutput else " ->" if state.isEntry else "   ",state.name))
            table.add_row(row)
        return table

    def isDeterministic(self,table = ''):
        if table == '':
            table = self.states
        for state in table:
            for letter in state.transitions.keys():
                if len(state.transitions[letter] > 1):
                    return False
        return True

    def determinize(self,det_table = 'None'):
        if det_table == 'None':#first part of the alorithm
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
        added = False
        for state in det_table:
            for transition in state.transitions:
                if len(transition[1]) > 1:#mean that we have a composite state to create
                    temp = [str(t) for t in transition[1]]
                    name = ".".join(temp)
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
                                det_table.append(s)
                                added = True
        if added:
            det_table = self.determinize(det_table)
        return det_table

    def isComplete(self,table = ''):
        if table == '':
            table = self.det_table
        for state in table:
            for letter in self.alphabet:
                found = False
                for transition in state.transitions:
                    if letter == transition[0]:
                        found = True
                if not found:
                    return False
        return True

    def complete(self):
        complete = deepcopy(self.det_table)
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
        complete.append(sink)
        self.complete = complete

    def combine(self):
        for state in self.states:
            state.combine()

    def recognize(self,word):
        entry = [entry for entry in self.complete if entry.isEntry]
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
        else:
            return False

    def complementary(self,table):
        if table == 'CDFA':
            table = self.complete
        elif table == 'MDCFA':
            table = self.min_table

        complement = deepcopy(table)
        for state in complement:
            if state.isOutput:
                state.isOutput = False
            else:
                state.isOutput = True
        self.complement = complement

    def minimize(self, previous = []):
        if previous == []:
            previous = self.complete

        Omega = []
        for state in previous:
            list = []
            for letter in self.alphabet:
                for transition in state.transitions:
                    if transition[1][0].isOutput:
                        list.append("T")
                    else:
                        list.append("NT")
            set = "".join(list)






def load(path):
    global size_alphabet
    with open(path,'r') as file:
        isNotDet = None
        size_alphabet = int(file.readline().rstrip('\n'))#the rstrip removes the new line character at the end of the line that could cause issues
        n_state = int(file.readline())
        states = []
        for i in range(n_state):#initialize the list to put the states in order corresponding to their label
            states.append(Node(str(i)))
        initial = file.readline().rstrip('\n').split(':')
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
            if t[1] in states[int(t[0])].transitions.keys():
                states[int(t[0])].transitions[t[1]].append(states[int(t[2])])
            else:
                states[int(t[0])].transitions[t[1]] = [states[int(t[2])]]
    return Automaton(states,isNotDet)

auto = load("automaton.txt")
print("Finite Automaton table : ")
print(auto.table())
auto.det_table = auto.determinize()
print("Deterministic Automaton Finite table :")
print(auto.table(auto.det_table))
auto.complete()
print("Deterministic Complete Finite Automaton table :")
print(auto.table(auto.complete))
print("Complement Deterministic Complete Finite Automaton table :")
auto.complementary('CDFA')
print(auto.table(auto.complement))
a = True
exit = 'Quit'
while a:
    word = input(f"Please give the word you want to check (type {exit} to exit) : ")
    if word != exit:
        print(auto.recognize(word))
    else:
        a = False
