"""config.py - Các hằng số cấu hình cho ứng dụng cờ vua."""

SQUARE = 80                      # Kích thước mỗi ô (pixel)
BOARD_SIZE = SQUARE * 8          # 640 px
PANEL_WIDTH = 220                # Bảng thông tin bên phải
WIDTH = BOARD_SIZE + PANEL_WIDTH
HEIGHT = BOARD_SIZE
FPS = 60

# Màu sắc (R, G, B)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOR = (246, 246, 105)
MOVE_HINT_COLOR = (90, 160, 90)
LAST_MOVE_COLOR = (205, 210, 106)
CHECK_COLOR = (220, 60, 60)

PANEL_BG = (40, 40, 48)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (70, 110, 170)
BUTTON_HOVER = (95, 140, 205)
BUTTON_DANGER = (170, 70, 70)
BUTTON_DANGER_HOVER = (205, 95, 95)

WHITE = "W"
BLACK = "B"