# Chess Game - Python & Pygame

## Cài đặt
    pip install pygame-ce

(pygame-ce là bản cộng đồng của pygame, vẫn dùng `import pygame`, hỗ trợ tốt Python 3.12 - 3.14.)

## Chạy
    python main.py

## Cách chơi
- Bấm chuột vào quân của mình để chọn (ô vàng), các nước đi hợp lệ được gợi ý (chấm/vòng xanh).
- Bấm vào ô đích để di chuyển. Trắng đi trước, hai bên luân phiên.
- Ô vua chuyển đỏ khi bị chiếu. Ván kết thúc khi chiếu hết hoặc hòa (hết nước đi).
- Tốt đi đến hàng cuối tự động phong Hậu.

## Ảnh quân cờ (tùy chọn)
Đặt ảnh PNG vào assets/pieces/ với tên: white_king.png, white_queen.png, ... black_pawn.png.
Nếu không có ảnh, chương trình tự vẽ quân bằng hình tròn + chữ cái (K, Q, R, B, N, P).