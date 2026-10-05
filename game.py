"""game.py - Quản lý lượt chơi, nước đi, ăn quân, chiếu, chiếu hết."""
from config import *
from board import Board

PLAYING, CHECK, CHECKMATE, STALEMATE = "playing", "check", "checkmate", "stalemate"


class Game:
    def __init__(self):
        self.board = Board()
        self.restart()

    def restart(self):
        self.board.reset()
        self.turn = WHITE
        self.selected = None
        self.valid_moves = []
        self.last_move = None
        self.status = PLAYING
        self.captured = {WHITE: [], BLACK: []}   # quân của mỗi bên đã bị ăn

    @property
    def game_over(self):
        return self.status in (CHECKMATE, STALEMATE)

    def handle_click(self, pos):
        if self.game_over:
            return
        x, y = pos
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            return
        r, c = y // SQUARE, x // SQUARE

        # Đã chọn quân và bấm vào ô đích hợp lệ -> di chuyển
        if self.selected and (r, c) in self.valid_moves:
            self._make_move(self.selected, (r, c))
            return

        # Chọn quân của mình
        piece = self.board.get(r, c)
        if piece and piece.color == self.turn:
            self.selected = (r, c)
            self.valid_moves = self.board.legal_moves(r, c)
        else:
            self.selected, self.valid_moves = None, []

    def _make_move(self, src, dst):
        captured = self.board.move(src[0], src[1], dst[0], dst[1])
        if captured:
            self.captured[captured.color].append(captured.kind)
        self.last_move = (src, dst)
        self.selected, self.valid_moves = None, []

        # Đổi lượt
        self.turn = BLACK if self.turn == WHITE else WHITE
        self._update_status()

    def _update_status(self):
        in_check = self.board.in_check(self.turn)
        has_move = self.board.has_any_legal_move(self.turn)
        if in_check and not has_move:
            self.status = CHECKMATE
        elif not in_check and not has_move:
            self.status = STALEMATE
        elif in_check:
            self.status = CHECK
        else:
            self.status = PLAYING

    # ---------- Văn bản hiển thị ----------
    def turn_name(self):
        return "TRẮNG" if self.turn == WHITE else "ĐEN"

    def status_text(self):
        if self.status == CHECKMATE:
            winner = "ĐEN" if self.turn == WHITE else "TRẮNG"
            return f"CHIẾU HẾT! {winner} thắng"
        if self.status == STALEMATE:
            return "HÒA (hết nước đi)"
        if self.status == CHECK:
            return "CHIẾU!"
        return ""