import pygame

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ Pygame
WIDTH, HEIGHT = 300, 300
TILE_SIZE = WIDTH // 3

# Màu sắc
COLORS = {
    "WHITE": {"hex": "#FFFFFF", "rgb": (255, 255, 255)},
    "BLACK": {"hex": "#333333", "rgb": (51, 51, 51)},  # Đen đậm nhẹ
    "PRIMARY": {"hex": "#4A90E2", "rgb": (74, 144, 226)},  # Xanh dương chính
    "SECONDARY": {"hex": "#F5F7FA", "rgb": (245, 247, 250)},  # Xám nhạt nền
    "ACCENT": {"hex": "#50C878", "rgb": (80, 200, 120)},  # Xanh lá nổi bật
    "GRAY": {"hex": "#E0E6ED", "rgb": (224, 230, 237)},  # Xám nhạt
    "DARK_GRAY": {"hex": "#7F8FA6", "rgb": (127, 143, 166)},  # Xám đậm
    "SHADOW": {"hex": "#D1D9E6", "rgb": (209, 217, 230)},  # Màu bóng đổ
}