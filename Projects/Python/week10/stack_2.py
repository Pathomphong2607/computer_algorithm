stack = []
popped = []
N = 3

for i in range(N):
    inp = input("Stack push :")
    stack.append(inp)
    
print("Stack now :",stack)

for i in range(N):
    x = stack.pop()
    popped.append(x)
    print("popped :",x)
    
print("popped now :",popped)

    