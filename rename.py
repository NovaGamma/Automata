import os
path = "automaton/"
for file in os.listdir("automaton/"):
    number = file.lstrip('Int1-8-Int1-8-').rstrip('.txt')
    new_name = f"automaton/Int1-8-{number}.txt"
    #os.rename("automaton/"+file,new_name)
