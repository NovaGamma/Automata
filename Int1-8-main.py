import os
from Int1_8_Class import*

#choosing the automaton to load

path = "automaton/"
files = []
for i in range(46):
    file_name = f"Int1-8-{i}.txt"
    if os.path.exists(path+file_name):
        files.append(file_name)

print("{} automatons were found".format(len(files)))

leaving = 0

while leaving == 0 :
    print("Type 0 to leave. You can choose an automaton from the list : ")
    for i,file in enumerate(files):
        print(f"{i+1} : {file}")

    choice = int(input())

    while not -1 < choice < len(files)+1:
        print("You cannot choose this")
        choice = int(input())
    if(not choice):
        quit()

    else:
        path = 'automaton/' + files[choice-1]

        #path = "automaton.txt"
        auto = load(path)

        print(auto)
        print(auto.table())

        ope = 0
        previous = ''
        while (ope != 8):
            ope = int(input("Which operation do you want to do? Type :\n 1 to determinize,\n 2 to complete,\n 3 to minimize,\n 4 to standardize,\n 5 to check if a given word is recognized,\n 6 to make the automaton synchronous,\n 7 to complementarize it,\n 8 to change automaton,\n 9 to leave the program. "))
            while not 0 < ope < 10:
                print("You cannot choose this")
                ope = int(input())

            print("\n")

            if (ope == 1):   #determinize
                if isAsync(auto.states):
                    table = auto.synchronize()
                else:
                    table = auto.states
                if(not auto.isDeterministic(table)):
                    auto.det_table = auto.determinize(table)
                    print("Deterministic Finite Automaton table :")
                    print(auto.table(auto.det_table))
                    previous = auto.det_table
                else:
                    print("Automaton already deterministic. ")


            elif(ope == 2): #complete
                if isAsync(auto.states):
                    table = auto.synchronize()
                else:
                    table = auto.states
                if(not auto.isDeterministic(table)): #cant complete a non deterministic FA
                    auto.det_table = auto.determinize(table)
                if(auto.isDeterministic(table) and auto.isComplete(table)): #need both cause a non deterministic FA could have the properties of a complete FA
                    print("Automaton already complete.\n")

                else:
                    complete = auto.complete(table)
                    print("Complete Deterministic Finite Automaton table :")
                    print(auto.table(complete))
                    previous = complete

            elif(ope == 3): #minimize
                if isAsync(auto.states):
                    table = auto.synchronize()
                else:
                    table = auto.states
                if(not auto.isDeterministic(table)): #FA needs to be complete and therefore deterministic to minimize it
                    auto.det_table = auto.determinize(table)
                    table = auto.complete()
                elif(not auto.isComplete(table)):
                    table = auto.complete(table)

                minimized = auto.minimize(table)
                print("Minimized Finite Automaton table :")
                print(auto.table(minimized))
                previous = minimized


            elif (ope == 4): #standardize
                if previous == '':
                    table = auto.states
                else:
                    table = previous
                if isAsync(table):
                    table = auto.synchronize()
                if(auto.isStandard(table)):
                    print("Automaton already standard.")
                else:
                    standardized = auto.standardize()
                    print("Standard Finite Automaton table :")
                    print(auto.table(standardized))

            elif(ope == 5): #word to enter
                if(not auto.isDeterministic()): #FA needs to be deterministic to search word
                    table = auto.determinize()
                    print("determinized")
                else:
                    table = auto.states
                a = True
                exit = 'Quit'
                while a:
                    word = input("Please give the word you want to check (type Quit to come back) : ")
                    if word != exit:
                        print(auto.recognize(word,table))
                    else:
                        a = False

            elif(ope == 6): #synchronous
                if (isAsync(auto.states)):
                    auto.sync = auto.synchronize()
                    print("Synchronous Automaton table :")
                    print(auto.table(auto.sync))
                else:
                    print("Automaton already synchronous")

            elif(ope == 7): #complementarize
                if isAsync(auto.states):
                    table = auto.synchronize()
                else:
                    table = auto.states
                if(not auto.isDeterministic(table)): #cant get complementary if not complete and deterministic
                    auto.det_table = auto.determinize(table)
                    table = auto.complete()
                elif(not auto.isComplete(table)):
                    table = auto.complete(table)
                else:
                    table = auto.states

                print("Complement of Complete Deterministic Finite Automaton table :")
                complement = auto.complementary(table)
                print(auto.table(complement))
                previous = complement


            elif(ope == 9): #leave program
                quit()

            print("\n")
