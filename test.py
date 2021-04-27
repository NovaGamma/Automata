test = {}
test['a'] = [1,2]
test['b'] = [0,1]
test2 = {}
test2['a'] = [1,2]
test2['b'] = [0,1]
for i,v in zip(test,test2):
    print(i,v)
