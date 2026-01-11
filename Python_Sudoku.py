import pygame
import sys
import random

class SudokuGraph:
    def __init__(self):
        self.graph = {}
        self.values = {}
        self.create_graph()

    def create_graph(self):
        for row in range(9):
            for col in range(9):
                node = (row, col)
                self.graph[node] = self.get_neighbors(row, col)
                self.values[node] = 0

    def get_neighbors(self, row, col):
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

    def get_value(self, row, col):
        return self.values.get((row, col), 0)

    def set_value(self, row, col, value):
        self.values[(row, col)] = value

    def make_move(self, row, col, value):
        if self.is_valid(row, col, value):
            self.set_value(row, col, value)
            return True
        return False

    def remove_move(self, row, col):
        self.set_value(row, col, 0)

    def is_valid(self, row, col, num):
        node = (row, col)
        for neighbor in self.graph[node]:
            if self.get_value(*neighbor) == num:
                return False
        return True

    def solve_sudoku(self):
        empty_cells = [node for node, value in self.values.items() if value == 0]
        
        if not empty_cells:
            return True

        row, col = empty_cells[0]
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.set_value(row, col, num)
                if self.solve_sudoku():
                    return True
                self.remove_move(row, col)

        return False

    def remove_numbers(self, difficulty):
        if difficulty == "easy":
            cells_to_remove = 20
        elif difficulty == "medium":
            cells_to_remove = 35
        elif difficulty == "hard":
            cells_to_remove = 50
        else:
            cells_to_remove = 0

        all_cells = list(self.values.keys())
        random.shuffle(all_cells)

        removed = 0
        for row, col in all_cells:
            if removed >= cells_to_remove:
                break
            if self.get_value(row, col) != 0:
                self.remove_move(row, col)
                removed += 1

    def check_win_condition(self):
        for node, value in self.values.items():
            if value == 0:
                return False 
            row, col = node
            if not self.is_valid(row, col, value):
                return False
        print("Congratulations! You've completed the Sudoku!")
        return True

pygame.init()
pygame.font.init()

running = True

# window dimensions
screen_width, screen_height = 950, 750 # Main window 
width, height = 450, 450 # Used for sudoku grid
cell_size = width // 9 # Cell size
console_height = 500 
console_width = 240
total_window_height = screen_height

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Sudoku")

# Fonts for the game
counter_font = pygame.font.Font(None, 24) 
Cell_font = pygame.font.Font(None, 34)
console_font = pygame.font.Font(None, 28)
author_font = pygame.font.SysFont("arial", 28)

# Colors (RGB Format)
White = (255, 255, 255)
Black = (0, 0, 0)
background_color = (202, 244, 244) # https://www.schemecolor.com/relaxing-to-the-eye-color-palette.php
console_color = (180, 244, 255)

# Game Logic
sudoku_graph = SudokuGraph()
selected_cell = None 
move_count = 0
console_messages = []
win_condition = False

def render_grid():
    screen.fill(background_color)

    offset_x = (screen_width - width) // 2
    offset_y = (screen_height - height) // 2

    for i in range(10):
        
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, Black, (offset_x, offset_y + i * cell_size), (offset_x + width, offset_y + i * cell_size), thickness)
        pygame.draw.line(screen, Black, (offset_x + i * cell_size, offset_y), (offset_x + i * cell_size, offset_y + height), thickness)
    
    for row in range(9):
        for col in range(9):
            num = sudoku_graph.get_value(row, col)
            if num != 0:
                text = Cell_font.render(str(num), True, Black)
                x_pos = offset_x + col * cell_size
                y_pos = offset_y + row * cell_size
                text_rect = text.get_rect(center=(x_pos + cell_size // 2, y_pos + cell_size // 2))
                screen.blit(text, text_rect)

    if selected_cell:
        sel_row, sel_col = selected_cell
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(offset_x + sel_col * cell_size, offset_y + sel_row * cell_size, cell_size, cell_size, ), 3, )

def render_buttons():
    button_width = 120 
    button_height = 50
    spacing = 15
    margin_right = 20
    x_pos = screen_width - button_width - margin_right
    y_start = 150 

    easy_button = pygame.Rect(x_pos, y_start, button_width, button_height)
    medium_button = pygame.Rect(x_pos, y_start + button_height + spacing, button_width, button_height)
    hard_button = pygame.Rect(x_pos, y_start + 2 * (button_height + spacing), button_width, button_height)
    solver_button = pygame.Rect(x_pos, y_start + 3 * (button_height + spacing), button_width, button_height)
    instructions_button = pygame.Rect(x_pos, y_start + 4 * (button_height + spacing), button_width, button_height)

    pygame.draw.rect(screen, (200, 255, 200), easy_button)
    pygame.draw.rect(screen, (255, 255, 200), medium_button)
    pygame.draw.rect(screen, (255, 200, 200), hard_button)
    pygame.draw.rect(screen, (200, 200, 255), solver_button)
    pygame.draw.rect(screen, (220, 220, 220), instructions_button)

    easy_text = counter_font.render("Easy", True, Black)
    medium_text = counter_font.render("Medium", True, Black)
    hard_text = counter_font.render("Hard", True, Black)
    solver_text = counter_font.render("Solve!", True, Black)
    instructions_text = counter_font.render("Instructions", True, Black)

    screen.blit(easy_text, (easy_button.x + (button_width - easy_text.get_width()) // 2, easy_button.y + (button_height - easy_text.get_height()) // 2))
    screen.blit(medium_text, (medium_button.x + (button_width - medium_text.get_width()) // 2, medium_button.y + (button_height - medium_text.get_height()) // 2))
    screen.blit(hard_text, (hard_button.x + (button_width - hard_text.get_width()) // 2, hard_button.y + (button_height - hard_text.get_height()) // 2))
    screen.blit(solver_text, (solver_button.x + (button_width - solver_text.get_width()) // 2, solver_button.y + (button_height - solver_text.get_height()) // 2))
    screen.blit(instructions_text, (instructions_button.x + (button_width - instructions_text.get_width()) // 2, instructions_button.y + (button_height - instructions_text.get_height()) // 2))

    return easy_button, medium_button, hard_button, solver_button, instructions_button

def render_text():
    header_text = console_font.render("Activity Log", True, Black)
    screen.blit(header_text, (70, 105))
    author_text = author_font.render("Created by Nikola Shikole", True, Black)
    author_x = (screen_width - author_text.get_width()) // 2
    author_y = 50
    screen.blit(author_text, (author_x, author_y))

def render_move_counter():
    text_surface = counter_font.render(f"Moves: {move_count}", True, Black)
    screen.blit(text_surface, (10, 10))

def render_console():
    console_rect = pygame.Rect(5, (screen_height - console_height) // 2, console_width, console_height)
    pygame.draw.rect(screen, console_color, console_rect) 
    pygame.draw.rect(screen, Black, console_rect, 2)  

    for i, message in enumerate(reversed(console_messages[-24:])):
        text_surface = console_font.render(message, True, Black)
        screen.blit(text_surface, (10, 130 + i * 20))

def log_message(message):
    console_messages.append(message)
    if len(console_messages) > 100:
        console_messages.pop(0)
        
def get_cell_from_mouse(pos):
    offset_x = (screen_width - width) // 2
    offset_y = (screen_height - height) // 2
    x, y = pos
    col = (x - offset_x) // cell_size
    row = (y - offset_y) // cell_size
    if 0 <= row < 9 and 0 <= col < 9:
        return row, col
    return None

def generate_random_sudoku(difficulty, TSudokuGraph):
    def backtrack(sudoku_graph):
        for row in range(9):
            for col in range(9):
                if sudoku_graph.get_value(row, col) == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if sudoku_graph.is_valid(row, col, num):
                            sudoku_graph.set_value(row, col, num)
                            if backtrack(sudoku_graph):
                                return True
                            sudoku_graph.set_value(row, col, 0)
                    return False 

        return True
    backtrack(TSudokuGraph)

    if difficulty == "easy":
        cells_to_remove = 20
        log_message("Easy puzzle generated!")
        print("easy")
    elif difficulty == "medium":
        cells_to_remove = 35
        log_message("ted!")
        log_message("Medium puzzle genera-")
        print("medium")
    elif difficulty == "hard":
        cells_to_remove = 50
        log_message("Hard puzzle generated!")
        print("hard")
    all_cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(all_cells)

    removed = 0
    for row, col in all_cells:
        if removed >= cells_to_remove:
            break
        if TSudokuGraph.get_value(row, col) != 0:
            TSudokuGraph.set_value(row, col, 0)
            removed += 1

    return TSudokuGraph

def render_instructions():
    instruction_window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Instructions")
    instruction_window.fill(White)

    instructions = [
        "Welcome to Sudoku!",
        "1. Click on a cell to select it.",
        "2. Type a number 1 through 9 on your keyboard to place it in the cell.",
        "3. In order to delete a number from a cell, press backspace or the number 0",
        "on your keyboard.",
        "4. Use the Solver button to solve the board automatically.",
        "5. Use the Easy, Medium, or Hard buttons to start a new game.",
        "6. To win, fill the board correctly with numbers 1 through 9.",
    ]

    y_offset = 20
    for line in instructions:
        text_surface = console_font.render(line, True, Black)
        instruction_window.blit(text_surface, (20, y_offset))
        y_offset += 40

    pygame.display.flip()

    # Wait for the user to close the instructions window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.set_mode((screen_width, screen_height))
                pygame.display.set_caption("Sudoku Game")
                return

while running:
    for event in pygame.event.get():
        
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_cell = get_cell_from_mouse(event.pos)
                mouse_pos = event.pos
                if easy_button.collidepoint(mouse_pos):
                    console_messages.clear()
                    generate_random_sudoku("easy", sudoku_graph)
                    win_condition = False
                    move_count = 0
                if medium_button.collidepoint(mouse_pos):
                    console_messages.clear()
                    generate_random_sudoku("medium", sudoku_graph)
                    win_condition = False
                    move_count = 0
                if hard_button.collidepoint(mouse_pos):
                    console_messages.clear()
                    generate_random_sudoku("hard", sudoku_graph)
                    win_condition = False
                    move_count = 0
                if solver_button.collidepoint(mouse_pos):
                    if sudoku_graph.solve_sudoku():
                        print("Sudoku solved using solver!")
                        log_message("solver!")
                        log_message("Sudoku solved using")
                    else:
                        print("No solution found.")
                        log_message("No solution found.")
                if instructions_button.collidepoint(mouse_pos):
                    render_instructions()

        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            if selected_cell and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                row, col = selected_cell
                value = event.key - pygame.K_0
                if sudoku_graph.make_move(row, col, value):
                    move_count += 1
                    print("Move successful!")
                    log_message("Move successful!")
                else:
                    print("Invalid move!")
                    log_message("Invalid move!")
            if selected_cell and event.key in [pygame.K_BACKSPACE, pygame.K_0]:
                row, col = selected_cell
                sudoku_graph.remove_move(row, col)
                move_count += 1
                print("Cell cleared!")
                log_message("Cell cleared!")
            if event.key == pygame.K_s:
                if sudoku_graph.solve_sudoku():
                    print("Sudoku solved using solver!")
                    log_message("solver!")
                    log_message("Sudoku solved using")
                else:
                    print("No solution found.")
                    log_message("No solution found.")
        
        # Rendering elements
        render_grid()
        render_move_counter()
        render_console()
        render_text()
        easy_button, medium_button, hard_button, solver_button, instructions_button = render_buttons()
        
        if win_condition is False:
            if sudoku_graph.check_win_condition():
                win_condition = True
                log_message(f"Total moves made: {move_count} ")
                log_message("Sudoku!")
                log_message("You've completed the")
                log_message("Congratulations!")
                move_count = 0
        
        pygame.display.flip()
        if event.type == pygame.QUIT:
            print(f"Total moves made: {move_count} ")
            running = False

pygame.quit()
sys.exit()