"""board.py - Quản lý bàn cờ, vị trí quân, vẽ bàn cờ, kiểm tra chiếu."""
import os
import pygame
from config import *
from piece import PIECE_CLASSES, Queen

# Ma trận ban đầu như thiết kế ở báo cáo (mục 4.2)
INITIAL_LAYOUT = [
    ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
    ["BP"] * 8,
    [""] * 8, [""] * 8, [""] * 8, [""] * 8,
    ["WP"] * 8,
    ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"],
]

SYMBOLS = {"K": "K", "Q": "Q", "R": "R", "B": "B", "N": "N", "P": "P"}


class Board:
    def __init__(self):
        self.grid = []
        self.images = {}
        self.font = None
        self.small_font = None
        self.reset()

    # ---------- Khởi tạo ----------
    def reset(self):
        self.grid = [[None] * 8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                code = INITIAL_LAYOUT[r][c]
                if code:
                    self.grid[r][c] = PIECE_CLASSES[code[1]](code[0])

    def load_assets(self):
        """Nạp ảnh quân cờ từ assets/pieces. Nếu thiếu ảnh sẽ tự vẽ hình thay thế."""
        base = os.path.join(os.path.dirname(__file__), "assets", "pieces")
        for color, cname in (("W", "white"), ("B", "black")):
            for kind, cls in PIECE_CLASSES.items():
                path = os.path.join(base, f"{cname}_{cls.name}.png")
                if os.path.exists(path):
                    img = pygame.image.load(path).convert_alpha()
                    self.images[color + kind] = pygame.transform.smoothscale(
                        img, (SQUARE - 10, SQUARE - 10))
        self.font = pygame.font.SysFont("arial", 38, bold=True)
        self.small_font = pygame.font.SysFont("arial", 14, bold=True)

    # ---------- Truy xuất ----------
    def get(self, r, c):
        return self.grid[r][c]

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.kind == "K" and p.color == color:
                    return (r, c)
        return None

    # ---------- Chiếu / nước đi hợp lệ ----------
    def is_attacked(self, r, c, by_color):
        for rr in range(8):
            for cc in range(8):
                p = self.grid[rr][cc]
                if p and p.color == by_color and (r, c) in p.attacks(self.grid, rr, cc):
                    return True
        return False

    def in_check(self, color):
        king = self.find_king(color)
        enemy = BLACK if color == WHITE else WHITE
        return king is not None and self.is_attacked(king[0], king[1], enemy)

    def legal_moves(self, r, c):
        """Nước đi hợp lệ: đúng luật di chuyển và không làm vua mình bị chiếu."""
        piece = self.grid[r][c]
        if piece is None:
            return []
        result = []
        for (nr, nc) in piece.moves(self.grid, r, c):
            captured = self.grid[nr][nc]
            self.grid[nr][nc], self.grid[r][c] = piece, None   # thử đi
            if not self.in_check(piece.color):
                result.append((nr, nc))
            self.grid[r][c], self.grid[nr][nc] = piece, captured  # hoàn tác
        return result

    def has_any_legal_move(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and self.legal_moves(r, c):
                    return True
        return False

    # ---------- Di chuyển ----------
    def move(self, fr, fc, tr, tc):
        """Thực hiện nước đi. Trả về quân bị ăn (nếu có)."""
        piece = self.grid[fr][fc]
        captured = self.grid[tr][tc]
        self.grid[tr][tc], self.grid[fr][fc] = piece, None
        # Phong cấp: tốt đến hàng cuối tự động thành Hậu
        if piece.kind == "P" and tr in (0, 7):
            self.grid[tr][tc] = Queen(piece.color)
        return captured

    # ---------- Vẽ ----------
    def draw(self, screen, selected, valid_moves, last_move, turn):
        king_in_check = self.find_king(turn) if self.in_check(turn) else None
        for r in range(8):
            for c in range(8):
                color = LIGHT_SQUARE if (r + c) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(c * SQUARE, r * SQUARE, SQUARE, SQUARE)
                pygame.draw.rect(screen, color, rect)

                if last_move and (r, c) in last_move:
                    pygame.draw.rect(screen, LAST_MOVE_COLOR, rect)
                if selected == (r, c):
                    pygame.draw.rect(screen, SELECTED_COLOR, rect)
                if king_in_check == (r, c):
                    pygame.draw.rect(screen, CHECK_COLOR, rect)

                # tọa độ
                lbl_color = DARK_SQUARE if (r + c) % 2 == 0 else LIGHT_SQUARE
                if c == 0:
                    screen.blit(self.small_font.render(str(8 - r), True, lbl_color),
                                (rect.x + 3, rect.y + 2))
                if r == 7:
                    screen.blit(self.small_font.render("abcdefgh"[c], True, lbl_color),
                                (rect.right - 12, rect.bottom - 18))

        # gợi ý nước đi
        for (r, c) in valid_moves:
            center = (c * SQUARE + SQUARE // 2, r * SQUARE + SQUARE // 2)
            if self.grid[r][c] is None:
                pygame.draw.circle(screen, MOVE_HINT_COLOR, center, 10)
            else:
                pygame.draw.circle(screen, MOVE_HINT_COLOR, center, SQUARE // 2 - 4, 5)

        # quân cờ
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p:
                    self._draw_piece(screen, p, r, c)

    def _draw_piece(self, screen, piece, r, c):
        x, y = c * SQUARE, r * SQUARE
        img = self.images.get(piece.code)
        if img:
            screen.blit(img, (x + 5, y + 5))
            return
        # Không có ảnh -> vẽ quân bằng hình tròn + chữ cái
        center = (x + SQUARE // 2, y + SQUARE // 2)
        fill = (250, 250, 250) if piece.color == WHITE else (30, 30, 30)
        edge = (30, 30, 30) if piece.color == WHITE else (250, 250, 250)
        pygame.draw.circle(screen, fill, center, SQUARE // 2 - 10)
        pygame.draw.circle(screen, edge, center, SQUARE // 2 - 10, 3)
        text = self.font.render(SYMBOLS[piece.kind], True, edge)
        screen.blit(text, text.get_rect(center=center))