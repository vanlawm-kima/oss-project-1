"""게임 전체에서 쓰는 설정값(상수) 모음."""
import os

# 화면
WIDTH = 480
HEIGHT = 640
FPS = 60
TITLE = "Vertical Shooter"

# 파일 위치 (이 파일이 있는 폴더 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

# 스프라이트 시트에서 잘라 쓸 칸: (파일, (x, y, 가로, 세로), 확대 배율)
PLAYER_FRAME = ("ship.png", (32, 0, 16, 24), 3)        # 48 x 72
BULLET_FRAME = ("laser-bolts.png", (6, 18, 5, 12), 2)  # 10 x 24
ENEMY_FRAMES = (
    ("enemy-small.png", (0, 0, 16, 16), 3),            # 48 x 48
    ("enemy-medium.png", (0, 0, 32, 16), 2),           # 64 x 32
    ("enemy-big.png", (3, 2, 26, 30), 2),              # 52 x 60
)

# 배경 (아래로 흐르는 속도, 픽셀/프레임)
BACKGROUND_IMAGE = "desert-backgorund-looped.png"
CLOUDS_IMAGE = "clouds-transparent.png"
BACKGROUND_SCALE = 2
BACKGROUND_SPEED = 1
CLOUDS_SPEED = 2

# 플레이어
PLAYER_SPEED = 6

# 총알
BULLET_SPEED = 10

# 적
ENEMY_SPEED_MIN = 2
ENEMY_SPEED_MAX = 4
ENEMY_SPAWN_MS = 700  # 몇 밀리초마다 적이 하나씩 나타나는가

# 게임 규칙
START_LIVES = 3
SCORE_PER_ENEMY = 10

# 색 (R, G, B) / 반투명 막 (R, G, B, 투명도)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
RED = (230, 50, 50)
HUD_SHADE = (0, 0, 0, 140)
GAME_OVER_SHADE = (0, 0, 0, 170)
