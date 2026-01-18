SCREEN_WIDTH = 950
SCREEN_HEIGHT = 750
GRID_SIZE = 450
GRID_ROWS = 9
CELL_SIZE = GRID_SIZE // GRID_ROWS

CONSOLE_WIDTH = 240
CONSOLE_HEIGHT = 500

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
BUTTON_SPACING = 15
BUTTON_MARGIN_RIGHT = 20
BUTTON_START_Y = 150

INSTRUCTIONS_WIDTH = 800
INSTRUCTIONS_HEIGHT = 600

MAX_CONSOLE_MESSAGES = 100
CONSOLE_VISIBLE_LINES = 24

COUNTER_FONT_SIZE = 24
CELL_FONT_SIZE = 34
CONSOLE_FONT_SIZE = 28

WINDOW_CAPTION = "Sudoku"
INSTRUCTIONS_CAPTION = "Instructions"
ACTIVITY_LOG_TEXT = "Activity Log"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DEFAULT_THEME = "light"

GRID_RADIUS = 8
PANEL_RADIUS = 12
BUTTON_RADIUS = 10
PANEL_SHADOW_OFFSET = (3, 3)
CONSOLE_PADDING = 12
CONSOLE_HEADER_SPACING = 8

THEMES = {
    "dark": {
        "background": (12, 18, 28),
        "panel": (20, 29, 44),
        "panel_border": (55, 80, 110),
        "grid_bg": (18, 26, 40),
        "grid_line_minor": (50, 70, 96),
        "grid_line_major": (95, 125, 160),
        "console_bg": (20, 30, 46),
        "text": (230, 238, 246),
        "muted_text": (160, 180, 200),
        "given_text": (125, 180, 255),
        "user_text": (230, 240, 250),
        "selected": (86, 165, 255),
        "button_text": (230, 238, 246),
        "button": {
            "easy": (35, 85, 115),
            "medium": (45, 75, 130),
            "hard": (55, 70, 150),
            "solve": (60, 105, 175),
            "instructions": (38, 55, 85),
        },
        "shadow": (0, 0, 0, 90),
    },
    "light": {
        "background": (225, 243, 252),
        "panel": (205, 232, 248),
        "panel_border": (130, 170, 200),
        "grid_bg": (214, 238, 250),
        "grid_line_minor": (135, 168, 190),
        "grid_line_major": (90, 130, 160),
        "console_bg": (203, 230, 247),
        "text": (20, 35, 50),
        "muted_text": (60, 80, 100),
        "given_text": (30, 85, 150),
        "user_text": (15, 30, 45),
        "selected": (60, 130, 200),
        "button_text": (20, 35, 50),
        "button": {
            "easy": (170, 215, 235),
            "medium": (155, 205, 230),
            "hard": (140, 195, 225),
            "solve": (130, 205, 235),
            "instructions": (175, 220, 238),
        },
        "shadow": (0, 0, 0, 40),
    },
}
