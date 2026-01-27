from maze import Maze

class MazeGame:
    def __init__(self):
        raw = [
            "##########",
            "#S...#...#",
            "#.##.#.#.#",
            "#....#.#.#",
            "####.#.#.#",
            "#....#...#",
            "#.######.#",
            "#......G.#",
            "##########",
        ]
        self.maze = Maze(raw)
        self.player_r, self.player_c = self.maze.start
        self.goal_r, self.goal_c = self.maze.goal

        #สถิติ Stat
        self.steps = 0
        self.wall_hits = 0
        self.invalid_cmd = 0

    def reset(self):
        self.player_r, self.player_c = self.maze.start

    def is_win(self):
        return (self.player_r, self.player_c) == (self.goal_r, self.goal_c)
    

    def input_to_delta(self, cmd):

        if cmd == "W":
            return (-1, 0)
        elif cmd == "S":
            return(1, 0)
        elif cmd == "A":
            return(0, -1)
        elif cmd == "D":
            return(0, 1)
        return None
    
    def show_help(self):
        print("Controls")
        print("W = up, S = down, A = left, D = right")
        print("R = reset to start")
        print("H = help")
        print("Q = Quit game \n")
    
    def show_stats(self):
        print("===== Stats ======")
        print(f"Steps (successful move) : {self.steps}")
        print(f"Wall hits / blocked moves : {self.wall_hits}")
        print(f"Invalid commends : {self.invalid_cmd}")
        print()
    
    def run(self):
        print("=== Maze Game ===")
        self.show_help()

        while True:
            print(self.maze.render((self.player_r, self.player_c)))
            print()

            if self.is_win():
                print(" You is Winner\n")
                self.show_stats()
                break

            cmd = input("command (W/A/S/D H, R, Q)").strip().upper()

            if cmd == "Q":
                print("Exit game. \n")
                self.show_stats()
                break
            if cmd == "R":
                self.reset()
                print("Reset to start. \n")
            
            delta = self.input_to_delta(cmd)
            if delta is None:
                self.invalid_cmd += 1
                print("Invalid command \n")
                continue

            dr, dc = delta
            nr = self.player_r + dr
            nc = self.player_c + dc

            ok, msg = self.maze.can_move_to(nr, nc)
            if not ok:
                self.wall_hits += 1
                print(msg + "\n")
                continue

            #Walk
            self.player_r, self.player_c = nr, nc
            self.steps += 1



