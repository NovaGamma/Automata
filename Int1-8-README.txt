This is the project of the group Int1-8:
-Elvin AUPIAIS--BERTHY
-Thomas CASASNOVAS
-Guillaume GOMEZ
-Anne HIRIART

The objective of the project was to be able to automate all the tasks we were asked to perform during the courses.
We therefore had to be able to read a given Finite Automaton (FA), represent it in a table,
determine and complete it after testing if it already was, minimize it, find out whether or not it recognizes a given world,
find its complementary language and finally standardize it. In order to do this, we decided to use Python,
which is one of the most efficient.


Elvin was the main contributor to the project, but not all the function were written by him,
but he rewrote and optimized them, hence the code that seems written by only one person.

-Elvin did the synchronization and the magic method __add__ to combine two states into a new one
-Thomas wrote the algorithm for the minimize function and the complement
-Guillaume wrote the basis of the classes, did all the translation for the test automata, the standardize function
and the recognition of a word
-Anne did all the menu with the check functions that come with it, the load function, the determinization and completion of an automaton

Elvin's Note

I just wanted to clarify some things about the Int2-6 group, you may find the code of our project similar, I agree with that for some parts
Here are some explanation about why:

I helped this group to learn some python techniques and tricks (hence some parts of our code may seem similar)
mainly technics such as ternary operators and list comprehension (that are described in the Examples file)
I also helped them a bit on the data structure, which is a bit similar, but not entirely the same, but as the data structure is similar, the algorithm to implement standarization, to load the automaton from a file, to display the automaton are similar
But those functions such as the standardization or determinization were entirely written by them
Even if they asked me to helped them resolve some problems as one would seek help on the internet.

Moreover as it's explained in their code and in multiple places in ours, the way they display the transition table is using a library that I rewrote
Earlier I sent you an email asking if it was ok to used an external library to display the table and you agreed
But for the sake of it to be easier to use for you I rewrote the library myself (The file Int1_8_Table.py)
and they are also using it. It's the same as if they were using an external library.
This code is not commented because I do not consider it to be part of the project
