def MainMenu():
    print("" \
    "Press Enter Q = Exit\n " \
    "C = calculate")
    inp = input (" : ")
    if(inp == "Q" or inp == "q"):
        exit()
    if(inp == "C" or inp == "c"):
        Calculate()
    else:
        MainMenu()

def Calculate():
    print("+ = Plus\n" \
    "- = Minus\n"\
    "* = Multiply\n"\
    "/ = Divide\n"\
    "M = Main/Home")
    
    inp = input(": ")
    
    if inp == "+":
        N = int(input("N : "))
        total = 0
        for i in range(N):
            total += int(input("Number : "))
        print("Total =", total)
        Calculate()

    elif inp == "-":
        N = int(input("N : "))
        total = int(input("Number : "))
        for i in range(N - 1):
            total -= int(input("Number : "))
        print("Total =", total)
        Calculate()

    elif inp == "*":
        N = int(input("N : "))
        total = 1
        for i in range(N):
            total **= int(input("Number : "))
        print("Total =", total)
        Calculate()

    elif inp == "/":
        N = int(input("N : "))
        total = float(input("Number : "))
        for i in range(N - 1):
            num = int(input("Number : "))
            if num == 0:
                print("Error: divide by zero")
                Calculate()
                return 
            total /= num
        print("Total =", total)
        Calculate()

    elif inp == "M" or inp == "m":
        MainMenu()

    else:
        Calculate()


MainMenu()