import os
try:
    from prettytable import PrettyTable
except ModuleNotFoundError:
    os.system('cmd /c "pip install PTable"')
    _ = os.system('cls')
    from prettytable import PrettyTable
from numpy import copy

class Node():
    def __init__(self,name,x = 0,y = 0,isEntry = False,isOutput = False):
        self.transitions = []
        self.isEntry = isEntry
        self.isOutput = isOutput
        self.name = name

    def __repr__(self):
        return "Node {}".format(self.name)

class Automaton():
    def __init__(self,states = [],size_alphabet = 1):
        self.states = states
        self.alphabet = ["%c"%x for x in range(97,98+size_alphabet)]
        self.table()

    def __repr__(self):
        output = "Alphabet : {}\n\n".format(self.alphabet)
        for state in auto.states:
            output += "label : {}\n{}Transitions : {}\n\n".format(state.name,"Initial\n" if state.isEntry else "Final\n" if state.isOutput else "",state.transitions if len(state.transitions) > 0 else "None")
        return output

    def table(self):
        table = PrettyTable()
        fields = [letter for letter in self.alphabet]
        fields.insert(0,"States")
        real_table = {}
        table.field_names = fields
        for state in self.states:
            row = [' ' for i in range(len(self.alphabet))]
            #state.transitions.sort()
            for x in state.transitions:
                print(x)
                index = self.alphabet.index(x[0])
                if row[index] == ' ':
                    row[index] = str(x[1])
                else:
                    row[index] += ' , ' + str(x[1])
            real_table[state.name] = row.copy()
            row.insert(0,"{}{}".format("<->" if state.isOutput and state.isEntry else " <-" if state.isOutput else " ->" if state.isEntry else "   ",state.name))
            table.add_row(row)
        self.table = table#talbe correspond to the formatted table to be displayed
        self.real_table = real_table#real table correspond to the table that we can access to determinize or standardize the automaton
        print(real_table)

    def determinize(self):
        for key in self.real_table:#here we go through all the states
            i = self.real_table[key]#i is the list of transition
            for j in i:#j is a transition of the row i
                if len(j.split(' , '))>1:#mean that we need a composite state
                    states = j.split(' , ')
                    row = [' ' for i in range(len(self.alphabet))]
                    print(states)
                    for k in states:
                        transitions = self.real_table[int(k)]#here are the transition of a component of the new state
                        for l in range(len(self.alphabet)):
                            row[l] += transitions[l]
                    print(row)
                    new_state = (''.join(states))

def load(path):
    with open(path,'r') as file:
        size_alphabet = file.readline().rstrip('\n')#the rstrip removes the new line character at the end of the line that could cause issues
        n_state = int(file.readline())
        states = []
        for i in range(n_state):#initialize the list to put the states in order corresponding to their label
            states.append(Node(i))
        initial = file.readline().rstrip('\n').split(':')
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
    return Automaton(states)

auto = load("automaton.txt")
print(auto.table)
print(auto)
auto.determinize()
