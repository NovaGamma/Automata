class Example:
    def __init__(self,value):
        self.value = value

    def __repr__(self):
        #return the string to be used when doing a str() conversion or a print
        return str(self.value)

    def __add__(self,other):
        #function called when doing a + b with both elements being of class Example
        #we return a new element of class Example having as value the sum of both
        return Example(self.value + other.value)
        #it could also add value of the left one to the right one directly without returning a new element
        #self.value = self.value + other.value

example = Example(2)
second_example = Example(3)
print(example)                              #will call the __repr__ function of the class object
new_example = example + second_example      #will result in new_example having a value set to 5
print(new_example)

#---------------------------------------
#List Comprehensions
#int the form of [var for var in other_list if condition]
#will return a list filled with all elements of other_list that fullfill the condition
array = [i for i in range(20) if i%2==0]    #here being a list of all element from 0 to 19 that are mod2
print(array)                                #[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

#----------------------------------------
#Ternary operators
#Ternary operators are used to do a series of if-else statements in one line
n = 6
variable = 1 if n%4==0 else 2 if n%2==0 else 3
