from game import MazeGame

def main_menu():
    while True:
        print("=== Main Menu===")
        print("A = Enter Program (Maze Game)")
        print("Q = Exit")
        choice = input("Selct : ").strip().upper()

        if choice =="A":
            game = MazeGame()
            game.run()
        elif choice == "Q":
            print("Goodbye")
            break
        else:
            print("Invalid choice \n")


if __name__ == "__main__":
    main_menu()
