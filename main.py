"""종스크롤 슈팅 게임. 실행: python main.py"""
import sys

import pygame

from settings import (
    WIDTH, HEIGHT, FPS, TITLE, HIGHSCORE_FILE,
    ENEMY_SPAWN_MS, START_LIVES, SCORE_PER_ENEMY,
    WHITE, YELLOW, RED, HUD_SHADE, GAME_OVER_SHADE,
)
from entities import Background, Player, Enemy

SPAWN_ENEMY = pygame.USEREVENT + 1  # "적을 하나 만들 때가 됐다"는 타이머 이벤트


def load_high_score():
    """HIGHSCORE_FILE 에서 최고 점수를 읽어 돌려준다."""
    # TODO(F5): 파일에서 최고 점수를 읽어 int 로 반환할 것.
    #           파일이 없거나 내용이 숫자가 아니면 0 을 반환할 것.
    return 0


def save_high_score(score):
    """최고 점수를 HIGHSCORE_FILE 에 저장한다."""
    # TODO(F5): score 를 파일에 저장할 것. (다음 실행 때 load_high_score() 로 읽을 수 있게)
    pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 72)
        pygame.time.set_timer(SPAWN_ENEMY, ENEMY_SPAWN_MS)
        self.background = Background()
        # 밝은 배경 위에서도 글자가 보이도록 깔아 줄 반투명 어두운 막
        self.hud_shade = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
        self.hud_shade.fill(HUD_SHADE)
        self.dark_shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # 시작·게임 오버 화면용
        self.dark_shade.fill(GAME_OVER_SHADE)
        self.high_score = load_high_score()
        self.running = True
        self.on_title = True  # True 면 시작 화면, SPACE 를 누르면 False 가 되며 게임 시작
        self.reset()

    def reset(self):
        """새 판을 시작한다. 스프라이트·점수·생명을 처음 상태로 되돌린다."""
        self.all_sprites = pygame.sprite.Group()  # 화면에 그릴 모든 스프라이트
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0
        self.lives = START_LIVES
        self.game_over = False

    # ---------------- 입력 ----------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.on_title:
                self.handle_title_event(event)  # 시작 화면 입력은 여기서만 처리
            elif event.type == SPAWN_ENEMY and not self.game_over:
                enemy = Enemy()
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # TODO(F2): 스페이스 키를 누르면 self.player.shoot() 으로 총알을 만들어
                #           self.bullets 와 self.all_sprites 두 그룹에 넣을 것. (게임 오버 중에는 쏘지 않게)
                # TODO(F5): 게임 오버 상태에서 R 키를 누르면 self.reset() 으로 새 판을 시작할 것.

    def handle_title_event(self, event):
        """시작 화면의 입력: SPACE 면 새 판 시작, ESC 면 종료. (적 생성·발사 없음)"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.on_title = False
                self.reset()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    # ---------------- 갱신 ----------------
    def update(self):
        if self.game_over:
            return  # 게임 오버면 화면(배경 포함)을 멈춤.

        self.background.update()
        if self.on_title:
            return  # 시작 화면에서는 배경만 흐름.

        self.player.update(pygame.key.get_pressed())
        self.bullets.update()
        self.enemies.update()

        # TODO(F3): 총알과 적이 부딪히면 둘 다 없애고, 맞힌 적 하나당 SCORE_PER_ENEMY 점을 더할 것.
        #           힌트: pygame.sprite.groupcollide

        # TODO(F4): 적이 플레이어에 닿으면 그 적을 없애고 생명(self.lives)을 1 줄일 것.
        #           힌트: pygame.sprite.spritecollide

        # 화면 아래로 지나간 적은 없앨 것.
        for enemy in list(self.enemies):
            if enemy.rect.top > HEIGHT:
                enemy.kill()
                # TODO(F4): 적이 아래로 지나갔으니 생명을 1 줄일 것.

        # TODO(F4): 생명이 0 이하가 되면 self.end_game() 을 실행할 것.

    def end_game(self):
        """게임 오버 처리."""
        self.game_over = True
        # TODO(F5): 이번 점수가 최고 점수보다 높으면 self.high_score 를 바꾸고 save_high_score() 로 저장할 것.

    # ---------------- 그리기 ----------------
    def draw_text(self, text, font, color, **position):
        """글자를 화면에 그린다. 예: self.draw_text("Hi", self.font, WHITE, center=(240, 320))"""
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(**position))

    def draw(self):
        self.background.draw(self.screen)
        if self.on_title:
            self.draw_title()
            pygame.display.flip()
            return
        self.all_sprites.draw(self.screen)
        if self.game_over:
            self.screen.blit(self.dark_shade, (0, 0))  # 게임 오버 글자가 잘 보이게
        self.screen.blit(self.hud_shade, (0, 0))  # 점수·생명 글자 뒤 어두운 띠
        self.draw_text(f"LIVES: {self.lives}", self.font, WHITE, topright=(WIDTH - 10, 10))
        # TODO(F3): 화면 왼쪽 위에 현재 점수를 "SCORE: 120" 형태로 표시할 것.
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def draw_title(self):
        """시작 화면: 게임 이름, 플레이어 그림, 조작 안내, 깜빡이는 시작 안내."""
        cx = WIDTH // 2
        self.screen.blit(self.dark_shade, (0, 0))
        self.draw_text(TITLE, self.big_font, YELLOW, center=(cx, 150))
        self.screen.blit(self.player.image, self.player.image.get_rect(center=(cx, 270)))
        controls = ("LEFT / RIGHT : Move", "SPACE : Shoot", "R : Restart", "ESC : Quit")
        for i, line in enumerate(controls):
            self.draw_text(line, self.font, WHITE, center=(cx, 370 + i * 34))
        if pygame.time.get_ticks() // 500 % 2 == 0:  # 0.5초마다 깜빡임
            self.draw_text("Press SPACE to start", self.font, YELLOW, center=(cx, 540))

    def draw_game_over(self):
        """게임 오버 화면. self.game_over 가 True 일 때 draw() 가 부른다."""
        # TODO(F4): 화면 가운데에 "GAME OVER" 와 이번 판 점수를 표시할 것.
        # TODO(F5): 최고 점수("HIGH SCORE: 300")와 재시작 안내("Press R to restart")도 표시할 것.
        pass

    # ---------------- 게임 루프 ----------------
    def step(self):
        """한 프레임: 입력 → 갱신 → 그리기."""
        self.handle_events()
        self.update()
        self.draw()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.step()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
    sys.exit()
