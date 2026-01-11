import random


class SudokuBoard:
    def __init__(self):
        self.graph = {}
        self.values = {}
        self.givens = set()
        self._create_graph()

    def _create_graph(self):
        for row in range(9):
            for col in range(9):
                node = (row, col)
                self.graph[node] = self._get_neighbors(row, col)
                self.values[node] = 0

    def _get_neighbors(self, row, col):
        neighbors = set()
        for c in range(9):
            if c != col:
                neighbors.add((row, c))

        for r in range(9):
            if r != row:
                neighbors.add((r, col))

        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        for r in range(subgrid_row_start, subgrid_row_start + 3):
            for c in range(subgrid_col_start, subgrid_col_start + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def reset(self):
        for node in self.values:
            self.values[node] = 0
        self.givens.clear()

    def get_value(self, row, col):
        return self.values.get((row, col), 0)

    def set_value(self, row, col, value):
        self.values[(row, col)] = value

    def is_given(self, row, col):
        return (row, col) in self.givens

    def is_valid(self, row, col, num):
        node = (row, col)
        for neighbor in self.graph[node]:
            if self.get_value(*neighbor) == num:
                return False
        return True

    def make_move(self, row, col, value):
        if self.is_given(row, col):
            return False
        if self.is_valid(row, col, value):
            self.set_value(row, col, value)
            return True
        return False

    def clear_value(self, row, col):
        if self.is_given(row, col):
            return False
        self.set_value(row, col, 0)
        return True

    def solve(self):
        empty = self._find_empty()
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.set_value(row, col, num)
                if self.solve():
                    return True
                self.set_value(row, col, 0)

        return False

    def _fill_board(self):
        empty = self._find_empty()
        if not empty:
            return True

        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.set_value(row, col, num)
                if self._fill_board():
                    return True
                self.set_value(row, col, 0)

        return False

    def _find_empty(self):
        for node, value in self.values.items():
            if value == 0:
                return node
        return None

    def generate(self, difficulty):
        self.reset()
        if not self._fill_board():
            return False

        cells_to_remove = self._cells_to_remove(difficulty)
        all_cells = list(self.values.keys())
        random.shuffle(all_cells)

        removed = 0
        for row, col in all_cells:
            if removed >= cells_to_remove:
                break
            if self.get_value(row, col) != 0:
                self.set_value(row, col, 0)
                removed += 1

        self.givens = {node for node, value in self.values.items() if value != 0}
        return True

    def _cells_to_remove(self, difficulty):
        if difficulty == "easy":
            return 20
        if difficulty == "medium":
            return 35
        if difficulty == "hard":
            return 50
        return 0

    def check_win(self):
        for node, value in self.values.items():
            if value == 0:
                return False
            row, col = node
            if not self.is_valid(row, col, value):
                return False
        return True
