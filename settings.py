import pygame  # Import the pygame library
import random  # Import the random library

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
# Ground height for the dinosaur game
GROUND_HEIGHT = 500

# Dimensions and position of the game box
BOX_WIDTH = 400
BOX_HEIGHT = 300
BOX_X = BOX_WIDTH // 2
BOX_Y = BOX_HEIGHT // 2

# Initialize the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FNAF FAN GAME")

# Load background image for "center" POV
background_image = pygame.image.load("images/Background.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
DINOSAUR_WIDTH, DINOSAUR_HEIGHT = 40, 60  # Dimensions of the dinosaur
dinosaur_x, dinosaur_y = 300, 290 # Initial position of the dinosaur
dino = pygame.Rect(dinosaur_x, dinosaur_y, DINOSAUR_WIDTH, DINOSAUR_HEIGHT)

# Obstacle settings
OBSTACLE_WIDTH = 20
obstacles = []  # List to store obstacles
SPAWN_OBSTACLE_EVENT = pygame.USEREVENT + 1  # Custom event for spawning obstacles
pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, random.randint(1500, 2500))  # Set timer for obstacle spawning

# Jumping mechanics
jumping = False
jump_velocity = -15  # Initial jump velocity
gravity = 1  # Gravity affecting the dinosaur
velocity_y = 0  # Vertical velocity of the dinosaur

# Game state variables
score = 0  # Player's score
flashlight = False  # Flashlight state
flashlightkeyduration = 2000  # Duration for holding the flashlight key
dino_game_active = True  # State of the dinosaur game
dino_paused = False  # Pause state of the game
current_pov = "center"  # Current point of view (camera)
last_pov_change = pygame.time.get_ticks()  # Time of the last POV change
# Draw sky
sky_image = pygame.image.load("images/sky.png").convert_alpha()  # Load the sky image
sky_x, sky_y = 400, 240  # Position of the sky image
sky_image = pygame.transform.scale(sky_image, (sky_x, sky_y))  # Adjust height to fit between ground and top of box
# Draw ground
ground_image = pygame.image.load("images/ground.png").convert_alpha()  # Load the ground image
groundimg_height, groundimg_width = 400, 60  # Position of the ground image
ground_x,ground_y= 200, 330  # Position of the ground image
ground_image = pygame.transform.scale(ground_image, (groundimg_height,groundimg_width))  # Scale the ground image to fit the box width and dinosaur height
gameover_x, gameover_y = 400, 200  # Position of the game over image
retry_x, retry_y = 400, 300  # Position of the retry image
pause_x, pause_y = 260, 250 # Position of the pause image
resume_x, resume_y= 260, 300 # Position of the resume image
gameborder_x, gameborder_y, gamerborder_height, gameborder_width= 195, 145, 410, 310  # Position and dimensions of the game border


# Timer variables
game_start_time = pygame.time.get_ticks()  # Start time of the game
minutesinmil= 60000 # 1 Minute in milliseconds
current_time_label = "12:00 AM"  # Initial time label

# Font settings
font = pygame.font.Font("font/Minecraft.ttf", 24)  # Font for rendering text

# Initialize key_held_start
key_held_start = 0 # Start time for tracking key press duration

# Base speed for obstacles
base_obstacle_speed = 5 

# Load win screen image
win_image = pygame.image.load("images/winscreen.jpg").convert()
winsound= pygame.mixer.Sound("sound/winsound.wav")

# Dinosaur Animation State
current_frame_index = 0  # Current frame index for running animation
ANIMATION_SPEED = 0.15  # Speed of the animation (bigger is faster)
animation_timer = 0  # Timer for animation

# Load Dino Sprite Sheet
sprite_sheet_path = "images/purpguy.png"  # Path to the sprite sheet
