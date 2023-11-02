import pygame
import random
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600 #Display Size
BALL_SIZE = 20
PADDLE_LIMIT = WIDTH

# Variables
paddle_speed = 5
ball_speed = 3
paddle_width = 100
paddle_height = 10


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
DGRAY = (64, 64, 64) #Dark Gray
LGRAY = (196, 196, 196) #Light Gray
CYAN = (0, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker Project")

# Game variables
play = False
score = 0
paddle = 310

#Random Ball Placement and Direction
ball_pos = [340 + random.randint(-50,50), 350 + random.randint(-30,30)]
ball_dir = [2*[-1,1][random.randrange(2)], -3]

#Number of Rows and Columns
rows=5
cols=7
total_bricks = rows*cols

# Initialize the map (layout of bricks) - Checkered Decreasing Pattern
map = [[(i//2 + 1) if ((i + j) % 2 == 0 and i%2==1 ) else i//2 if ((i + j) % 2 == 1 and i%2==1) else i//2 - 1 if ((i + j) % 2 == 1 and i%2==0) else i//2 + 1 for j in range(cols)] for i in range(rows+2,0,-1)]

#Brick Size
brick_width = 640 // cols
brick_height = 40

# Pygame clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
mode_text = font.render("Normal Mode", True, LGRAY)

# Main game loop initialize
running = True
move_left = False
move_right = False

#Game Loop
while running:
    for event in pygame.event.get():

        #Quit Game - X button
        if event.type == pygame.QUIT:
            running = False
        
        #If any Key is pressed
        if event.type == pygame.KEYDOWN:
            
            #Play/Pause - Spacebar
            if event.key == pygame.K_SPACE:
                play = not play
            
            #Move Paddle - Start
            if play:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
            
        # New Game

            # Normal Mode - Press Enter
            if event.key == pygame.K_RETURN:
                play = False
                ball_pos = [340  + random.randint(-50,50), 350 + random.randint(-30,30)]
                paddle = 310
                paddle_speed = 5
                paddle_width = 100
                paddle_height = 10
                ball_speed = 3
                ball_dir = [2*[-1,1][random.randrange(2)], -3]
                score = 0
                mode_text = font.render("Normal Mode", True, LGRAY)
                total_bricks = rows*cols
                map = [[(i//2 + 1) if ((i + j) % 2 == 0 and i%2==1 ) else i//2 if ((i + j) % 2 == 1 and i%2==1) else i//2 - 1 if ((i + j) % 2 == 1 and i%2==0) else i//2 + 1 for j in range(cols)] for i in range(rows+2,0,-1)]
            
            #Easy Mode - Press 1
            if event.key == pygame.K_1:
                play = False
                ball_pos = [340  + random.randint(-50,50), 340 + random.randint(-30,30)]
                ball_speed = 3
                ball_dir = [2*[-1,1][random.randrange(2)], -3]
                paddle_speed = 5
                paddle_width = 200
                paddle_height = 10
                paddle = 310
                score = 0
                mode_text = font.render("Easy Mode", True, LGRAY)
                total_bricks = rows*cols
                map = [[(i//2 + 1) if ((i + j) % 2 == 0 and i%2==1 ) else i//2 if ((i + j) % 2 == 1 and i%2==1) else i//2 - 1 if ((i + j) % 2 == 1 and i%2==0) else i//2 + 1 for j in range(cols)] for i in range(rows+2,0,-1)]
            
            #Hard Mode - Press 2
            if event.key == pygame.K_2:
                play = False
                ball_pos = [240  + random.randint(-50,50), 350 + random.randint(-30,30)]
                ball_speed = 6
                ball_dir = [4*[-1,1][random.randrange(2)], -6]
                paddle_speed = 7
                paddle_width = 80
                paddle_height = 20
                paddle = 310
                score = 0
                mode_text = font.render("Hard Mode", True, LGRAY)
                total_bricks = rows*cols
                map = [[(i//2 + 1) if ((i + j) % 2 == 0 and i%2==1 ) else i//2 if ((i + j) % 2 == 1 and i%2==1) else i//2 - 1 if ((i + j) % 2 == 1 and i%2==0) else i//2 + 1 for j in range(cols)] for i in range(rows+2,0,-1)]
        
        #Move Paddle - Stop
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
    
    #Paddle Movement
    if move_left and paddle - paddle_speed > 0:
        paddle -= paddle_speed
    if move_right and paddle + paddle_width + paddle_speed < PADDLE_LIMIT:
        paddle += paddle_speed

    #If Game is running
    if play:
        ball_pos[0] += ball_dir[0]
        ball_pos[1] += ball_dir[1]

        #Collision with Wall
        if ball_pos[0] < 0 or ball_pos[0] > WIDTH - BALL_SIZE:
            ball_dir[0] = -ball_dir[0]
        if ball_pos[1] < 0:
            ball_dir[1] = -ball_dir[1]

        #Ball out of Bound (Game Over)
        if ball_pos[1] > HEIGHT - BALL_SIZE:
            play = False

        if (paddle < ball_pos[0] < paddle + paddle_width and HEIGHT - BALL_SIZE - paddle_height <= ball_pos[1] <= HEIGHT - BALL_SIZE + ball_speed):
            ball_dir[1] = -ball_dir[1]

        #Brick Layout Generator
        for i in range(rows):
            for j in range(cols):
                if map[i][j] > 0:
                    brick_x = j * brick_width + 80
                    brick_y = i * brick_height + 50
                    brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                    ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE)

                    #Collision Detection
                    if brick_rect.colliderect(ball_rect):
                        if ball_pos[0] + BALL_SIZE - 2 <= brick_x or ball_pos[0] + 2 >= brick_x + brick_width:
                            ball_dir[0] = -ball_dir[0]
                        else:
                            ball_dir[1] = -ball_dir[1]
                        
                        #Score Increment and Brick Level Down
                        if map[i][j]>1:
                            map[i][j]-=1
                            score +=map[i][j]*5
                        else:
                            #Brick Removal
                            map[i][j] = 0
                            total_bricks -= 1
                            score += 5
    

    # Clear the screen
    screen.fill(BLACK)

    # Draw the map (bricks)
    for i in range(rows):
        for j in range(cols):
            if map[i][j] > 0:
                brick_x = j * brick_width + 80
                brick_y = i * brick_height + 50
                brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)

                #Color of Bricks depending on level
                color = WHITE if map[i][j] == 1 else LGRAY if map[i][j] == 2 else GRAY if map[i][j] == 3 else DGRAY
                pygame.draw.rect(screen, color, brick_rect)
                pygame.draw.rect(screen, BLACK, brick_rect, 3)

    # Draw the paddle
    pygame.draw.rect(screen, GREEN, (paddle, HEIGHT - paddle_height, paddle_width, paddle_height))

    # Draw the ball
    pygame.draw.ellipse(screen, RED, (ball_pos[0], ball_pos[1], BALL_SIZE+1, BALL_SIZE+1))

    # Draw the score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))
    screen.blit(mode_text, (60, 10))


    # Displays Game Guide
    project_info_font = pygame.font.Font(None, 25)
    info_text4 = project_info_font.render("Press Spacebar play/pause", True, GRAY)
    info_text5 = project_info_font.render("Press Enter to Restart", True, GRAY)
    screen.blit(info_text4, (80, 500))
    screen.blit(info_text5, (80, 525))

    # Check for win condition
    if total_bricks <= 0:
        play = False
        win_text = font.render("YOU WON: " + str(score), True, CYAN)
        screen.blit(win_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))

    # Check for game over
    if not play and ball_pos[1] > HEIGHT - BALL_SIZE:
        
        # Displaying Game Score and Restart Option
        game_over_text = font.render("Game Over, Score: " + str(score), True, CYAN)
        restart_text = font.render("Press Enter To Restart", True, WHITE)
        easy_text = font.render("Press 1 for Easy Mode", True, LGRAY)
        hard_text = font.render("Press 2 for Hard Mode", True, LGRAY)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 ))
        screen.blit(easy_text, (WIDTH // 2 - 150, HEIGHT // 2 + 30))
        screen.blit(hard_text, (WIDTH // 2 - 150, HEIGHT // 2 + 60))
        
        # Displaying Project Info
        info_text1 = project_info_font.render("Project by -", True, WHITE)
        info_text2 = project_info_font.render("Divjot, Varshit, Arpit, Vedashree", True, WHITE)
        info_text3 = project_info_font.render("131, 100, 079, 088", True, WHITE)
        screen.blit(info_text1, (180, 400))
        screen.blit(info_text2, (180, 425))
        screen.blit(info_text3, (180, 450))

    #Next Frame
    pygame.display.update()
    clock.tick(60)

# End of Program
pygame.quit()