import pygame
import random
import os 

pygame.init()

# music initialize
pygame.mixer.init()



screen_width=800
screen_height=500


#defining colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
violet =(204, 204, 255)
green = (51, 204, 51)
green2 = (0, 255, 153)
redtone = (255, 51, 0)

gameWindow=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake game by ShivaRK")
pygame.display.update()
clock = pygame.time.Clock()

#bg image
bgimg = pygame.image.load('bg3.jpg')
bgimg = pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha()

bgimg2 = pygame.image.load('welcomebg.jpg')
bgimg2 = pygame.transform.scale(bgimg2,(screen_width,screen_height)).convert_alpha()

bgimg3 = pygame.image.load('gameoverbg.jpg')
bgimg3 = pygame.transform.scale(bgimg3,(screen_width,screen_height)).convert_alpha()

#score on screen
font=pygame.font.SysFont('gabriola', 60)
def text_screen(text,color,x,y):
    screen_text=font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

# length increament
def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,blue,[x,y,snake_size, snake_size])


def welcome():
    exit_game=False
    while not exit_game:
        # gameWindow.fill(violet)

        gameWindow.blit(bgimg2, (0,0))
        text_screen("Welcome to Snake Game By ShivaRK", redtone, 60, screen_height/8)
        text_screen("Press Space to Play", redtone, 200, screen_height/3)
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        # pygame.mixer.music.load('Stardrive2.mp3')
                        # pygame.mixer.music.play()
                        gameloop()

        pygame.display.update()
        clock.tick(30)
        


# Creating game loop
def gameloop():
    #defining variables
    
    exit_game=False
    game_over=False
    score=0

    snake_x=50
    snake_y = 50
    snake_size = 20

    velocity_x=0  #both made zeroes here
    velocity_y=0
    init_velocity=5

    food_x= random.randint(20, screen_width-20)
    food_y= random.randint(20, screen_height-20)

    fps=30

    snk_list=[]
    snk_length=1

    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt","r") as f:
        highscore = f.read()


    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            # gameWindow.fill(red)
            gameWindow.blit(bgimg3, (0,0))
            text_screen("Game Over!!! Press Enter to continue", red, 80, screen_height/5)
            text_screen("Check textfile for highscore", redtone, 80, screen_height/3)
            text_screen("Your score : "+ str(score), redtone, 50, screen_height*(0.75))
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True

                
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()
        
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x = init_velocity #changed here
                        velocity_y = 0 #it goes diagonally , so if snake moves in x , it cant go in y direction
                    if event.key==pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key==pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key==pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key==pygame.K_i:
                        score+=20    

            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            if abs(snake_x - food_x) < 14 and abs(snake_y - food_y) < 14:
                score+=10
                # print("Score is ", score)
                snk_length+=5
                pygame.mixer.music.load('eat.wav')
                pygame.mixer.music.play()

                food_x= random.randint(20, screen_width-20)
                food_y= random.randint(20, screen_height-20)
                if score>int(highscore):
                    highscore=score
            
            # gameWindow.fill(white)
            gameWindow.blit(bgimg, (0,0))
            pygame.draw.circle(gameWindow, red, (food_x,food_y), 10) #food
            # pygame.draw.rect(gameWindow,blue,[snake_x,snake_y,snake_size, snake_size])
            plot_snake(gameWindow,blue,snk_list,snake_size)

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over=True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()

            if snake_x<0 or snake_y<0 or snake_x>screen_width or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()
                # print("Game over")

            text_screen("Score : "+str(score) + "                                   Highscore :"+ str(highscore) , black, 5, 5)
        pygame.display.update() #must for updating bg color or any other functions
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()