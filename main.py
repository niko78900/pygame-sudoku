import sys

import pygame

import config
import ui
from sudoku import SudokuBoard


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.WINDOW_CAPTION)

    fonts = {
        "counter": pygame.font.Font(None, config.COUNTER_FONT_SIZE),
        "cell": pygame.font.Font(None, config.CELL_FONT_SIZE),
        "console": pygame.font.Font(None, config.CONSOLE_FONT_SIZE),
    }

    board = SudokuBoard()
    selected_cell = None
    move_count = 0
    console_messages = []
    win_condition = False

    theme_name = config.DEFAULT_THEME
    theme = config.THEMES[theme_name]

    buttons = ui.create_buttons()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected_cell = ui.get_cell_from_mouse(event.pos)
                mouse_pos = event.pos

                if buttons["easy"].collidepoint(mouse_pos):
                    console_messages.clear()
                    if board.generate("easy"):
                        ui.log_message(console_messages, "Easy puzzle generated!")
                    else:
                        ui.log_message(console_messages, "Failed to generate puzzle.")
                    win_condition = False
                    move_count = 0
                    selected_cell = None
                elif buttons["medium"].collidepoint(mouse_pos):
                    console_messages.clear()
                    if board.generate("medium"):
                        ui.log_message(console_messages, "Medium puzzle generated!")
                    else:
                        ui.log_message(console_messages, "Failed to generate puzzle.")
                    win_condition = False
                    move_count = 0
                    selected_cell = None
                elif buttons["hard"].collidepoint(mouse_pos):
                    console_messages.clear()
                    if board.generate("hard"):
                        ui.log_message(console_messages, "Hard puzzle generated!")
                    else:
                        ui.log_message(console_messages, "Failed to generate puzzle.")
                    win_condition = False
                    move_count = 0
                    selected_cell = None
                elif buttons["solve"].collidepoint(mouse_pos):
                    if board.solve():
                        ui.log_message(console_messages, "Sudoku solved using solver!")
                    else:
                        ui.log_message(console_messages, "No solution found.")
                elif buttons["instructions"].collidepoint(mouse_pos):
                    screen = ui.render_instructions(screen, fonts, theme)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    theme_name = "light" if theme_name == "dark" else "dark"
                    theme = config.THEMES[theme_name]
                    ui.log_message(
                        console_messages, f"Theme set to {theme_name}."
                    )
                if selected_cell and event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                ]:
                    row, col = selected_cell
                    value = event.key - pygame.K_0
                    if board.is_given(row, col):
                        ui.log_message(console_messages, "Cell is locked.")
                    elif board.make_move(row, col, value):
                        move_count += 1
                        ui.log_message(console_messages, "Move successful!")
                    else:
                        ui.log_message(console_messages, "Invalid move!")

                if selected_cell and event.key in [pygame.K_BACKSPACE, pygame.K_0]:
                    row, col = selected_cell
                    if board.clear_value(row, col):
                        move_count += 1
                        ui.log_message(console_messages, "Cell cleared!")
                    else:
                        ui.log_message(console_messages, "Cell is locked.")

                if event.key == pygame.K_s:
                    if board.solve():
                        ui.log_message(console_messages, "Sudoku solved using solver!")
                    else:
                        ui.log_message(console_messages, "No solution found.")

        ui.draw_grid(screen, board, selected_cell, fonts, theme)
        ui.draw_move_counter(screen, fonts, move_count, theme)
        ui.draw_console(screen, fonts, console_messages, theme)
        ui.draw_buttons(screen, fonts, buttons, theme)

        if not win_condition and board.check_win():
            win_condition = True
            ui.log_message(console_messages, f"Total moves made: {move_count}")
            ui.log_message(console_messages, "Sudoku!")
            ui.log_message(console_messages, "You've completed the")
            ui.log_message(console_messages, "Congratulations!")
            move_count = 0

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
