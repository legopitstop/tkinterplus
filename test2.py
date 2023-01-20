
def test():
    items = [0,1,2,3,4,5]
    for i in items:
        yield i


res = test()
print(list(res))

for i in res:
    print(i)