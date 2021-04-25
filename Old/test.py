import os
import random

size = 50

print("Start Loading :\n["+"."*size+"]")
input()
for i in range(1,size+1):
    os.system('cls')
    output = '[' + '|'*i + '.'*(size-i) + ']'
    print("Loading...{}%\n".format(int(i/size*100)) + output)
os.system('cls')
print("Done !\n"+output)
input()
