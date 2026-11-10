"""게임에 나오는 것들 — Background(배경), Player(플레이어), Bullet(총알), Enemy(적)."""
import os
import random

import pygame

from settings import (
    ASSET_DIR, WIDTH, HEIGHT,
    PLAYER_FRAME, BULLET_FRAME, ENEMY_FRAMES,
    BACKGROUND_IMAGE, CLOUDS_IMAGE, BACKGROUND_SCALE, BACKGROUND_SPEED, CLOUDS_SPEED,
    PLAYER_SPEED, BULLET_SPEED, ENEMY_SPEED_MIN, ENEMY_SPEED_MAX,
)

_image_cache = {}


def load_frame(name, frame=None, scale=1):
    """assets/ 의 그림 name 에서 frame=(x, y, 가로, 세로) 칸 하나를 잘라 scale로 키운다.

    frame 이 None 이면 그림 전체. 픽셀 그림이라 부드럽게 하지 않고 픽셀 그대로 키운다.
    같은 그림은 한 번만 만들어 두고 다시 쓴다. pygame.display.set_mode() 다음에 불러야 한다.
    """
    key = (name, frame, scale)
    if key not in _image_cache:
        image = pygame.image.load(os.path.join(ASSET_DIR, name)).convert_alpha()
        if frame is not None:
            image = image.subsurface(pygame.Rect(frame))
        w, h = image.get_size()
        _image_cache[key] = pygame.transform.scale(image, (w * scale, h * scale))
    return _image_cache[key]


class Background:
    """아래로 천천히 흐르는 사막 배경 + 조금 더 빨리 흐르는 구름."""

    def __init__(self):
        self.ground = load_frame(BACKGROUND_IMAGE, scale=BACKGROUND_SCALE)
        self.clouds = load_frame(CLOUDS_IMAGE, scale=BACKGROUND_SCALE)
        self.x = (WIDTH - self.ground.get_width()) // 2  # 가운데 맞춤
        self.ground_y = 0
        self.clouds_y = 0

    def update(self):
        self.ground_y = (self.ground_y + BACKGROUND_SPEED) % self.ground.get_height()
        self.clouds_y = (self.clouds_y + CLOUDS_SPEED) % (HEIGHT + self.clouds.get_height())

    def draw(self, screen):
        # 같은 그림을 위아래로 이어 붙여 끊김 없이 반복한다.
        screen.blit(self.ground, (self.x, self.ground_y))
        screen.blit(self.ground, (self.x, self.ground_y - self.ground.get_height()))
        screen.blit(self.clouds, (self.x, self.clouds_y - self.clouds.get_height()))


class Player(pygame.sprite.Sprite):
    """화면 아래쪽에서 좌우로 움직이는 플레이어 비행기."""

    def __init__(self):
        super().__init__()
        self.image = load_frame(*PLAYER_FRAME)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))

    def update(self, keys):
        """매 프레임 한 번 불린다. keys 는 pygame.key.get_pressed() 의 결과."""
        # TODO(F1): 왼쪽 방향키(keys[pygame.K_LEFT])를 누르고 있으면 PLAYER_SPEED 만큼 왼쪽으로,
        #           오른쪽 방향키(keys[pygame.K_RIGHT])면 오른쪽으로 움직이게 할 것.
        #           플레이어가 화면 왼쪽·오른쪽 끝 밖으로 나가지 않도록 위치를 제한.
        pass

    def shoot(self):
        """플레이어 위쪽 가운데에서 출발하는 총알 하나를 만들어 돌려준다."""
        # TODO(F2): Bullet(x, y) 를 작성할 것.
        #           x 는 플레이어의 가로 가운데, y 는 플레이어의 위쪽 끝이므로 참고.
        return None


class Bullet(pygame.sprite.Sprite):
    """플레이어가 쏜 총알. 위로 날아간다."""

    def __init__(self, x, y):
        super().__init__()
        self.image = load_frame(*BULLET_FRAME)
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self):
        # TODO(F2): 매 프레임 BULLET_SPEED 만큼 위로 움직이게 할 것.
        #           총알이 화면 위로 완전히 나가면 self.kill() 로 없앨 것.
        pass


class Enemy(pygame.sprite.Sprite):
    """화면 위에서 나타나 아래로 내려오는 적. 세 종류 중 하나가 무작위로 나온다."""

    def __init__(self):
        super().__init__()
        self.image = load_frame(*random.choice(ENEMY_FRAMES))
        x = random.randint(0, WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(bottomleft=(x, 0))
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)

    def update(self):
        self.rect.y += self.speed
