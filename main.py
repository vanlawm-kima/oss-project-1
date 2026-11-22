"""종스크롤 슈팅 게임. 실행: python main.py"""
import sys

import pygame

from settings import (
    WIDTH, HEIGHT, FPS, TITLE, HIGHSCORE_FILE,
    ENEMY_SPAWN_MS, START_LIVES, SCORE_PER_ENEMY,
    WHITE, YELLOW, RED, HUD_SHADE, GAME_OVER_SHADE,
)
from entities import Background, Player, Bullet,Enemy

SPAWN_ENEMY = pygame.USEREVENT + 1  # "적을 하나 만들 때가 됐다"는 타이머 이벤트


def load_high_score():
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as file:
        file.write(str(score))


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
                elif event.key == pygame.K_SPACE and not self.game_over:
                    bullet = self.player.shoot()
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    self.reset()
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
            return

        self.background.update()

        if self.on_title:
            return

        self.player.update(pygame.key.get_pressed())
        self.bullets.update()
        self.enemies.update()

    # F3: Bullet-enemy collision and scoring
        hits = pygame.sprite.groupcollide(
            self.bullets,
            self.enemies,
            True,
            True
        )

        self.score += len(hits) * SCORE_PER_ENEMY

    # F4: Enemy hits the player
        hits = pygame.sprite.spritecollide(
            self.player,
            self.enemies,
            True
        )

        self.lives -= len(hits)

    # F4: Enemy passes the bottom
        for enemy in list(self.enemies):
            if enemy.rect.top > HEIGHT:
                enemy.kill()
                self.lives -= 1

    # F4: Game over
        if self.lives <= 0:
            self.end_game()


    def end_game(self):
        """게임 오버 처리."""
        self.game_over = True

        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

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
        self.draw_text(
            f"SCORE: {self.score}",
            self.font,
            WHITE,
            topleft=(10, 10)
        )
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
        """게임 오버 화면."""

        self.draw_text(
            "GAME OVER",
            self.big_font,
            RED,
            center=(WIDTH // 2, HEIGHT // 2 - 80)
        )

        self.draw_text(
            f"FINAL SCORE: {self.score}",
            self.font,
            WHITE,
            center=(WIDTH // 2, HEIGHT // 2 - 10)
        )

        self.draw_text(
            f"HIGH SCORE: {self.high_score}",
            self.font,
            YELLOW,
            center=(WIDTH // 2, HEIGHT // 2 + 35)
        )

        self.draw_text(
            "PRESS R TO RESTART",
            self.font,
            WHITE,
            center=(WIDTH // 2, HEIGHT // 2 + 100)
        )

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

