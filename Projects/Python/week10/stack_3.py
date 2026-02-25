stack = []
pairs = {')':'(',']':'[','}':'{'}


opens = set(pairs.values())
expr = input("Enter expression with brackets:")
valid = True

for ch in expr:
    if ch in opens:
        stack.append(ch)
        print("push :",ch,"stack =",stack)
        
    elif ch in pairs:
        if not stack:
            print("Error : stack empty but found clossing brackets ",ch)
            valid = False 
            break
        
        top = stack.pop()
        print("pop :",top,"for clossing",ch,"stack = ",stack)
    
        if top != pairs[ch]:
            print("Error: bracket not match ->",top,"vs",ch)
            valid = False
            break
    
if valid:
    if stack:
        print("Error : still ",stack)
        valid = False
        
if valid:
    print("result : Valid")
else:
    print("result : Invalid")
  