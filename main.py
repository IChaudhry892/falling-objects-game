import pygame
import random

pygame.init()
pygame.display.set_caption("Dylan Game")

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the player, background, and falling object images
player_image = pygame.image.load("dylan.png")
background_image = pygame.image.load("green-hill-zone.png")
ring_image = pygame.image.load('ring.png')
sonic_image = pygame.image.load("sonic.png")
silver_image = pygame.image.load("silver.png") # its no use sound effect
officer_earl_image = pygame.image.load("officer_earl.png") # police siren or gunshot sound effect

# Load the sound effects
ringSound = pygame.mixer.Sound('ring.wav')
silverSound = pygame.mixer.Sound('itsnouse.wav')
sonicSound = pygame.mixer.Sound('sonic.wav')
gunshotSound = pygame.mixer.Sound('gunshot.wav')
gameOverSound = pygame.mixer.Sound('shutup.wav')

# Player properties
# player = pygame.Rect((300, 250, 50, 50)) #(x, y, width, height)
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5

    def draw(self, screen):
        screen.blit(player_image, (dylan.x, dylan.y, dylan.width, dylan.height)) #Draw the player image on the screen

# player_width, player_height = 125, 153
# player_x = SCREEN_WIDTH // 2 - player_width // 2
# player_y = SCREEN_HEIGHT - player_height
# player_speed = 5

# Object properties
class fallingObject(object):
    def __init__(self, x, y, velocity, image, sound, point_value, lives_value):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.velocity = velocity
        self.image = image
        self.sound = sound
        self.point_value = point_value #Different point values for different falling objects
        self.lives_value = lives_value

    def fall(self):
        self.y += self.velocity #moves object down

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y)) #draws object to screen

    def checkCollision(self, player):
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y):
            self.sound.play()
            return True
        return False

# Game variables
dylan = player(338, 447, 125, 153)
falling_objects = []
game_over = False
running = True
lives = 3
score = 0
clock = pygame.time.Clock()
game_over_sound_played = False # if the game over sound has been played, don't play it agian

def resetGame(): #reset the game to play again if game_over is true
    global lives, score, falling_objects, game_over, game_over_sound_played
    # Reset the lives, score, falling_objects, and dylan's position to how they were initially
    lives = 3
    score = 0
    falling_objects = []
    game_over = False
    game_over_sound_played = False # reset sound flag
    dylan.x = 338
    dylan.y = 447

def redrawGameWindow():
    screen.blit(background_image, (0,0)) #Draw the background image
    # screen.blit(player_image, (dylan.x, dylan.y, dylan.width, dylan.height))
    dylan.draw(screen) #Draw the player
    for obj in falling_objects:
        obj.draw(screen)  # Draw each falling object

    #Display score and lives
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    screen.blit(lives_text, (10, 50))

    #Display game over message if game_over is true
    if game_over:
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        retry_text = font.render("Press R to Retry", True, (255, 255, 255))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()

# Main game loop
while running:

    # Fills screen with black after character moves in last frame
    # screen.fill((0, 0, 0))

    # Draw player
    # pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))
    # Draw player using loaded image
    # screen.blit(player_image, (player_x, player_y, player_width, player_height))

    # Game over check if lives <= 0
    # if lives <= 0:
    #     font = pygame.font.SysFont(None, 72)
    #     game_over_text = font.render("Game Over", True, (255, 0, 0))
    #     screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
    #     gameOverSound.play()
    #     pygame.display.update()
    #     pygame.time.delay(2000)  # Wait 2 seconds to show the Game Over screen
    #     running = False  # Exit the game loop

    # Check if game is over
    if lives <= 0:
        game_over = True
        if not game_over_sound_played:
            gameOverSound.play()
            game_over_sound_played = True

    if game_over:
        # Freezes game until user presses 'r' or closes the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the user closes the window
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: # if the user presses 'r'
                resetGame()
        redrawGameWindow() # shows the game over screen
        clock.tick(60)
        continue # skip the rest of the loop if game over

    # Controls
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and dylan.x > 0: # (x, y)
        # player.move_ip(-1, 0) # Player moves left
        dylan.x -= dylan.velocity
    if key[pygame.K_RIGHT] and dylan.x < SCREEN_WIDTH - dylan.width:
        # player.move_ip(1, 0) # Player moves right
        dylan.x += dylan.velocity
    if key[pygame.K_DOWN] and dylan.y < SCREEN_HEIGHT - dylan.height:
        # player.move_ip(0, 1) # Player moves down
        dylan.y += dylan.velocity
    if key[pygame.K_UP] and dylan.y > 0:
        # player.move_ip(0, -1) # Player moves up
        dylan.y -= dylan.velocity

    # Spawning the falling objects
    # Canes Object
    # if random.randint(1, 60) == 1:  # Adjust frequency as needed, object has a 1/60 chance of spawning every frame
    #     x_pos = random.randint(0, SCREEN_WIDTH - 70)  # Random horizontal position
    #     # fallSpeed = random.randint(2, 4)  # Random fall speed
    #     fallSpeed = 3 # constant fall speed
    #     falling_objects.append(fallingObject(x_pos, 0, fallSpeed, canes_image, monkeySound, 1, 0)) # adds a canes object to falling_objects

    # Ring Object
    if random.randint(1, 60) == 1:  # Adjust frequency as needed, object has a 1/60 chance of spawning every frame
        x_pos = random.randint(0, SCREEN_WIDTH - 70)  # Random horizontal position
        # fallSpeed = random.randint(2, 4)  # Random fall speed
        fallSpeed = 3 # constant fall speed
        falling_objects.append(fallingObject(x_pos, 0, fallSpeed, ring_image, ringSound, 1, 0)) # adds a canes object to falling_objects

    # Sonic Object
    if random.randint(1, 600) == 1:  # Adjust frequency as needed
        x_pos = random.randint(0, SCREEN_WIDTH - 70)  # Random horizontal position
        # fallSpeed = random.randint(3, 5)  # Random fall speed
        fallSpeed = 7 # constant fall speed
        falling_objects.append(fallingObject(x_pos, 0, fallSpeed, sonic_image, sonicSound, 0, 1)) # adds a sonic object to falling_objects

    # Silver Object
    if random.randint(1, 60) == 1:
        x_pos = random.randint(0, SCREEN_WIDTH - 70)
        fallSpeed = 5
        falling_objects.append(fallingObject(x_pos, 0, fallSpeed, silver_image, silverSound, 0, -1))

    # Officer Earl Object
    if random.randint(1, 600) == 1:
        x_pos = random.randint(0, SCREEN_WIDTH - 70)
        fallSpeed = 5
        falling_objects.append(fallingObject(x_pos, 0, fallSpeed, officer_earl_image, gunshotSound, 0, 0))

    # Updating the falling objects
    for obj in falling_objects[:]:
        obj.fall()
        if obj.checkCollision(dylan):
            score += obj.point_value  # Increase score if player catches the object, points depend on object type
            lives += obj.lives_value
            if (obj.image == officer_earl_image):
                lives = 0
            falling_objects.remove(obj)  # Remove object after being caught
        elif obj.y > SCREEN_HEIGHT:
            falling_objects.remove(obj)  # Remove object if it goes off screen

    # Event handler, pygame.Quit means user closed the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.display.update()
    redrawGameWindow()
    clock.tick(60)

pygame.quit()