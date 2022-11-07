class Test():
    def __init__(self,x,y,z):
        self.x=x
        self.y=1
        self.z=1


#w=Test(1)
#print(w.x)

# print(w.y)
# print(w.z)


a = [1,2,3,4]
b = [5,6,7,8]
c=[a,b]
print(c)
print(c[0])
w=list(map(lambda x: x+1, a))
print(w)