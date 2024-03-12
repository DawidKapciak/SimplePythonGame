import pygame
import random
import sys
import math

__author__ = "Dawid Kapciak"
# Inicjalizacja Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("JPWMII - Projekt")

# Ustawienia muzyki
pygame.mixer.music.load("resources/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
hurt_sound = pygame.mixer.Sound("resources/hurt.wav")
hurt_sound.set_volume(0.1)
game_over_sound = pygame.mixer.Sound("resources/game_over.wav")
game_over_sound.set_volume(0.1)

# Ustawienia gry
WIDTH, HEIGHT = 1600, 900
FPS = 60
RED = (255, 0, 0)
ENEMY_SPEED = 7
PLAYER_SPEED = 5
BULLET_RADIUS = 20
BULLET_SPEED = 7
ENEMY_SPAWN_INTERVAL_SECONDS = 1
PLAYER_HEALTH = 20
ENEMY_DAMAGE = 5
EXP = 0
MAX_EXP = 100
LEVEL = 1
DIFFICULTY = 10

# Inicjalizacja okna gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Załaduj sprite z pliku sprite.png
sprite_sheet = pygame.image.load("resources/sprite.png")

# Inicjalizacja chmury
cloud_img = pygame.image.load("resources/cloud.png")

# Inicjalizacja mapy
map_img = pygame.image.load("resources/map.png")

# Inicjalizacja broni
tear_img = sprite_sheet.subsurface(pygame.Rect(110, 408, 32, 29))
bloody_tear_img = sprite_sheet.subsurface(pygame.Rect(111, 271, 29, 29))
blessed_tear_img = sprite_sheet.subsurface(pygame.Rect(112, 315, 23, 34))
spectral_tear_img = sprite_sheet.subsurface(pygame.Rect(111, 364, 28, 28))
huge_tear_img = sprite_sheet.subsurface(pygame.Rect(22, 322, 56, 55))
weapon_images = [
    tear_img,
    blessed_tear_img,
    bloody_tear_img,
    huge_tear_img,
    spectral_tear_img,
]

# Inicjalizacja skrzynek
chest_img = sprite_sheet.subsurface(pygame.Rect(233, 397, 49, 40))

# Inicjalizacja potworów
enemy_img = [
    sprite_sheet.subsurface(pygame.Rect(301, 276, 49, 55)),
    sprite_sheet.subsurface(pygame.Rect(22, 391, 50, 63)),
    sprite_sheet.subsurface(pygame.Rect(169, 315, 40, 47)),
    sprite_sheet.subsurface(pygame.Rect(233, 317, 57, 61)),
    sprite_sheet.subsurface(pygame.Rect(155, 376, 69, 32)),
]

# Inicjalizacja gracza
player_frames = {
    "up": [
        sprite_sheet.subsurface(pygame.Rect(30, 126, 48, 55)),
        sprite_sheet.subsurface(pygame.Rect(86, 123, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(146, 126, 47, 55)),
        sprite_sheet.subsurface(pygame.Rect(201, 127, 47, 58)),
        sprite_sheet.subsurface(pygame.Rect(255, 126, 49, 57)),
        sprite_sheet.subsurface(pygame.Rect(313, 126, 48, 56)),
        sprite_sheet.subsurface(pygame.Rect(369, 127, 47, 54)),
        sprite_sheet.subsurface(pygame.Rect(423, 126, 49, 56)),
        sprite_sheet.subsurface(pygame.Rect(482, 127, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(537, 125, 49, 58)),
    ],
    "down": [
        sprite_sheet.subsurface(pygame.Rect(537, 125, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(482, 127, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(423, 126, 49, 56)),
        sprite_sheet.subsurface(pygame.Rect(369, 127, 47, 54)),
        sprite_sheet.subsurface(pygame.Rect(313, 126, 48, 56)),
        sprite_sheet.subsurface(pygame.Rect(255, 126, 49, 57)),
        sprite_sheet.subsurface(pygame.Rect(201, 127, 47, 58)),
        sprite_sheet.subsurface(pygame.Rect(146, 126, 47, 55)),
        sprite_sheet.subsurface(pygame.Rect(86, 123, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(30, 126, 48, 55)),
    ],
    "left": [
        sprite_sheet.subsurface(pygame.Rect(537, 49, 49, 56)),
        sprite_sheet.subsurface(pygame.Rect(481, 47, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(425, 47, 48, 58)),
        sprite_sheet.subsurface(pygame.Rect(369, 47, 48, 58)),
        sprite_sheet.subsurface(pygame.Rect(313, 47, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(257, 47, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(200, 47, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(144, 47, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(86, 47, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(30, 47, 49, 57)),
    ],
    "right": [
        sprite_sheet.subsurface(pygame.Rect(31, 202, 49, 56)),
        sprite_sheet.subsurface(pygame.Rect(87, 200, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(143, 200, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(200, 200, 48, 58)),
        sprite_sheet.subsurface(pygame.Rect(256, 200, 48, 58)),
        sprite_sheet.subsurface(pygame.Rect(311, 200, 49, 57)),
        sprite_sheet.subsurface(pygame.Rect(367, 200, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(423, 200, 49, 58)),
        sprite_sheet.subsurface(pygame.Rect(481, 201, 49, 57)),
        sprite_sheet.subsurface(pygame.Rect(538, 200, 48, 57)),
    ],
    "idle": [sprite_sheet.subsurface(pygame.Rect(313, 126, 47, 56))],
}

# Inicjalizacja serduszka
heart_img = pygame.transform.rotozoom(sprite_sheet.subsurface(pygame.Rect(182, 417, 17, 16)), 0, 2)


def spawn_enemy():
    rand = random.randint(0, len(enemy_img) - 1)
    enemy_rect = enemy_img[rand].get_rect()
    enemy_rect.x = random.randint(0, WIDTH - enemy_rect.width)
    enemy_rect.y = random.randint(-100, -50)
    enemies.append({"rect": enemy_rect, "speed": ENEMY_SPEED, "index": rand})


def spawn_heart(x, y):
    heart_rect = heart_img.get_rect()
    heart_rect.x = x
    heart_rect.y = y
    hearts.append({"rect": heart_rect})


def spawn_chest(x, y):
    chest_rect = chest_img.get_rect()
    chest_rect.x = x
    chest_rect.y = y
    chests.append({"rect": chest_rect, "opened": False})


def get_weapon_stats(weapon_level):
    if weapon_level == 0:
        return {"bullet_speed": 10, "damage": 10, "fire_rate": 2, "range": 200}
    elif weapon_level == 1:
        return {"bullet_speed": 12, "damage": 15, "fire_rate": 3, "range": 250}
    elif weapon_level == 2:
        return {"bullet_speed": 15, "damage": 20, "fire_rate": 4, "range": 300}
    elif weapon_level == 3:
        return {"bullet_speed": 17, "damage": 25, "fire_rate": 5, "range": 325}
    elif weapon_level == 4:
        return {"bullet_speed": 20, "damage": 30, "fire_rate": 6, "range": 350}


def game_over_screen():
    screen.fill((255, 255, 255))
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    game_over_text = font_large.render("Game Over", True, RED)
    score_text = font_small.render(f"Your Score: {score}", True, RED)
    timer_text = font_small.render(f"Your Time: {time}", True, RED)

    screen.blit(
        game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4)
    )
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Wyświetlanie wyników i zdrowia gracza
def draw_stats(time):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, RED)
    health_text = font.render(f"Health: {player_health}", True, RED)
    timer_text = font.render(f"Time: {time} seconds", True, RED)
    exp_text = font.render(f"EXP: {EXP}/{MAX_EXP}", True, RED)

    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(exp_text, (10, 90))
    screen.blit(timer_text, (700, 10))
    return health_text.get_width()


def draw_heart(health_text_width):
    health_text_position = (10, 50)
    heart_position = (
        health_text_position[0] + health_text_width + 15,
        health_text_position[1],
    )

    pygame.draw.polygon(
        screen,
        RED,
        [
            (heart_position[0], heart_position[1] + 7.5),
            (heart_position[0] + 5, heart_position[1]),
            (heart_position[0] + 10, heart_position[1] + 7.5),
        ],
    )
    pygame.draw.polygon(
        screen,
        RED,
        [
            (heart_position[0], heart_position[1] + 7.5),
            (heart_position[0] - 5, heart_position[1]),
            (heart_position[0] - 10, heart_position[1] + 7.5),
        ],
    )
    pygame.draw.polygon(
        screen,
        RED,
        [
            (heart_position[0] - 10, heart_position[1] + 7.5),
            (heart_position[0] + 10, heart_position[1] + 7.5),
            (heart_position[0], heart_position[1] + 20),
        ],
    )


def blitRotate(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)


def walk_animation(index, counter):
    # global player_index, player_animation_counter, player_img
    if current_direction != "idle":
        counter += 1
        if counter >= 5:
            index = (index + 1) % len(player_frames[current_direction])
            counter = 0

        # Sprawdź, czy indeks animacji mieści się w zakresie
        if index < len(player_frames[current_direction]):
            img = player_frames[current_direction][index]
        else:
            # Jeśli indeks przekracza zakres, ustaw na pierwszą klatkę animacji
            index = 0
            img = player_frames[current_direction][index]
    else:
        index = 0
        img = player_frames[current_direction][0]

    return index, counter, img


# Inicjalizacja zmiennych
clock = pygame.time.Clock()
score = 0
attack_cooldown = 0
enemy_spawn_timer = (ENEMY_SPAWN_INTERVAL_SECONDS * FPS)
player_health = PLAYER_HEALTH
start_time = pygame.time.get_ticks()
player_bullets = []
bullets_to_remove = []
game_over = False
upgrade_lvl = 0
time_temp = 0
rotation = 0
chests = []
current_direction = "idle"
player_index = 0
player_img = player_frames[current_direction][player_index]
player_rect = player_img.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 2)
player_animation_counter = 0
invulnerability_duration = 0
player_weapon_rect = weapon_images[0].get_rect(center=(WIDTH // 2, HEIGHT - 50))
map_rotation = 0
map_frames = 30
hearts = []
enemies = []
frame_change_counter = 10 * FPS
cloud_rect = cloud_img.get_rect()
cloud_rect.x = WIDTH  # Początkowa pozycja chmury (prawa krawędź ekranu)
cloud_speed = 3
movement_duration = 10 * FPS  # 10 sekund
movement_counter = movement_duration
reverse = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if player_rect.x - PLAYER_SPEED > 0:
            player_rect.x -= PLAYER_SPEED
        current_direction = "left"

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if player_rect.x + PLAYER_SPEED < WIDTH - player_rect.width:
            player_rect.x += PLAYER_SPEED
        current_direction = "right"

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if player_rect.y - PLAYER_SPEED > 0:
            player_rect.y -= PLAYER_SPEED
        current_direction = "up"

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if player_rect.y + PLAYER_SPEED < HEIGHT - player_rect.height:
            player_rect.y += PLAYER_SPEED
        current_direction = "down"

    if not any(
            (
                    keys[pygame.K_LEFT],
                    keys[pygame.K_a],
                    keys[pygame.K_RIGHT],
                    keys[pygame.K_d],
                    keys[pygame.K_UP],
                    keys[pygame.K_w],
                    keys[pygame.K_DOWN],
                    keys[pygame.K_s],
            )
    ):
        current_direction = "idle"

    # Aktualizacja animacji chodzenia
    player_index, player_animation_counter, player_img = walk_animation(player_index, player_animation_counter)

    # Rotacja mapy / animacja tła
    rotated_image = pygame.transform.rotate(map_img, map_rotation * 0.2)
    new_rect = rotated_image.get_rect(center=map_img.get_rect(topleft=(-160, -140)).center)
    screen.blit(rotated_image, new_rect.topleft)

    if reverse:
        if map_rotation <= 0:
            reverse = False
        map_rotation -= 1
    elif map_rotation >= map_frames:
        reverse = True
    else:
        map_rotation += 1

    for heart in hearts:
        pos = (heart["rect"][0], heart["rect"][1])
        blitRotate(screen, heart_img, pos, rotation)
    rotation += 1

    # Sprawdzanie kolizji serduszko-gracz
    for heart in hearts.copy():
        if player_rect.colliderect(heart["rect"]):
            if player_health < PLAYER_HEALTH:
                player_health += 10
                hearts.remove(heart)
                if player_health > PLAYER_HEALTH:
                    player_health = PLAYER_HEALTH

    # ENEMIES
    # Ograniczenie pojawiania się przeciwników
    if enemy_spawn_timer <= 0:
        spawn_enemy()
        enemy_spawn_timer = ENEMY_SPAWN_INTERVAL_SECONDS * FPS  # Resetujemy timer
    else:
        enemy_spawn_timer -= 1

    for enemy in enemies:
        screen.blit(enemy_img[enemy["index"]], enemy["rect"])

    # Poruszanie potworów w kierunku gracza
    for enemy in enemies:
        dx = player_rect.x - enemy["rect"].x
        dy = player_rect.y - enemy["rect"].y
        angle = math.atan2(dy, dx)
        enemy["rect"].x += math.cos(angle) * enemy["speed"]
        enemy["rect"].y += math.sin(angle) * enemy["speed"]

    # Sprawdzanie kolizji przeciwnik-gracz
    for enemy in enemies.copy():
        if player_rect.colliderect(enemy["rect"]) and invulnerability_duration <= 0:
            player_health -= ENEMY_DAMAGE
            invulnerability_duration = FPS // 2
            hurt_sound.play()

        # Aktualizacja czasu nieśmiertelności
        if invulnerability_duration > 0:
            invulnerability_duration -= 1

    if player_health > 0:
        screen.blit(player_frames[current_direction][player_index], player_rect)
    else:
        game_over_sound.play()
        game_over_screen()

    # Aktualizacja pozycji strzałów
    for bullet in player_bullets.copy():
        bullet["rect"].x += bullet["speed"] * math.cos(bullet["angle"])
        bullet["rect"].y += bullet["speed"] * math.sin(bullet["angle"])

        if (
                bullet["rect"].y < 0
                or bullet["rect"].y > HEIGHT
                or bullet["rect"].x < 0
                or bullet["rect"].x > WIDTH
        ):
            bullets_to_remove.append(bullet)

    # Usuń strzały poza obszarem gry
    for bullet in bullets_to_remove:
        try:
            player_bullets.remove(bullet)
        except Exception:
            pass

    # Rysowanie strzałów
    for bullet in player_bullets:
        tear_rect = pygame.Rect(
            int(bullet["rect"].x - BULLET_RADIUS),
            int(bullet["rect"].y - BULLET_RADIUS),
            BULLET_RADIUS * 2,
            BULLET_RADIUS * 2,
        )
        screen.blit(
            pygame.transform.scale(
                weapon_images[upgrade_lvl], (tear_rect.width, tear_rect.height)
            ),
            tear_rect,
        )

    # Obsługa strzałów
    if attack_cooldown <= 0:
        weapon_stats = get_weapon_stats(upgrade_lvl)
        for enemy in enemies:

            distance_to_enemy = math.hypot(
                enemy["rect"].centerx - player_rect.centerx,
                enemy["rect"].centery - player_rect.centery,
            )
            if distance_to_enemy <= get_weapon_stats(upgrade_lvl)["range"]:
                weapon_stats = get_weapon_stats(upgrade_lvl)
                player_bullets.append(
                    {
                        "rect": pygame.Rect(
                            player_rect.centerx - BULLET_RADIUS,
                            player_rect.centery - BULLET_RADIUS,
                            BULLET_RADIUS,
                            BULLET_RADIUS,
                        ),
                        "speed": weapon_stats["bullet_speed"],
                        "angle": math.atan2(
                            enemy["rect"].centery - player_rect.centery,
                            enemy["rect"].centerx - player_rect.centerx,
                        ),
                        "damage": weapon_stats["damage"],
                    }
                )
        attack_cooldown = (
                FPS // weapon_stats["fire_rate"]
        )
    else:
        attack_cooldown -= 1

    # Sprawdzanie kolizji strzał-przeciwnik
    bullets_to_remove = []
    for bullet in player_bullets:
        for enemy in enemies.copy():
            if bullet["rect"].colliderect(enemy["rect"]):
                bullets_to_remove.append(bullet)
                enemies.remove(enemy)
                score += 10
                if EXP < MAX_EXP:
                    EXP += 5
                else:
                    spawn_chest(enemy["rect"].x, enemy["rect"].y)
                    EXP = 0
                if random.randint(1, 100) <= 5:
                    spawn_heart(enemy["rect"].x, enemy["rect"].y)

    for chest in chests:
        if not chest["opened"]:
            screen.blit(chest_img, chest["rect"])

    # Sprawdzanie kolizji gracz-skrzynka
    for chest in chests.copy():
        if player_rect.colliderect(chest["rect"]) and not chest["opened"]:
            chest["opened"] = True
            if upgrade_lvl < 4:
                upgrade_lvl += 1
            else:
                score += 1000

    time = int((pygame.time.get_ticks() - start_time) / 1000)
    health_text_width = draw_stats(time)
    draw_heart(health_text_width)

    # Ruch chmury
    if movement_counter > -400:
        cloud_rect.x -= cloud_speed
        movement_counter -= 1
    else:
        cloud_rect.y = random.randint(0, HEIGHT)
        cloud_rect.x = WIDTH
        movement_counter = movement_duration
    screen.blit(cloud_img, cloud_rect)

    screen.blit(weapon_images[upgrade_lvl], player_weapon_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Aktualizacja poziomu
    time_temp += 1 / FPS
    if time_temp >= DIFFICULTY:
        ENEMY_SPEED += 1
        if ENEMY_SPAWN_INTERVAL_SECONDS > 0:
            ENEMY_SPAWN_INTERVAL_SECONDS -= 0.1
        time_temp = 0

    clock.tick(FPS)
