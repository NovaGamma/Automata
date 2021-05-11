array = [i for i in range(20)]

for i,v in enumerate(array):
    if v == 2:
        array[i] = 'test'
print(array)
