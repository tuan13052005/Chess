"""piece.py - Các loại quân cờ và quy tắc di chuyển cơ bản (chưa xét chiếu)."""

ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
KNIGHT_JUMPS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)]


def inside(r, c):
    return 0 <= r < 8 and 0 <= c < 8


class Piece:
    kind = ""        # K, Q, R, B, N, P
    name = ""        # tên dùng cho file ảnh

    def __init__(self, color):
        self.color = color           # "W" hoặc "B"

    @property
    def code(self):
        return self.color + self.kind  # ví dụ: "WK"

    def moves(self, grid, r, c):
        """Các nước đi theo luật di chuyển (chưa kiểm tra vua có bị chiếu)."""
        raise NotImplementedError

    def attacks(self, grid, r, c):
        """Các ô mà quân này đang tấn công (mặc định giống nước đi)."""
        return self.moves(grid, r, c)

    def _slide(self, grid, r, c, dirs):
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            while inside(nr, nc):
                target = grid[nr][nc]
                if target is None:
                    result.append((nr, nc))
                else:
                    if target.color != self.color:
                        result.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return result

    def _step(self, grid, r, c, offsets):
        result = []
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if inside(nr, nc):
                target = grid[nr][nc]
                if target is None or target.color != self.color:
                    result.append((nr, nc))
        return result


class King(Piece):
    kind, name = "K", "king"

    def moves(self, grid, r, c):
        return self._step(grid, r, c, ROOK_DIRS + BISHOP_DIRS)


class Queen(Piece):
    kind, name = "Q", "queen"

    def moves(self, grid, r, c):
        return self._slide(grid, r, c, ROOK_DIRS + BISHOP_DIRS)


class Rook(Piece):
    kind, name = "R", "rook"

    def moves(self, grid, r, c):
        return self._slide(grid, r, c, ROOK_DIRS)


class Bishop(Piece):
    kind, name = "B", "bishop"

    def moves(self, grid, r, c):
        return self._slide(grid, r, c, BISHOP_DIRS)


class Knight(Piece):
    kind, name = "N", "knight"

    def moves(self, grid, r, c):
        return self._step(grid, r, c, KNIGHT_JUMPS)


class Pawn(Piece):
    kind, name = "P", "pawn"

    def moves(self, grid, r, c):
        result = []
        d = -1 if self.color == "W" else 1          # Trắng đi lên, Đen đi xuống
        start_row = 6 if self.color == "W" else 1

        # Đi thẳng 1 ô, và 2 ô từ vị trí ban đầu
        if inside(r + d, c) and grid[r + d][c] is None:
            result.append((r + d, c))
            if r == start_row and grid[r + 2 * d][c] is None:
                result.append((r + 2 * d, c))

        # Ăn chéo
        for dc in (-1, 1):
            nr, nc = r + d, c + dc
            if inside(nr, nc):
                t = grid[nr][nc]
                if t is not None and t.color != self.color:
                    result.append((nr, nc))
        return result

    def attacks(self, grid, r, c):
        d = -1 if self.color == "W" else 1
        return [(r + d, c + dc) for dc in (-1, 1) if inside(r + d, c + dc)]


PIECE_CLASSES = {"K": King, "Q": Queen, "R": Rook,
                 "B": Bishop, "N": Knight, "P": Pawn}