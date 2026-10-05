"""main.py - Khởi động chương trình, vòng lặp chính, xử lý chuột, hiển thị giao diện."""
import sys
import pygame
from config import *
from game import Game

MENU, PLAY = "menu", "play"


class Button:
    def __init__(self, rect, text, color=BUTTON_COLOR, hover=BUTTON_HOVER):
        self.rect = pygame.Rect(rect)
        self.text, self.color, self.hover = text, color, hover

    def draw(self, screen, font):
        c = self.hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, c, self.rect, border_radius=8)
        label = font.render(self.text, True, TEXT_COLOR)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chơi Cờ Vua - Python & Pygame")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 48, bold=True)
    big_font = pygame.font.SysFont("arial", 26, bold=True)
    font = pygame.font.SysFont("arial", 20, bold=True)
    small_font = pygame.font.SysFont("arial", 16)

    game = Game()
    game.board.load_assets()
    state = MENU

    # Nút ở menu
    cx = WIDTH // 2
    btn_start = Button((cx - 110, 300, 220, 55), "BẮT ĐẦU")
    btn_exit_menu = Button((cx - 110, 375, 220, 55), "THOÁT", BUTTON_DANGER, BUTTON_DANGER_HOVER)

    # Nút trong ván chơi (bảng bên phải)
    px = BOARD_SIZE + 20
    btn_restart = Button((px, HEIGHT - 180, PANEL_WIDTH - 40, 48), "CHƠI LẠI")
    btn_menu = Button((px, HEIGHT - 120, PANEL_WIDTH - 40, 48), "MENU")
    btn_exit = Button((px, HEIGHT - 60, PANEL_WIDTH - 40, 48), "THOÁT", BUTTON_DANGER, BUTTON_DANGER_HOVER)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == MENU:
                    if btn_start.clicked(event.pos):
                        game.restart()
                        state = PLAY
                    elif btn_exit_menu.clicked(event.pos):
                        running = False
                else:
                    if btn_restart.clicked(event.pos):
                        game.restart()
                    elif btn_menu.clicked(event.pos):
                        state = MENU
                    elif btn_exit.clicked(event.pos):
                        running = False
                    else:
                        game.handle_click(event.pos)

        # ---------- Vẽ ----------
        if state == MENU:
            screen.fill(PANEL_BG)
            t = title_font.render("CHƠI CỜ VUA", True, TEXT_COLOR)
            screen.blit(t, t.get_rect(center=(cx, 180)))
            s = small_font.render("Hai người chơi trên cùng một máy", True, (180, 180, 190))
            screen.blit(s, s.get_rect(center=(cx, 235)))
            btn_start.draw(screen, font)
            btn_exit_menu.draw(screen, font)
        else:
            game.board.draw(screen, game.selected, game.valid_moves,
                            game.last_move, game.turn)
            # Bảng thông tin
            pygame.draw.rect(screen, PANEL_BG, (BOARD_SIZE, 0, PANEL_WIDTH, HEIGHT))
            screen.blit(big_font.render("CỜ VUA", True, TEXT_COLOR), (px, 20))
            screen.blit(font.render("Lượt:", True, (180, 180, 190)), (px, 80))
            screen.blit(big_font.render(game.turn_name(), True, TEXT_COLOR), (px, 108))

            msg = game.status_text()
            if msg:
                color = (255, 120, 120) if game.status != "stalemate" else (230, 220, 120)
                # tự xuống dòng nếu quá dài
                words, line, y = msg.split(" "), "", 160
                for w in words:
                    test = (line + " " + w).strip()
                    if font.size(test)[0] > PANEL_WIDTH - 40:
                        screen.blit(font.render(line, True, color), (px, y))
                        line, y = w, y + 28
                    else:
                        line = test
                screen.blit(font.render(line, True, color), (px, y))

            # Quân đã bị ăn
            y = 280
            for color, name in ((WHITE, "Trắng"), (BLACK, "Đen")):
                lost = " ".join(game.captured[color]) or "-"
                screen.blit(small_font.render(f"{name} mất: {lost}", True, (200, 200, 210)), (px, y))
                y += 26

            btn_restart.draw(screen, font)
            btn_menu.draw(screen, font)
            btn_exit.draw(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()