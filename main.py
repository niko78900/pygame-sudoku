import sys

import pygame

import config
import scoreboard
import ui
from sudoku import SudokuBoard


def score_delta(placement_count, is_correct):
    if placement_count <= 10:
        return 2 if is_correct else -1
    if placement_count <= 20:
        return 4 if is_correct else -2
    if placement_count <= 30:
        return 5 if is_correct else -3
    return 5 if is_correct else -6


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
    placement_count = 0
    score = 0
    last_cleared_values = {}
    solver_used = False
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
                    placement_count = 0
                    score = 0
                    last_cleared_values.clear()
                    solver_used = False
                    selected_cell = None
                elif buttons["medium"].collidepoint(mouse_pos):
                    console_messages.clear()
                    if board.generate("medium"):
                        ui.log_message(console_messages, "Medium puzzle generated!")
                    else:
                        ui.log_message(console_messages, "Failed to generate puzzle.")
                    win_condition = False
                    move_count = 0
                    placement_count = 0
                    score = 0
                    last_cleared_values.clear()
                    solver_used = False
                    selected_cell = None
                elif buttons["hard"].collidepoint(mouse_pos):
                    console_messages.clear()
                    if board.generate("hard"):
                        ui.log_message(console_messages, "Hard puzzle generated!")
                    else:
                        ui.log_message(console_messages, "Failed to generate puzzle.")
                    win_condition = False
                    move_count = 0
                    placement_count = 0
                    score = 0
                    last_cleared_values.clear()
                    solver_used = False
                    selected_cell = None
                elif buttons["solve"].collidepoint(mouse_pos):
                    if board.solve():
                        solver_used = True
                        ui.log_message(console_messages, "Sudoku solved using solver!")
                    else:
                        ui.log_message(console_messages, "No solution found.")
                elif buttons["instructions"].collidepoint(mouse_pos):
                    screen = ui.render_instructions(screen, fonts, theme)
                elif buttons["leaderboard"].collidepoint(mouse_pos):
                    entries = scoreboard.get_leaderboard()
                    screen = ui.render_leaderboard(screen, fonts, theme, entries)

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
                    elif board.get_value(row, col) != 0:
                        ui.log_message(
                            console_messages,
                            "Cell already filled. Press backspace to clear.",
                        )
                    elif board.make_move(row, col, value):
                        move_count += 1
                        if board.has_solution():
                            repeat_value = last_cleared_values.get((row, col)) == value
                            if repeat_value:
                                ui.log_message(
                                    console_messages,
                                    "Move recorded (no score for repeat).",
                                )
                            else:
                                placement_count += 1
                                delta = score_delta(placement_count, True)
                                score += delta
                                ui.log_message(
                                    console_messages,
                                    f"Valid move! ({delta:+d} pts)",
                                )
                        else:
                            ui.log_message(console_messages, "Move successful!")
                    else:
                        if board.has_solution():
                            placement_count += 1
                            delta = score_delta(placement_count, False)
                            score += delta
                            ui.log_message(
                                console_messages,
                                f"Invalid move. ({delta:+d} pts)",
                            )
                        else:
                            ui.log_message(console_messages, "Invalid move!")

                if selected_cell and event.key in [pygame.K_BACKSPACE, pygame.K_0]:
                    row, col = selected_cell
                    previous_value = board.get_value(row, col)
                    if board.clear_value(row, col):
                        move_count += 1
                        if previous_value != 0:
                            last_cleared_values[(row, col)] = previous_value
                        ui.log_message(console_messages, "Cell cleared!")
                    else:
                        ui.log_message(console_messages, "Cell is locked.")

                if event.key == pygame.K_s:
                    if board.solve():
                        solver_used = True
                        ui.log_message(console_messages, "Sudoku solved using solver!")
                    else:
                        ui.log_message(console_messages, "No solution found.")

        ui.draw_grid(screen, board, selected_cell, fonts, theme)
        ui.draw_move_counter(screen, fonts, move_count, score, theme)
        ui.draw_console(screen, fonts, console_messages, theme)
        ui.draw_buttons(screen, fonts, buttons, theme)

        if not win_condition and board.check_win():
            win_condition = True
            if not solver_used:
                score += 50
                ui.log_message(console_messages, "Completion bonus: +50 pts.")
            ui.log_message(console_messages, f"Total moves made: {move_count}")
            ui.log_message(console_messages, "Sudoku!")
            ui.log_message(console_messages, "You've completed the")
            ui.log_message(console_messages, "Congratulations!")
            screen, should_save = ui.prompt_save_score(screen, fonts, theme, score)
            if should_save is None:
                running = False
                break
            if should_save:
                screen, player_name = ui.prompt_player_name(screen, fonts, theme, score)
                if player_name is None:
                    running = False
                    break
                scoreboard.update_score(player_name, score)
                ui.log_message(console_messages, f"Score saved for {player_name}.")
            else:
                ui.log_message(console_messages, "Score not saved.")
            move_count = 0

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
