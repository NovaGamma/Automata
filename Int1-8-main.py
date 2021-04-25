import os
from Class import*

#choosing the automaton to load

path = "automaton/"
files = []
for i in range(46):
    file_name = f"Int1-8-{i}.txt"
    if os.path.exists(path+file_name):
        files.append(file_name)

print("{} automatons were found".format(len(files)))
print("You can choose an automaton from the list : ")
for i,file in enumerate(files):
    print(f"{i+1} : {file}")

choice = int(input())
while not 0 <= choice < len(files):
    print("You cannot choose this")
    choice = int(input())
path = 'automaton/' + files[choice]

#path = "automaton.txt"
auto = load(path)
print(auto)

print("Finite Automaton table : ")
print(auto.table())

if auto.standardize():
    print("Standard Finite Automaton table :")
    print(auto.table(auto.standard))
else:
    print("The automaton is already standard")
auto.det_table = auto.determinize()
print("Deterministic Finite Automaton table :")
print(auto.table(auto.det_table))
auto.complete()
print("Complete Deterministic Finite Automaton table :")
print(auto.table(auto.complete))
print("Complement of Complete Deterministic Finite Automaton table :")
auto.complementary('CDFA')
print(auto.table(auto.complement))
auto.minimize()
'''
a = True
exit = 'Quit'
while a:
    word = input(f"Please give the word you want to check (type {exit} to exit) : ")
    if word != exit:
        print(auto.recognize(word))
    else:
        a = False
'''
