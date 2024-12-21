from settings import *  # Import all constants and libraries from settings.py

class Enemy:
    def __init__(self, screen_name, jumpscare_image=None):
        self.screen_name = screen_name  # Screen name where the enemy appears
        self.jumpscare_image = jumpscare_image  # Image for the jumpscare animation
        self.active = False  # Whether the enemy is active
        self.cooldown = random.randint(10000, 20000)  # Cooldown time before the enemy can spawn again
        self.last_spawn_time = 0  # Last time the enemy was spawned
        self.spawn_time = 0  # Time when the enemy was spawned
        self.spawn_duration = 10000  # Duration the enemy stays active
        self.jumpscare_frames = []  # List to store jumpscare frames
        self.jumpscare_played = False  # Track if jumpscare has been played
        self.load_jumpscare_frames()  # Load jumpscare frames
        self.jumpscare_sound = None  # Jumpscare sound effect
        self.load_jumpscare_sound()  # Load jumpscare sound

    def spawn(self):
        """Spawn the enemy at a random location."""
        if not self.active and pygame.time.get_ticks() - self.last_spawn_time > self.cooldown:
            self.active = True  # Activate the enemy
            self.spawn_time = pygame.time.get_ticks()  # Record the spawn time

    def despawn(self):
        """Despawn the enemy."""
        self.active = False  # Deactivate the enemy
        self.last_spawn_time = pygame.time.get_ticks()  # Record the last spawn time

    def update(self):
        """Automatically despawn the enemy after its duration."""
        if self.active and pygame.time.get_ticks() - self.spawn_time > self.spawn_duration:
            if not self.jumpscare_played:
                self.trigger_jumpscare()  # Trigger the jumpscare
                self.jumpscare_played = True  # Mark the jumpscare as played

    def draw_indicator(self):
        """Draw an image on the respective screen."""
        if self.active:
            if self.screen_name == "left":
                indicator_image = pygame.image.load("images/BB.png").convert_alpha()  # Load the indicator image
            elif self.screen_name == "right":
                indicator_image = pygame.image.load("images/toy_bonnie.png").convert_alpha()  # Load the indicator image
            indicator_image = pygame.transform.scale(indicator_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen
            screen.blit(indicator_image, (0, 0))  # Draw the image on the screen

    def trigger_jumpscare(self):
        """Display an animated jumpscare and end the game."""
        if self.jumpscare_frames:
            if self.jumpscare_sound and not self.jumpscare_played:
                self.jumpscare_sound.play()  # Play the jumpscare sound effect if loaded and not already played
            for frame in self.jumpscare_frames:
                screen.blit(frame, (0, 0))  # Draw each frame on the screen
                pygame.display.flip()  # Update the display
                pygame.time.delay(20)  # Delay for smooth animation

            screen.blit(self.jumpscare_frames[-1], (0, 0))  # Draw the last frame
            pygame.display.flip()  # Update the display
            pygame.time.delay(3000)  # Delay for 3 seconds
        else:
            jumpscare_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create a surface for the jumpscare
            jumpscare_image.fill(RED)  # Fill the surface with red color
            screen.blit(jumpscare_image, (0, 0))  # Draw the surface on the screen
            pygame.display.flip()  # Update the display
            pygame.time.delay(3000)  # Delay for 3 seconds
        self.game_over_screen()  # Display the game over screen

    def load_jumpscare_frames(self):
        """Load jumpscare frames from sprite sheet."""
        if self.jumpscare_image:
            try:
                if self.jumpscare_image == "images/BBjumpscare.png":
                    sheet = pygame.image.load(self.jumpscare_image).convert_alpha()  # Load the sprite sheet
                    sheet_width, sheet_height = sheet.get_size()  # Get the size of the sprite sheet
                    cols, rows = 5, 10  # Number of columns and rows in the sprite sheet
                    total_frames = 51  # Total number of frames
                elif self.jumpscare_image == "images/toy_bonniejumpscare.png":
                    sheet = pygame.image.load(self.jumpscare_image).convert_alpha()  # Load the sprite sheet
                    sheet_width, sheet_height = sheet.get_size()  # Get the size of the sprite sheet
                    cols, rows = 5, 9  # Number of columns and rows in the sprite sheet
                    total_frames = 41  # Total number of frames
                else:
                    print(f"Unknown jumpscare image: {self.jumpscare_image}")
                    return
                frame_width = sheet_width // cols  # Width of each frame
                frame_height = sheet_height // rows  # Height of each frame

                for row in range(rows):
                    for col in range(cols):
                        if len(self.jumpscare_frames) < total_frames:
                            frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)  # Rectangle representing the frame
                            frame = sheet.subsurface(frame_rect)  # Extract the frame from the sprite sheet
                            scaled_frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the frame to fit the screen
                            self.jumpscare_frames.append(scaled_frame)  # Add the frame to the list
            except pygame.error as e:
                print(f"Error loading jumpscare frames: {e}")

    def load_jumpscare_sound(self):
        """Load the jumpscare sound effect."""
        if self.jumpscare_image == "images/BBjumpscare.png":
            self.jumpscare_sound = pygame.mixer.Sound("sound/BBjumpscaresound.wav")  # Load the jumpscare sound effect
        elif self.jumpscare_image == "images/toy_bonniejumpscare.png":
            self.jumpscare_sound = pygame.mixer.Sound("sound/bonniejumpscaresound.wav")  # Load the jumpscare sound effect
        else:
            print(f"Unknown jumpscare image: {self.jumpscare_image}")
            self.jumpscare_sound = None  # Set to None if unknown image
    def game_over_screen(self):
        """Display a game over screen with retry and placeholder for main menu."""
        font_large = pygame.font.Font('font/minecraft.ttf', 100)  # Load a large font
        font_small = pygame.font.Font('font/minecraft.ttf', 50)  # Load a small font

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Quit the game
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = False  # Exit the game over screen
                        restart_dinosaur_game()  # Restart the game

            screen.fill(BLACK)  # Fill the screen with black color
            game_over_text = font_large.render("GAME OVER", True, RED)  # Render the game over text
            retry_text = font_small.render("Press R to Retry", True, WHITE)  # Render the retry text
            screen.blit(game_over_text, game_over_text.get_rect(center=(gameover_x,gameover_y)))  # Draw the game over text
            screen.blit(retry_text, retry_text.get_rect(center=(retry_x,retry_y)))  # Draw the retry text
            pygame.display.flip()  # Update the display

# Create two enemies
red_enemy = Enemy("left", "images/BBjumpscare.png")  # Create a red enemy
blue_enemy = Enemy("right", "images/toy_bonniejumpscare.png")  # Create a blue enemy

def update_dino_animation():
    """Update Dino animation based on running or jumping state."""
    global current_frame_index, animation_timer
    if jumping:
        # If the dinosaur is jumping, return the jump frame
        return jump_frame
    else:
        # If the dinosaur is running, cycle through running frames
        animation_timer += ANIMATION_SPEED  # Increment the animation timer by the animation speed
        if animation_timer >= 1:
            # If the timer exceeds or equals 1, update the frame index
            current_frame_index = (current_frame_index + 1) % len(running_frames)  # Move to the next frame, looping back to the start if necessary
            animation_timer = 0  # Reset the animation timer
        return running_frames[current_frame_index]  # Return the current running frame based on the frame index

def wingamecondition():
    if score >= 143:  # Check if the score reaches 143
        return True  # End the game if the score reaches 143
    return False  # Continue the game

def restart_dinosaur_game():
    """Reset the Dinosaur Game variables."""
    global dino_game_active, score, obstacles, jumping, velocity_y, dino_paused, current_pov, hours, game_start_time, current_time_label, dinosaur_y
    # Reset variables
    dino_game_active = True
    score = 0
    hours = 12
    obstacles = []
    jumping = False
    velocity_y = 0
    dino_paused = False
    current_pov = "center"
    dino.y = dinosaur_y
    red_enemy.despawn()
    blue_enemy.despawn()
    pygame.event.clear(SPAWN_OBSTACLE_EVENT)
    red_enemy.jumpscare_played = False
    blue_enemy.jumpscare_played = False
    game_start_time = pygame.time.get_ticks()

def draw_pause_menu():
    """Draw the pause menu for the Dinosaur Game."""
    pause_text = font.render("Dinosaur Game Paused", True, BLACK)  # Render the pause text
    resume_text = font.render("Press ESC to Resume", True, BLACK)  # Render the resume text

    # Draw the pause text in the center of the screen
    screen.blit(pause_text, (pause_x, pause_y))
    # Draw the resume text below the pause text
    screen.blit(resume_text, (resume_x,resume_y))

    pygame.display.update()  # Update the display to show the pause menu

def update_timer():
    """Update the timer and display the current time."""
    global current_time_label, minutesinmil, hours
    elapsed_time = pygame.time.get_ticks() - game_start_time  # Calculate elapsed time since game start
    total_minutes = elapsed_time // minutesinmil  # Convert elapsed time to minutes
    if total_minutes >= 12:
        return True  # End the game if 12 minutes have passed

    hours = 12 + total_minutes // 2  # Calculate the current hour
    minutes = (total_minutes % 2) * 30  # Calculate the current minutes (0 or 30)
    if hours > 12:
        hours -= 12  # Adjust hours to 12-hour format

    current_time_label = f"{hours}:{minutes:02d} AM"  # Format the current time label
    return False  # Continue the game

def draw_timer():
    """Draw the timer on the screen."""
    timer_text = font.render(current_time_label, True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, SCREEN_HEIGHT - timer_text.get_height() - 20))

# Load Dino Sprite Sheet
def load_dino_sprite_sheet():
    """Load the dinosaur sprite sheet and extract frames for running and jumping."""
    sheet = pygame.image.load(sprite_sheet_path).convert_alpha()  # Load the sprite sheet
    sprite_width = sheet.get_width() // 5  # 5 columns in the sprite sheet
    sprite_height = sheet.get_height() // 7  # 7 rows in the sprite sheet
    running_frames = []

    # Extract frames for running (top row)
    for i in range(5):
        frame = sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))  # Extract frame
        running_frames.append(pygame.transform.scale(frame, (DINOSAUR_WIDTH, DINOSAUR_HEIGHT)))  # Scale and add to list

    # Extract frame for jumping (bottom-left frame)
    jump_frame = sheet.subsurface((0, 6 * sprite_height, sprite_width, sprite_height))  # Extract frame
    jump_frame = pygame.transform.scale(jump_frame, (DINOSAUR_WIDTH, DINOSAUR_HEIGHT))  # Scale the frame

    return running_frames, jump_frame  # Return the frames

running_frames, jump_frame = load_dino_sprite_sheet()  # Load the frames

def main():
    global jumping, velocity_y, score, dino_game_active, dino_paused, current_pov, last_pov_change, flashlight, flashlightkeyduration, background_image, gameborder_x, gameborder_y, gamerborder_height, gameborder_width, sky_image, ground_image
    global gameover_x, gameover_y, retry_x, retry_y, pause_x, pause_y, resume_x, resume_y, sky_x, sky_y, ground_x, ground_y
    running = True

    while running:
        if update_timer() or wingamecondition():
            winsound.play()  # Play the win sound
            scaled_win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_win_image, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5000)  # Display the win screen for 5 seconds
            running = False  # Game won by surviving until 6 AM or reaching 143 points

        # Apply camera function based on POV (covers the entire screen)
        if current_pov == "left":
            screen.fill(BLACK)
            red_enemy.draw_indicator()
        elif current_pov == "right":
            screen.fill(BLACK)
            blue_enemy.draw_indicator()
        else:
            screen.blit(background_image, (0, 0))

            # Dinosaur game (inside the white box)
            # Draw the game box border
            pygame.draw.rect(screen, BLACK, (gameborder_x, gameborder_y, gamerborder_height, gameborder_width), 5)
            
            if dino_game_active:
                if not dino_paused:
                    # Update dinosaur position if jumping
                    if jumping:
                        dino.y += velocity_y  # Update vertical position
                        velocity_y += gravity  # Apply gravity
                        if dino.y >= dinosaur_y:
                            dino.y = dinosaur_y  # Reset position if on the ground
                            jumping = False  # Stop jumping

                    # Update obstacles
                    obstacle_speed = base_obstacle_speed + score // 1000  # Increase obstacle speed based on score
                    for obstacle in list(obstacles):
                        obstacle['rect'].x -= obstacle_speed  # Move obstacle to the left
                        if obstacle['rect'].right < BOX_X + 30:  # Check if obstacle is near the left edge of the box
                            obstacle['alpha'] -= 68  # Decrease obstacle transparency
                            if obstacle['alpha'] <= 0:  # Remove obstacle if fully transparent
                                obstacles.remove(obstacle)
                                score += 1  # Increase score for successfully avoiding the obstacle
                        else:
                            if obstacle['alpha'] < 255:  # Increase obstacle transparency if not fully opaque
                                obstacle['alpha'] += 10  # Increase obstacle transparency

                        if dino.colliderect(obstacle['rect']):  # Check collision with obstacles
                            score -= 10  # Decrease score by 10 for collision
                            if score < 0:
                                score = 0  # Ensure score doesn't go below 0
                            obstacles.remove(obstacle)  # Remove the obstacle
                            dino.x = dinosaur_x
                            dino.y = dinosaur_y  # Reset dinosaur's vertical position
                            break  # Exit the loop after handling collision

                    # Ensure obstacles don't spawn too close to each other
                    if obstacles and obstacles[-1]['rect'].x < OBSCTALE_SPAWN_X:
                        pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, random.randint(1500, 2500))

                screen.blit(sky_image, (BOX_X, BOX_Y))  # Draw the sky image
                screen.blit(ground_image, (ground_x,ground_y))  # Draw the ground image

                # Draw Dino with animation
                dino_frame = update_dino_animation()  # Get the current frame for the dinosaur animation
                screen.blit(dino_frame, dino)  # Draw the dinosaur frame
                
                # Draw obstacles
                for obstacle in obstacles:
                    obstacle_image = pygame.image.load("images/obstacle.png").convert_alpha()  # Load the obstacle image
                    obstacle_image = pygame.transform.scale(obstacle_image, (obstacle['rect'].width, obstacle['rect'].height))  # Scale the obstacle image
                    obstacle_image.set_alpha(obstacle['alpha'])  # Set the transparency of the obstacle image
                    screen.blit(obstacle_image, obstacle['rect'].topleft)  # Draw the obstacle image

                # Draw score
                score_text = font.render(f"Score: {score}", True, BLACK)  # Render the score text
                screen.blit(score_text, (BOX_X + BOX_WIDTH - score_text.get_width() - 20, BOX_Y + BOX_HEIGHT - score_text.get_height() - 20))  # Draw the score text

            if dino_paused:
                draw_pause_menu()  # Draw the pause menu if the game is paused

        # Spawn and handle enemies
        red_enemy.spawn()  # Spawn the red enemy
        blue_enemy.spawn()  # Spawn the blue enemy

        red_enemy.update()  # Update the red enemy
        blue_enemy.update()  # Update the blue enemy

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SPAWN_OBSTACLE_EVENT and dino_game_active and not dino_paused:
                obstacle_height = random.randint(20, 60)

                obstacle = {
                    'rect': pygame.Rect(580, 350- obstacle_height, OBSTACLE_WIDTH, obstacle_height),
                    'alpha': 0
                }
                obstacles.append(obstacle)
                pygame.time.set_timer(SPAWN_OBSTACLE_EVENT, random.randint(1500, 2500))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    Enemy.jumpscare_played = False
                    if not dino_game_active:
                        restart_dinosaur_game()
                    elif dino_paused:
                        dino_paused = False
                if event.key == pygame.K_ESCAPE and current_pov == "center":
                    dino_paused = not dino_paused
                if event.key == pygame.K_f:
                    key_held_start = pygame.time.get_ticks()  # Start tracking key press time
                    flashlight = True

            # Detect key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    key_held_start = 0  # Reset when key is released
                    flashlight = False

            # Check if F key is held long enough
            if pygame.key.get_pressed()[pygame.K_f]:
                if key_held_start and pygame.time.get_ticks() - key_held_start > flashlightkeyduration:
                    if red_enemy.active and current_pov == "left":
                        red_enemy.despawn()
                    elif blue_enemy.active and current_pov == "right":
                        blue_enemy.despawn()
                    key_held_start = pygame.time.get_ticks()  # Reset the timer to allow continuous despawning

        # Show flashlight image if flashlight is true
        if flashlight:
            if red_enemy.active and current_pov == "left":
                indicator_image = pygame.image.load("images/BBflashlight.png").convert_alpha()
                indicator_image = pygame.transform.scale(indicator_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(indicator_image, (0, 0))
            elif blue_enemy.active and current_pov == "right":
                indicator_image = pygame.image.load("images/toy_bonnieflashlight.png").convert_alpha()
                indicator_image = pygame.transform.scale(indicator_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(indicator_image, (0, 0))
            elif current_pov == "left" or current_pov == "right":
                indicator_image = pygame.image.load("images/noneflashlight.png").convert_alpha()
                indicator_image = pygame.transform.scale(indicator_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(indicator_image, (0, 0))
            elif current_pov == "center":
                flashlight = False  # Disable flashlight in center POV

        # User input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not jumping and dino_game_active and not dino_paused:
            jumping = True
            velocity_y = jump_velocity
        if keys[pygame.K_a] and pygame.time.get_ticks() - last_pov_change > 500:
            current_pov = "left" if current_pov == "center" else "center"
            last_pov_change = pygame.time.get_ticks()
        if keys[pygame.K_d] and pygame.time.get_ticks() - last_pov_change > 500:
            current_pov = "right" if current_pov == "center" else "center"
            last_pov_change = pygame.time.get_ticks()

        # Draw timer
        draw_timer()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
