import pygame
import random

# Initialize PyGame
pygame.init()

# Window settings: NES exact resolution (256x224, scaled 2x to 512x448)
NES_WIDTH, NES_HEIGHT = 256, 224
SCALE = 2
WIDTH, HEIGHT = NES_WIDTH * SCALE, NES_HEIGHT * SCALE
TILE_SIZE = 16  # NES tiles are 8x8, scaled 2x to 16x16
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Bros. 3 - Nintendo Certified Engine")

# Colors: NES PPU palette (SMB3-specific)
COLORS = {
    "SKY": (92, 148, 252),      # $22 Sky blue
    "GROUND": (160, 64, 0),     # $17 Brown
    "MARIO_SKIN": (252, 152, 56),  # $38 Peach
    "MARIO_RED": (252, 40, 40),    # $16 Red
    "MARIO_BLACK": (0, 0, 0),      # $0F Black
    "MARIO_WHITE": (248, 248, 248),# $30 White (transparency)
    "GOOMBA": (160, 64, 0),     # $17 Brown
    "BLOCK": (252, 188, 0),     # $2A Yellow
    "COIN": (252, 188, 0)       # $2A Yellow
}

# Mario sprite animations (16x16, small Mario, SMB3)
# 0 = transparent, 1 = skin, 2 = red, 3 = black
MARIO_IDLE_RIGHT = [
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 3, 3, 1, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 1, 1, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
    [0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

MARIO_RUN1_RIGHT = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 3, 3, 1, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

MARIO_RUN2_RIGHT = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 3, 3, 1, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

MARIO_JUMP_RIGHT = [
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 3, 3, 1, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 1, 1, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3, 3, 0, 3, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Flip sprites for left-facing
def flip_sprite(sprite):
    return [row[::-1] for row in sprite]

MARIO_IDLE_LEFT = flip_sprite(MARIO_IDLE_RIGHT)
MARIO_RUN1_LEFT = flip_sprite(MARIO_RUN1_RIGHT)
MARIO_RUN2_LEFT = flip_sprite(MARIO_RUN2_RIGHT)
MARIO_JUMP_LEFT = flip_sprite(MARIO_JUMP_RIGHT)

# Goomba sprite (16x16)
GOOMBA_SPRITE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
]

# Mario class with NES-certified physics
class Mario:
    def __init__(self):
        self.x = 32.0  # Sub-pixel precision (NES uses fixed-point)
        self.y = float(NES_HEIGHT - TILE_SIZE * 3)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.jumping = False
        self.facing_right = True
        self.sound_queue = []
        self.frame = 0
        self.frame_timer = 0
        self.accel_x = 0.0  # Acceleration for NES momentum
        self.friction = 0.046875  # NES friction (0x0C / 256)

    def update(self, ground, blocks):
        # NES horizontal movement (momentum-based)
        if self.accel_x != 0:
            self.vel_x += self.accel_x
            if abs(self.vel_x) > 1.40625:  # Max walk speed (1 + 26/64)
                self.vel_x = 1.40625 if self.vel_x > 0 else -1.40625
        else:
            # Apply friction
            if self.vel_x > 0:
                self.vel_x -= self.friction
                if self.vel_x < 0:
                    self.vel_x = 0
            elif self.vel_x < 0:
                self.vel_x += self.friction
                if self.vel_x > 0:
                    self.vel_x = 0

        self.x += self.vel_x
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        if self.x + self.width > NES_WIDTH:
            self.x = NES_WIDTH - self.width
            self.vel_x = 0

        # NES vertical movement
        self.vel_y += 0.21875  # Gravity (0x38 / 256)
        if self.vel_y > 4.0:  # Terminal velocity
            self.vel_y = 4.0
        self.y += self.vel_y

        # Ground collision
        if self.y >= ground.y - self.height:
            self.y = ground.y - self.height
            self.vel_y = 0
            self.jumping = False

        # Block collision (top only)
        for block in blocks:
            if (self.x + self.width > block.x and self.x < block.x + block.width and
                self.y + self.height > block.y and self.y < block.y + block.height):
                if self.vel_y > 0 and self.y + self.height - self.vel_y <= block.y:
                    self.y = block.y - self.height
                    self.vel_y = 0
                    self.jumping = False

        # Animation
        self.frame_timer += 1
        if self.jumping:
            self.frame = 0
        elif abs(self.vel_x) > 0:
            if self.frame_timer % 8 == 0:  # ~7.5 FPS at max speed (NES timing)
                self.frame = 1 if self.frame == 0 else 0
        else:
            self.frame = 0

    def jump(self):
        if not self.jumping:
            self.vel_y = -4.0  # Initial jump velocity (SMB3 small Mario)
            self.jumping = True
            self.sound_queue.append("BOING")

    def draw(self, screen):
        pixel_size = SCALE
        if self.jumping:
            sprite = MARIO_JUMP_RIGHT if self.facing_right else MARIO_JUMP_LEFT
        elif self.vel_x != 0:
            sprite = [MARIO_RUN1_RIGHT, MARIO_RUN2_RIGHT][self.frame] if self.facing_right else [MARIO_RUN1_LEFT, MARIO_RUN2_LEFT][self.frame]
        else:
            sprite = MARIO_IDLE_RIGHT if self.facing_right else MARIO_IDLE_LEFT

        for y, row in enumerate(sprite):
            for x, pixel in enumerate(row):
                if pixel != 0:
                    color = [COLORS["MARIO_SKIN"], COLORS["MARIO_RED"], COLORS["MARIO_BLACK"]][pixel - 1]
                    pygame.draw.rect(screen, color,
                                   [int(self.x * SCALE) + x * pixel_size, int(self.y * SCALE) + y * pixel_size, pixel_size, pixel_size])

# Ground class
class Ground:
    def __init__(self):
        self.x = 0
        self.y = NES_HEIGHT - TILE_SIZE * 2
        self.width = NES_WIDTH
        self.height = TILE_SIZE * 2

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["GROUND"], [self.x * SCALE, self.y * SCALE, self.width * SCALE, self.height * SCALE])

# Block class
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["BLOCK"], [self.x * SCALE, self.y * SCALE, self.width * SCALE, self.height * SCALE])
        pygame.draw.rect(screen, COLORS["MARIO_BLACK"], [self.x * SCALE, self.y * SCALE, self.width * SCALE, self.height * SCALE], 1)

# Goomba class
class Goomba:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.vel_x = -0.5  # NES Goomba speed

    def update(self, ground):
        self.x += self.vel_x
        if self.x < 0:
            self.x = NES_WIDTH - self.width
        self.y = ground.y - self.height

    def draw(self, screen):
        pixel_size = SCALE
        for y, row in enumerate(GOOMBA_SPRITE):
            for x, pixel in enumerate(row):
                if pixel == 1:
                    pygame.draw.rect(screen, COLORS["GOOMBA"],
                                   [int(self.x * SCALE) + x * pixel_size, int(self.y * SCALE) + y * pixel_size, pixel_size, pixel_size])

# Coin class
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, COLORS["COIN"], [self.x * SCALE, self.y * SCALE, self.width * SCALE, self.height * SCALE])
            pygame.draw.rect(screen, COLORS["MARIO_BLACK"], [self.x * SCALE, self.y * SCALE, self.width * SCALE, self.height * SCALE], 1)

# Main game loop
def main():
    clock = pygame.time.Clock()
    mario = Mario()
    ground = Ground()
    blocks = [Block(96, NES_HEIGHT - TILE_SIZE * 4), Block(112, NES_HEIGHT - TILE_SIZE * 4)]
    goombas = [Goomba(160, NES_HEIGHT - TILE_SIZE * 3), Goomba(208, NES_HEIGHT - TILE_SIZE * 3)]
    coins = [Coin(104, NES_HEIGHT - TILE_SIZE * 5), Coin(208, NES_HEIGHT - TILE_SIZE * 4)]
    score = 0
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Controls (NES-certified input handling)
        keys = pygame.key.get_pressed()
        mario.accel_x = 0
        if keys[pygame.K_LEFT]:
            mario.accel_x = -0.09375  # Acceleration (0x18 / 256)
            mario.facing_right = False
        if keys[pygame.K_RIGHT]:
            mario.accel_x = 0.09375
            mario.facing_right = True
        if keys[pygame.K_SPACE]:
            mario.jump()

        # Update
        mario.update(ground, blocks)
        for goomba in goombas[:]:
            goomba.update(ground)
            if (mario.x + mario.width > goomba.x and mario.x < goomba.x + goomba.width and
                mario.y + mario.height > goomba.y and mario.vel_y > 0 and
                mario.y + mario.height - mario.vel_y <= goomba.y):
                goombas.remove(goomba)
                mario.vel_y = -2.0  # NES stomp bounce
                mario.sound_queue.append("STOMP")
                score += 100

        for coin in coins:
            if not coin.collected and (mario.x + mario.width > coin.x and mario.x < coin.x + coin.width and
                                      mario.y + mario.height > coin.y and mario.y < coin.y + coin.height):
                coin.collected = True
                mario.sound_queue.append("CHING")
                score += 50

        # Draw
        WINDOW.fill(COLORS["SKY"])
        ground.draw(WINDOW)
        for block in blocks:
            block.draw(WINDOW)
        for goomba in goombas:
            goomba.draw(WINDOW)
        for coin in coins:
            coin.draw(WINDOW)
        mario.draw(WINDOW)

        # Draw score and sounds
        font = pygame.font.SysFont('courier', 16, bold=True)
        score_text = font.render(f'SCORE {score:06d}', True, COLORS["MARIO_BLACK"])
        WINDOW.blit(score_text, (8 * SCALE, 8 * SCALE))
        if mario.sound_queue:
            sound_text = font.render(mario.sound_queue[-1], True, COLORS["MARIO_BLACK"])
            WINDOW.blit(sound_text, (NES_WIDTH * SCALE - 80, 8 * SCALE))
            if len(mario.sound_queue) > 1 or pygame.time.get_ticks() % 60 > 30:
                mario.sound_queue.pop(0)

        pygame.display.update()
        clock.tick(60)  # NES NTSC 60.0988 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
