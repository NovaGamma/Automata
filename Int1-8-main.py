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
        while (ope != 8):
            ope = int(input("Which operation do you want to do? Type :\n 1 to determinize,\n 2 to complete,\n 3 to minimize,\n 4 to standardize,\n 5 to check if a given word is recognized,\n 6 to make the automaton synchronous,\n 7 to complementarize it,\n 8 to change automaton,\n 9 to leave the program. "))
            while not 0 < ope < 10:
                print("You cannot choose this")
                ope = int(input())
            
            print("\n")
        
            if (ope == 1):   #determinize
                if(not auto.isDeterministic()):
                    auto.det_table = auto.determinize()
                    print("Deterministic Finite Automaton table :")
                    print(auto.table(auto.det_table))
                else:
                    print("Automaton already deterministic. ")
                
                
            elif(ope == 2): #complete
                if(not auto.isDeterministic()): #cant complete a non deterministic FA
                    auto.det_table = auto.determinize()
                if(auto.isDeterministic() and auto.isComplete()): #need both cause a non deterministic FA could have the properties of a complete FA
                    print("Automaton already complete.\n")
                    
                else:
                    auto.complete()
                    print("Complete Deterministic Finite Automaton table :")
                    print(auto.table(auto.complete))
                    
                    
            elif(ope == 3): #minimize
                if(not auto.isDeterministic()): #FA needs to be complete and therefore deterministic to minimize it
                    auto.det_table = auto.determinize()
                    auto.complete()
                elif(not auto.isComplete()):
                    auto.complete()

                minimized = auto.minimize(auto.complete)
                print("Minimized Finite Automaton table :")
                print(auto.table(minimized))
                
                
            elif (ope == 4): #standardize
                if(auto.isStandard()):
                    print("Automaton already standard.")
                else:
                    standardized = auto.standardize()
                    print("Standard Finite Automaton table :")
                    print(auto.table(standardized))

            elif(ope == 5): #word to enter
                #if(not auto.isDeterministic()): #FA needs to be deterministic to search word
                 #   auto.det_table = auto.determinize()
                  #  print("determinized")
                auto.det_table = auto.determinize() #to remove?
                a = True
                exit = 'Quit'
                while a:
                    word = input("Please give the word you want to check (type Quit to come back) : ")
                    if word != exit:
                        print(auto.recognize(word,auto.det_table))
                    else:
                        a = False

            #error
            elif(ope == 6): #synchronous
                if (auto.isAsync()):
                    auto.sync = auto.synchronize()
                    print("Standard Synchronous Automaton table :")
                    print(auto.table(auto.sync))
                else:
                    print("Automaton already synchronous")
                    
            elif(ope == 7): #complementarize
               # if(not auto.isDeterministic()): #cant get complementary if not complete and deterministic 
                #    auto.det_table = auto.determinize()
                 #   auto.complete()
                  #  print("completed0")
                #elif(not auto.isComplete()):
                 #   auto.complete()
                  #  print("completed")
                auto.det_table = auto.determinize()
                auto.complete()
                
                print("Complement of Complete Deterministic Finite Automaton table :")
                complement = auto.complementary(auto.complete)
                print(auto.table(complement))
                
                
            elif(ope == 9): #leave program
                quit()
        
            print("\n")

    
        


'''
print("Finite Automaton table : ")

if auto.standardize():
    print("Standard Finite Automaton table :")
    print(auto.table(auto.standard))
else:
    print("The automaton is already standard")
print("Complement of Complete Deterministic Finite Automaton table :")
auto.complementary('CDFA')
print(auto.table(auto.complement))
auto.sync = auto.synchronize()
print(auto.table(auto.sync))

a = True
exit = 'Quit'
while a:
    word = input(f"Please give the word you want to check (type {exit} to exit) : ")
    if word != exit:
        print(auto.recognize(word))
    else:
        a = False
'''
