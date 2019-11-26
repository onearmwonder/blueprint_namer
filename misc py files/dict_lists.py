test_list = [{'id': 2, 'name': 'don'},
            {'id': 1, 'name': 'won'},
            {'id': 4, 'name': 'why'},
            {'id': 3, 'name': 'god'}]

test_dict = {'name': 'don', 'age': 45, 'weight': 222, 'height': 7}

keys = test_dict.keys()
print(keys)
for i in keys:
    print(i)

'''
for y in range(len(test_list)):
    x = (item for item in test_list if item['id'] == y+1)
    print(x)
    print(list(x))
'''