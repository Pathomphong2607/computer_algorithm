class Maze:
    def __init__(self, raw_rows):
        self.grid = [list(row) for row in raw_rows]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0] if self.rows > 0 else 0)

        self.start = self.find_pos("S")
        self.goal = self.find_pos("G")

        if self.start is None or self.goal is None:
            raise ValueError("Maze must contain 'S' OR 'G'")
    
    def find_pos(self, ch):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == ch:
                    return (r,c)
        return None

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    
    def cell(self, r, c):
        return self.grid[r][c]

    def is_wall(self, r, c):
        return self.cell(r,c) == "#"
    
    def can_move_to(self, r, c):
        if not self.in_bounds(r,c):
            return False, "Out of bounds!"
        if self.is_wall(r, c):
            return False, "Hit a wall"
        return "True", ""
    
    def render(self, player_pos):
        pr, pc = player_pos
        lines = []
        for r in range(self.rows):
            row_chars = []
            for c in range(self.cols):
                if r == pr and c == pc:
                    row_chars.append("P")
                else:
                    row_chars.append(self.grid[r][c])
            lines.append("".join(row_chars))
        return "\n".join(lines)
