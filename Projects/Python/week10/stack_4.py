stack = []
pairs = {')':'(',']':'[','}':'{'}

opens = set(pairs.values())
valid = True


def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0


def apply_op(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a // b


expr = input("Enter expression: ")

nums = []
ops = []
valid = True
i = 0

while i < len(expr):

    # ตัวเลข
    if expr[i].isdigit():
        num = 0
        while i < len(expr) and expr[i].isdigit():
            num = num * 10 + int(expr[i])
            i += 1
        nums.append(num)
        print("push number:", num, "nums =", nums)
        continue

    # วงเล็บเปิด
    elif expr[i] == '(':
        ops.append(expr[i])
        print("push (  ops =", ops)

    # วงเล็บปิด
    elif expr[i] == ')':
        while ops and ops[-1] != '(':
            if len(nums) < 2:
                valid = False
                break
            b = nums.pop()
            a = nums.pop()
            op = ops.pop()
            result = apply_op(a, b, op)
            nums.append(result)
            print("calculate:", a, op, b, "=", result)

        if not ops:
            valid = False
            break

        ops.pop()  # เอา '(' ออก
        print("pop (  ops =", ops)

    # operator
    elif expr[i] in '+-*/':
        while (ops and ops[-1] != '(' and
               precedence(ops[-1]) >= precedence(expr[i])):
            b = nums.pop()
            a = nums.pop()
            op = ops.pop()
            result = apply_op(a, b, op)
            nums.append(result)
            print("calculate:", a, op, b, "=", result)

        ops.append(expr[i])
        print("push operator:", expr[i], "ops =", ops)

    i += 1


# คำนวณที่เหลือ
while valid and ops:
    if len(nums) < 2:
        valid = False
        break
    b = nums.pop()
    a = nums.pop()
    op = ops.pop()
    result = apply_op(a, b, op)
    nums.append(result)
    print("calculate:", a, op, b, "=", result)


if valid and len(nums) == 1:
    print("Result =", nums[0])
else:
    print("Invalid expression")

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
  