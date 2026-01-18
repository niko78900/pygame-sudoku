import pygame

import config
import scoreboard


def get_grid_offset():
    offset_x = (config.SCREEN_WIDTH - config.GRID_SIZE) // 2
    offset_y = (config.SCREEN_HEIGHT - config.GRID_SIZE) // 2
    return offset_x, offset_y


def create_buttons():
    x_pos = config.SCREEN_WIDTH - config.BUTTON_WIDTH - config.BUTTON_MARGIN_RIGHT
    y_start = config.BUTTON_START_Y

    return {
        "easy": pygame.Rect(x_pos, y_start, config.BUTTON_WIDTH, config.BUTTON_HEIGHT),
        "medium": pygame.Rect(
            x_pos,
            y_start + config.BUTTON_HEIGHT + config.BUTTON_SPACING,
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
        ),
        "hard": pygame.Rect(
            x_pos,
            y_start + 2 * (config.BUTTON_HEIGHT + config.BUTTON_SPACING),
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
        ),
        "solve": pygame.Rect(
            x_pos,
            y_start + 3 * (config.BUTTON_HEIGHT + config.BUTTON_SPACING),
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
        ),
        "instructions": pygame.Rect(
            x_pos,
            y_start + 4 * (config.BUTTON_HEIGHT + config.BUTTON_SPACING),
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
        ),
        "leaderboard": pygame.Rect(
            x_pos,
            y_start + 5 * (config.BUTTON_HEIGHT + config.BUTTON_SPACING),
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
        ),
    }


def draw_shadow(screen, rect, color, offset, radius):
    if not color:
        return
    shadow_rect = rect.move(offset)
    shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(
        shadow_surface,
        color,
        shadow_surface.get_rect(),
        border_radius=radius,
    )
    screen.blit(shadow_surface, shadow_rect)


def draw_panel(screen, rect, fill_color, border_color, radius):
    pygame.draw.rect(screen, fill_color, rect, border_radius=radius)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=radius)


def draw_grid(screen, board, selected_cell, fonts, theme):
    screen.fill(theme["background"])

    offset_x, offset_y = get_grid_offset()
    grid_rect = pygame.Rect(offset_x, offset_y, config.GRID_SIZE, config.GRID_SIZE)

    draw_shadow(
        screen,
        grid_rect,
        theme["shadow"],
        config.PANEL_SHADOW_OFFSET,
        config.GRID_RADIUS,
    )
    draw_panel(
        screen,
        grid_rect,
        theme["grid_bg"],
        theme["panel_border"],
        config.GRID_RADIUS,
    )

    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1
        line_color = (
            theme["grid_line_major"] if i % 3 == 0 else theme["grid_line_minor"]
        )
        start_h = (offset_x, offset_y + i * config.CELL_SIZE)
        end_h = (offset_x + config.GRID_SIZE, offset_y + i * config.CELL_SIZE)
        start_v = (offset_x + i * config.CELL_SIZE, offset_y)
        end_v = (offset_x + i * config.CELL_SIZE, offset_y + config.GRID_SIZE)

        if thickness == 1:
            pygame.draw.aaline(screen, line_color, start_h, end_h)
            pygame.draw.aaline(screen, line_color, start_v, end_v)
        else:
            pygame.draw.line(screen, line_color, start_h, end_h, thickness)
            pygame.draw.line(screen, line_color, start_v, end_v, thickness)

    for row in range(9):
        for col in range(9):
            num = board.get_value(row, col)
            if num != 0:
                color = (
                    theme["given_text"]
                    if board.is_given(row, col)
                    else theme["user_text"]
                )
                text = fonts["cell"].render(str(num), True, color)
                x_pos = offset_x + col * config.CELL_SIZE
                y_pos = offset_y + row * config.CELL_SIZE
                text_rect = text.get_rect(
                    center=(x_pos + config.CELL_SIZE // 2, y_pos + config.CELL_SIZE // 2)
                )
                screen.blit(text, text_rect)

    if selected_cell:
        sel_row, sel_col = selected_cell
        pygame.draw.rect(
            screen,
            theme["selected"],
            pygame.Rect(
                offset_x + sel_col * config.CELL_SIZE,
                offset_y + sel_row * config.CELL_SIZE,
                config.CELL_SIZE,
                config.CELL_SIZE,
            ),
            3,
            border_radius=6,
        )


def draw_buttons(screen, fonts, buttons, theme):
    labels = {
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "solve": "Solve!",
        "instructions": "Instructions",
        "leaderboard": "Leaderboard",
    }

    for key, rect in buttons.items():
        draw_shadow(
            screen,
            rect,
            theme["shadow"],
            config.PANEL_SHADOW_OFFSET,
            config.BUTTON_RADIUS,
        )
        draw_panel(screen, rect, theme["button"][key], theme["panel_border"], config.BUTTON_RADIUS)
        text = fonts["counter"].render(labels[key], True, theme["button_text"])
        screen.blit(
            text,
            (
                rect.x + (rect.width - text.get_width()) // 2,
                rect.y + (rect.height - text.get_height()) // 2,
            ),
        )


def draw_move_counter(screen, fonts, move_count, score, theme):
    moves_surface = fonts["counter"].render(
        f"Moves: {move_count}", True, theme["muted_text"]
    )
    score_surface = fonts["counter"].render(
        f"Score: {score}", True, theme["muted_text"]
    )
    screen.blit(moves_surface, (10, 10))
    screen.blit(score_surface, (10, 10 + moves_surface.get_height() + 4))


def wrap_text(font, text, max_width):
    lines = []
    for raw_line in text.splitlines() or [""]:
        if raw_line == "":
            lines.append("")
            continue
        words = raw_line.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if font.size(candidate)[0] <= max_width:
                current = candidate
                continue
            lines.append(current)
            if font.size(word)[0] <= max_width:
                current = word
                continue
            chunk = ""
            for char in word:
                candidate = chunk + char
                if font.size(candidate)[0] <= max_width:
                    chunk = candidate
                else:
                    if chunk:
                        lines.append(chunk)
                    chunk = char
            current = chunk
        lines.append(current)
    return lines


def draw_console(screen, fonts, console_messages, theme):
    console_rect = pygame.Rect(
        5,
        (config.SCREEN_HEIGHT - config.CONSOLE_HEIGHT) // 2,
        config.CONSOLE_WIDTH,
        config.CONSOLE_HEIGHT,
    )
    draw_shadow(
        screen,
        console_rect,
        theme["shadow"],
        config.PANEL_SHADOW_OFFSET,
        config.PANEL_RADIUS,
    )
    draw_panel(
        screen,
        console_rect,
        theme["console_bg"],
        theme["panel_border"],
        config.PANEL_RADIUS,
    )

    padding = config.CONSOLE_PADDING
    header_text = fonts["console"].render(
        config.ACTIVITY_LOG_TEXT, True, theme["text"]
    )
    header_pos = (console_rect.x + padding, console_rect.y + padding)
    screen.blit(header_text, header_pos)

    content_top = header_pos[1] + header_text.get_height() + config.CONSOLE_HEADER_SPACING
    inner_rect = pygame.Rect(
        console_rect.x + padding,
        content_top,
        console_rect.width - 2 * padding,
        console_rect.bottom - padding - content_top,
    )
    line_height = fonts["console"].get_linesize()
    max_lines = min(
        config.CONSOLE_VISIBLE_LINES, max(1, inner_rect.height // line_height)
    )

    clip_rect = screen.get_clip()
    screen.set_clip(inner_rect)

    wrapped_lines = []
    for message in reversed(console_messages):
        for line in wrap_text(fonts["console"], message, inner_rect.width):
            wrapped_lines.append(line)
            if len(wrapped_lines) >= max_lines:
                break
        if len(wrapped_lines) >= max_lines:
            break

    for i, line in enumerate(wrapped_lines):
        text_surface = fonts["console"].render(line, True, theme["text"])
        screen.blit(text_surface, (inner_rect.x, inner_rect.y + i * line_height))

    screen.set_clip(clip_rect)


def log_message(console_messages, message):
    console_messages.append(message)
    if len(console_messages) > config.MAX_CONSOLE_MESSAGES:
        console_messages.pop(0)


def get_cell_from_mouse(pos):
    offset_x, offset_y = get_grid_offset()
    x, y = pos
    col = (x - offset_x) // config.CELL_SIZE
    row = (y - offset_y) // config.CELL_SIZE
    if 0 <= row < 9 and 0 <= col < 9:
        return row, col
    return None


def render_instructions(screen, fonts, theme):
    instruction_window = pygame.display.set_mode(
        (config.INSTRUCTIONS_WIDTH, config.INSTRUCTIONS_HEIGHT)
    )
    pygame.display.set_caption(config.INSTRUCTIONS_CAPTION)
    instruction_window.fill(theme["background"])

    instructions = [
        "Welcome to Sudoku!",
        "1. Click on a cell to select it.",
        "2. Type a number 1 through 9 on your keyboard to place it in the cell.",
        "3. To delete a number from a cell, press backspace or 0.",
        "4. Cells with darker numbers are given clues and cannot be edited.",
        "5. Use the Solver button to solve the board automatically.",
        "6. Use the Easy, Medium, or Hard buttons to start a new game.",
        "7. To win, fill the board correctly with numbers 1 through 9.",
        "8. View the leaderboard using the Leaderboard button.",
        "9. Your score is saved after completing a puzzle.",
        "Press T to toggle the theme.",
        "Press ESC to return to the game.",
    ]

    y_offset = 20
    for line in instructions:
        text_surface = fonts["console"].render(line, True, theme["text"])
        instruction_window.blit(text_surface, (20, y_offset))
        y_offset += 40

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                pygame.display.set_caption(config.WINDOW_CAPTION)
                return screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                pygame.display.set_caption(config.WINDOW_CAPTION)
                return screen


def prompt_player_name(screen, fonts, theme, score):
    prompt_window = pygame.display.set_mode(
        (config.NAME_PROMPT_WIDTH, config.NAME_PROMPT_HEIGHT)
    )
    pygame.display.set_caption(config.NAME_PROMPT_CAPTION)

    input_text = ""
    error_message = ""
    clock = pygame.time.Clock()

    panel_rect = pygame.Rect(
        20,
        20,
        config.NAME_PROMPT_WIDTH - 40,
        config.NAME_PROMPT_HEIGHT - 40,
    )
    input_rect = pygame.Rect(
        panel_rect.x + 20,
        panel_rect.y + 110,
        panel_rect.width - 40,
        44,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                pygame.display.set_caption(config.WINDOW_CAPTION)
                return screen, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    candidate = input_text.strip()
                    error_message = scoreboard.validate_name(candidate)
                    if not error_message:
                        screen = pygame.display.set_mode(
                            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
                        )
                        pygame.display.set_caption(config.WINDOW_CAPTION)
                        return screen, candidate
                    input_text = candidate
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode:
                    if (
                        len(input_text) < config.NAME_MAX_LENGTH
                        and event.unicode in scoreboard.ALLOWED_NAME_CHARS
                    ):
                        input_text += event.unicode

        prompt_window.fill(theme["background"])
        draw_shadow(
            prompt_window,
            panel_rect,
            theme["shadow"],
            config.PANEL_SHADOW_OFFSET,
            config.PANEL_RADIUS,
        )
        draw_panel(
            prompt_window,
            panel_rect,
            theme["panel"],
            theme["panel_border"],
            config.PANEL_RADIUS,
        )

        title = fonts["console"].render("Save your score", True, theme["text"])
        prompt_window.blit(title, (panel_rect.x + 20, panel_rect.y + 20))

        score_text = fonts["counter"].render(f"Score: {score}", True, theme["muted_text"])
        prompt_window.blit(score_text, (panel_rect.x + 20, panel_rect.y + 60))

        hint = f"Name (max {config.NAME_MAX_LENGTH}):"
        hint_text = fonts["counter"].render(hint, True, theme["muted_text"])
        prompt_window.blit(hint_text, (input_rect.x, input_rect.y - 28))

        pygame.draw.rect(prompt_window, theme["grid_bg"], input_rect, border_radius=8)
        pygame.draw.rect(prompt_window, theme["panel_border"], input_rect, 2, border_radius=8)

        display_text = input_text or " "
        text_surface = fonts["console"].render(display_text, True, theme["text"])
        prompt_window.blit(text_surface, (input_rect.x + 10, input_rect.y + 6))

        if error_message:
            error_lines = wrap_text(fonts["counter"], error_message, panel_rect.width - 40)
            for index, line in enumerate(error_lines):
                error_surface = fonts["counter"].render(line, True, theme["given_text"])
                prompt_window.blit(
                    error_surface,
                    (panel_rect.x + 20, input_rect.bottom + 12 + index * 22),
                )
        else:
            help_text = "Press Enter to save."
            help_surface = fonts["counter"].render(help_text, True, theme["muted_text"])
            prompt_window.blit(help_surface, (panel_rect.x + 20, input_rect.bottom + 14))

        pygame.display.flip()
        clock.tick(30)


def render_leaderboard(screen, fonts, theme, entries):
    leaderboard_window = pygame.display.set_mode(
        (config.LEADERBOARD_WIDTH, config.LEADERBOARD_HEIGHT)
    )
    pygame.display.set_caption(config.LEADERBOARD_CAPTION)

    clock = pygame.time.Clock()

    panel_rect = pygame.Rect(
        24,
        24,
        config.LEADERBOARD_WIDTH - 48,
        config.LEADERBOARD_HEIGHT - 48,
    )
    header_y = panel_rect.y + 20
    line_height = fonts["console"].get_linesize()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                pygame.display.set_caption(config.WINDOW_CAPTION)
                return screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                pygame.display.set_caption(config.WINDOW_CAPTION)
                return screen

        leaderboard_window.fill(theme["background"])
        draw_shadow(
            leaderboard_window,
            panel_rect,
            theme["shadow"],
            config.PANEL_SHADOW_OFFSET,
            config.PANEL_RADIUS,
        )
        draw_panel(
            leaderboard_window,
            panel_rect,
            theme["panel"],
            theme["panel_border"],
            config.PANEL_RADIUS,
        )

        title = fonts["console"].render("Leaderboard", True, theme["text"])
        leaderboard_window.blit(title, (panel_rect.x + 20, header_y))

        col_rank = panel_rect.x + 20
        col_name = panel_rect.x + 90
        col_score = panel_rect.right - 120
        header_y += line_height + 10

        header_rank = fonts["counter"].render("Rank", True, theme["muted_text"])
        header_name = fonts["counter"].render("Player", True, theme["muted_text"])
        header_score = fonts["counter"].render("Score", True, theme["muted_text"])
        leaderboard_window.blit(header_rank, (col_rank, header_y))
        leaderboard_window.blit(header_name, (col_name, header_y))
        leaderboard_window.blit(header_score, (col_score, header_y))

        content_y = header_y + line_height + 8
        if not entries:
            empty_text = fonts["counter"].render(
                "No scores yet. Finish a puzzle to add one!", True, theme["muted_text"]
            )
            leaderboard_window.blit(empty_text, (panel_rect.x + 20, content_y))
        else:
            max_entries = min(config.LEADERBOARD_MAX_ENTRIES, len(entries))
            for index in range(max_entries):
                entry = entries[index]
                rank_text = fonts["counter"].render(
                    str(index + 1), True, theme["text"]
                )
                name_text = fonts["counter"].render(
                    entry["name"], True, theme["text"]
                )
                score_text = fonts["counter"].render(
                    str(entry["score"]), True, theme["text"]
                )
                y_pos = content_y + index * (line_height + 6)
                leaderboard_window.blit(rank_text, (col_rank, y_pos))
                leaderboard_window.blit(name_text, (col_name, y_pos))
                leaderboard_window.blit(score_text, (col_score, y_pos))

        footer_text = fonts["counter"].render(
            "Press ESC to return.", True, theme["muted_text"]
        )
        leaderboard_window.blit(
            footer_text,
            (panel_rect.x + 20, panel_rect.bottom - footer_text.get_height() - 14),
        )

        pygame.display.flip()
        clock.tick(30)
