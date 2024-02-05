import pygame
import random

# initialize pygame
pygame.init()

# initialize pygame fonts
pygame.font.init()

# game score
playerScore = 0
scoreStatement = "score:"

# game levels
gameLevel = 1
levelStatement = "level:"

# SOUND
pygame.mixer.init()
pygame.mixer.music.load("assets/music_zapsplat_and_action_breakbeat.mp3")  # From Zapsplat
pygame.mixer.music.play(loops=-1)  # '-1' = Never ends for background music

collision_sound = pygame.mixer.Sound(
    "assets/esm_8bit_explosion_heavy_with_voice_bomb_boom_blast_cannon_retro_old_school_classic_cartoon.mp3")  # From Epic Stock on Zapsplat
shoot_sound = pygame.mixer.Sound("assets/comedy_missle_launch.mp3")  # From Zapsplat
powerup_sound = pygame.mixer.Sound(
    "assets/little_robot_sound_factory_Collect_Point_01.mp3")  # From Little Robot Sound Factory on Zapsplat
missile_powerup_sound = pygame.mixer.Sound(
    "assets/zapsplat_multimedia_game_sound_retro_digital_fifths_ascend_power_up_level_up_001_40593.mp3")  # From Zapsplat

# CONTROL KEYS
from pygame.locals import (
    RLEACCEL,
    K_SPACE,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# screen size and color values
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screenRed = 215
screenGreen = 232
screenBlue = 253

# ENEMY CLASS
enemySpeed = random.randint(10, 15)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width=75, height=25):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20,10))
        #  self.surf.fill((255,0,255))
        self.surf = pygame.image.load("assets/enemyJet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 50),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = enemySpeed

    # ENEMY MOVEMENT (KILL WHEN OFF-SCREEN)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# POWER-UP CLASS (slows enemies)
class Powerup(pygame.sprite.Sprite):
    def __init__(self, width=50, height=50):
        super(Powerup, self).__init__()
        self.surf = pygame.image.load("assets/PowerUp.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 50),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = 5

    # UPDATE SPEED FOR POWERUP
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Missile Powerup (bypasses reload mechanic)
class missilePowerup(pygame.sprite.Sprite):
    def __init__(self):
        super(missilePowerup, self).__init__()
        self.surf = pygame.image.load("assets/BulletPowerup.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 10, SCREEN_WIDTH + 50),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = 5

    # Update movement
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# PLAYER CLASS inherited from sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, width=75, height=25):
        super(Player, self).__init__()
        #  self.surf = pygame.Surface((width,height))
        #  self.surf.fill((255,255,255))
        self.surf = pygame.image.load("assets/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(0, 300)
        )
        self.power = 0
        self.missilePower = 0

    # PLAYER MOVEMENT
    def update(self, pressed_keys, speed):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)

        # KEEP PLAYER ON SCREEN
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    # FIRE MISSILES
    def fire(self):
        shoot_sound.play()
        return Missile(player.rect.width, player.rect.height)

    # PICKUP POWERUPS AND TIMER
    def getPower(self):
        self.power += 1

    # Pickup Missile powerup
    def getMissilePower(self):
        self.missilePower += 1


# MISSILE CLASS
class Missile(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("assets/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(width, height)
        )

    # MISSILE MOVEMENT
    def update(self):
        self.rect.move_ip(5, 0)
        if self.rect.x >= SCREEN_WIDTH:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets/cloud.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # randomly place clouds
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Skull(pygame.sprite.Sprite):  # Replaces clouds on level 3
    def __init__(self):
        super(Skull, self).__init__()
        self.surf = pygame.image.load("assets/Skull.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        # randomly place clouds
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# ADD ENEMIES IN INTERVALS & set spawn timer
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 300)

# cloud spawn interval
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

# skull spawn interval
ADD_SKULL = pygame.USEREVENT + 3
pygame.time.set_timer(ADD_SKULL, 1000)

# Missile recharge timer so player can't spam
MISSILE_RECHARGE = pygame.USEREVENT + 4
pygame.time.set_timer(MISSILE_RECHARGE, 1000)

# Missile Powerup spawn timer
ADD_MISSILEPOWER = pygame.USEREVENT + 5
pygame.time.set_timer(ADD_MISSILEPOWER, 20000)

# Powerup spawn timer
ADD_POWERUP = pygame.USEREVENT + 6
pygame.time.set_timer(ADD_POWERUP, 10000)

# instantiate player object
player = Player()

# Sprite groups for enemies and all sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
skulls = pygame.sprite.Group()
powerups = pygame.sprite.Group()
missilepowerups = pygame.sprite.Group()
missiles = pygame.sprite.Group()
Missilereload = []
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_group.add(player)
all_sprites.add(player)

# GAME LOOP START
# runs until event happens that makes game quit
running = True

clock = pygame.time.Clock()

while running:

    # if statement for slowing enemy speed when player is powered-up
    # decreases in power with increasing levels
    if player.power == 1 and gameLevel == 1:
        enemySpeed = 5
    elif player.power == 0 and gameLevel == 1:
        enemySpeed = random.randint(10, 15)
    if player.power == 1 and gameLevel == 2:
        enemySpeed = 8
    elif player.power == 0 and gameLevel == 2:
        enemySpeed = random.randint(13, 18)
    if player.power == 1 and gameLevel == 3:
        enemySpeed = 12
    elif player.power == 0 and gameLevel == 3:
        enemySpeed = random.randint(17, 22)

    # Show level change w/ different colors between levels
    # colors show progression of day (morning, mid-day, and afternoon)
    if playerScore < 100:  # LEVEL 1
        gameLevel = 1
    if 100 <= playerScore < 150:  # LEVEL 2
        screenRed = 159
        screenGreen = 206
        screenBlue = 250
        gameLevel = 2
    if 150 <= playerScore:  # LEVEL 3
        screenRed = 238
        screenGreen = 179
        screenBlue = 120
        gameLevel = 3

    # draw the screen
    # EVENTS
    # when user clicks exit or any game-ending event, quit the game by changing 'running' to false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # FIRE MISSILES
            elif event.key == K_SPACE and len(Missilereload) < 1 and player.missilePower == 0:
                player.fire()
                newMissile = Missile(player.rect.x + 62, player.rect.y + 18)  # Fire missiles from bottom front of jet
                missiles.add(newMissile)
                all_sprites.add(newMissile)
                Missilereload.append(newMissile)
            # FIRE CONTINUOUS MISSILES W MISSILEPOWERUP
            elif event.key == K_SPACE and player.missilePower == 1:
                player.fire()
                newMissile = Missile(player.rect.x + 62, player.rect.y + 18)
                missiles.add(newMissile)
                all_sprites.add(newMissile)
                Missilereload.append(newMissile)
        # CREATE NEW ENEMY
        elif event.type == ADD_ENEMY:
            newEnemy = Enemy()
            enemies.add(newEnemy)
            all_sprites.add(newEnemy)
        # CREATE CLOUDS
        elif event.type == ADD_CLOUD and gameLevel < 3:
            newCloud = Cloud()
            clouds.add(newCloud)
            all_sprites.add(newCloud)
        # ADD SKULLS
        elif event.type == ADD_SKULL and gameLevel > 2:
            newSkull = Skull()
            skulls.add(newSkull)
            all_sprites.add(newSkull)
        # SPAWN POWERUPS
        elif event.type == ADD_POWERUP:
            player.power = 0
            player.missilePower = 0
            newPowerup = Powerup()
            powerups.add(newPowerup)
            all_sprites.add(newPowerup)
        # SPAWN MISSILE POWERUPS
        elif event.type == ADD_MISSILEPOWER:
            newMissilePower = missilePowerup()
            missilepowerups.add(newMissilePower)
            all_sprites.add(newMissilePower)
        # RELOAD MISSILES
        elif event.type == MISSILE_RECHARGE:
            Missilereload.clear()
            # also add one point to score every second alive
            playerScore += 1

    # Get pressed keys to update movement
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, 6)  # player speed and update method
    enemies.update()
    clouds.update()
    missiles.update()  # updates missile movement
    powerups.update()
    missilepowerups.update()
    skulls.update()

    # SCREEN BACKGROUND COLOR
    screen.fill((screenRed, screenGreen, screenBlue))  # RGB 250
    # Create surface/define player
    # screen.blit(player.surf, player.rect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # SPRITE COLLISION
    if pygame.sprite.spritecollideany(player, enemies):
        collision_sound.play()
        player.kill()
        running = False
    elif pygame.sprite.groupcollide(missiles, enemies, True, True):
        collision_sound.play()
        playerScore += 5
    elif pygame.sprite.groupcollide(player_group, powerups, False, True):
        powerup_sound.play()
        player.getPower()
        playerScore += 10
    elif pygame.sprite.groupcollide(player_group, missilepowerups, False, True):
        missile_powerup_sound.play()
        player.getMissilePower()
        playerScore += 10

    # DISPLAY SCORES
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 30)

    numScore = font.render(str(playerScore), True, (0, 0, 0))
    screen.blit(numScore, (105, 5))  # 380
    strScore = font.render(scoreStatement, True, (0, 0, 0))
    screen.blit(strScore, (0, 5))  # 275

    # Display powerup effects
    slowPow = font2.render("enemies: SLOWED", True, (0, 0, 0))
    missilePow = font2.render("INFINITE MISSILES", True, (0, 0, 0))

    if player.power == 1:
        screen.blit(slowPow, (200, 0))
    if player.missilePower == 1:
        screen.blit(missilePow, (200, 20))

    # DISPLAY LEVEL
    numLevel = font.render(str(gameLevel), True, (0, 0, 0))
    screen.blit(numLevel, (780, 5))
    strLevel = font.render(levelStatement, True, (0, 0, 0))
    screen.blit(strLevel, (685, 5))

    ''' 
    surf = pygame.Surface((50,50))
    surf.fill((255,255,255))
    rect = surf.get_rect()

    #include shapes and other decor by drawing
    #pygame.draw.circle(screen,(0,0,0),(200,200),100) screen, color of circle, location, size
    screen.blit(surf, (SCREEN_WIDTH/2-surf.get_width()/2, SCREEN_HEIGHT/2-surf.get_height()/2))
    '''

    # flip display
    pygame.display.flip()
    # Define framerate
    clock.tick(60)  # END GAME LOOP

print("-----------------------------------------")
print("You ended with a score of " + str(playerScore) + "!")
print("-----------------------------------------")

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.font.quit()
pygame.quit()