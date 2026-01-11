import pygame

import config


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


def draw_move_counter(screen, fonts, move_count, theme):
    text_surface = fonts["counter"].render(
        f"Moves: {move_count}", True, theme["muted_text"]
    )
    screen.blit(text_surface, (10, 10))


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
