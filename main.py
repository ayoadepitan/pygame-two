import os
from tracemalloc import start
import pygame
import random

# Opens window in second monitor
x = 1920
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (0, 155, 0)
light_green = (0,255,0)


display_width = 800
display_height = 600


game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')

# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

# img = pygame.image.load('snakehead.png')
# apple_img = pygame.image.load('apple.png')

clock = pygame.time.Clock()



tank_width = 40
tank_height = 20

turret_width = 5
wheel_width = 5

ground_height = 35

FPS = 15


small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)


def text_objects(text, color, size):
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "medium":
        text_surface = med_font.render(text, True, color)
    elif size == "large":
        text_surface = large_font.render(text, True, color)
            
    return text_surface, text_surface.get_rect()

def text_to_button(text, color, button_x, button_y, button_width, button_height, size="small"):
    text_surf, text_rect = text_objects(text, color, size)
    text_rect.center = ((button_x + (button_width/2)), button_y + (button_height/2))
    game_display.blit(text_surf, text_rect)

def message_to_screen(text, color, y_displace=0, size="small"):
    text_surf, text_rect = text_objects(text, color, size)
    text_rect.center = (display_width / 2),  (display_height / 2) + y_displace
    game_display.blit(text_surf, text_rect)

def tank(x,y, tur_pos):
    x = int(x)
    y = int(y)

    possible_turrets = [(x-27, y-2),
                        (x-26, y-5),
                        (x-25, y-8),
                        (x-23, y-12),
                        (x-20, y-14),
                        (x-18, y-15),
                        (x-15, y-17),
                        (x-13, y-19),
                        (x-11, y-21),
                        ]

    pygame.draw.circle(game_display, black, (x,y), int(tank_height/2))
    pygame.draw.rect(game_display, black, (x-tank_height, y, tank_width, tank_height))

    pygame.draw.line(game_display,black, (x,y), possible_turrets[tur_pos], turret_width)

    start_x = 15

    for _ in range(7):
        pygame.draw.circle(game_display, black, (x-start_x, y+20), wheel_width)
        start_x -= 5

    return possible_turrets[tur_pos]

def enemy_tank(x,y, tur_pos):
    x = int(x)
    y = int(y)

    possible_turrets = [(x+27, y-2),
                        (x+26, y-5),
                        (x+25, y-8),
                        (x+23, y-12),
                        (x+20, y-14),
                        (x+18, y-15),
                        (x+15, y-17),
                        (x+13, y-19),
                        (x+11, y-21),
                        ]

    pygame.draw.circle(game_display, black, (x,y), int(tank_height/2))
    pygame.draw.rect(game_display, black, (x-tank_height, y, tank_width, tank_height))

    pygame.draw.line(game_display,black, (x,y), possible_turrets[tur_pos], turret_width)

    start_x = 15

    for _ in range(7):
        pygame.draw.circle(game_display, black, (x-start_x, y+20), wheel_width)
        start_x -= 5

    return possible_turrets[tur_pos]

def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        game_display.fill(white)
        message_to_screen("Controls", green, -100, "large")
        message_to_screen("Fire: Spacebar", black, -30)
        message_to_screen("Move Turret: Up and Down arrows", black, 10)
        message_to_screen("Move Tank: Left and Right arrows", black, 50)
        message_to_screen("Pause: P", black, 90)

        button("play", 150,500,100,50, green, light_green, action="play")
        end_controls = button("main", 350,500,100,50, yellow, light_yellow, action="main")
        button("quit", 550,500,100,50, red, light_red, action="quit")

        if end_controls == True:
            gcont = False

        pygame.display.update()
        clock.tick(FPS)


def button(text, x, y , width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+width > cur[0] > x and y+height > cur[1] > y:
        pygame.draw.rect(game_display,active_color, (x,y,width,height))
    else:
        pygame.draw.rect(game_display,inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)
    
    if click[0] == 1 and x+width > cur[0] > x and y+height > cur[1] > y:
        while x+width > cur[0] > x and y+height > cur[1] > y:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if action == 'quit':
                        pygame.quit()
                    elif action == 'controls':
                        game_controls()
                    elif action == 'play':
                        gameLoop()
                    elif action == 'main':
                        game_intro()

    # cur = pygame.mouse.get_pos()
    # click = pygame.mouse.get_pressed()

    # if x + width > cur[0] > x and y + height > cur[1] > y:
    #     pygame.draw.rect(game_display, active_color, (x,y,width,height))
    #     if click[0] == 1 and action != None:
    #         if action == "quit":
    #             pygame.quit()
    #             quit()
    #         if action == "controls":
    #             game_controls()
    #         if action == "play":
    #             gameLoop()
    #         if action == "main":
    #             return True

    # else:
    #     pygame.draw.rect(game_display, inactive_color, (x,y,width,height))
    
    # text_to_button(text,black,x,y,width,height)

def pause():
    paused = True
    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press C to continue or Q to quit", black)

    pygame.display.update()
    clock.tick(5)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit() 

        # game_display.fill(white)
        

def score(score):
    text = small_font.render('Score: ' + str(score), True, black)
    game_display.blit(text, [0,0])


def barrier(location_x, random_height, barrier_width):
    pygame.draw.rect(game_display, black, [location_x, display_height-random_height, barrier_width, random_height])

def explosion(x,y, size=50):
    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        start_point = x, y

        color_choices = [red, light_red, yellow, light_yellow]

        magnitude = 1

        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1*magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1*magnitude, magnitude)

            pygame.draw.circle(game_display, color_choices[random.randrange(0,4)], (exploding_bit_x, exploding_bit_y), random.randrange(1,5))
            magnitude += 1

            pygame.display.update()
            clock.tick(100)
        
        explode = False



def fire_shell(gun_position, tank_x, tank_y, tur_pos, gun_power, location_x, barrier_width, random_height, enemy_tank_x, enemy_tank_y):
    fire = True
    damage = 0

    starting_shell = list(gun_position)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.draw.circle(game_display, red, (starting_shell[0], starting_shell[1]), 5)
        
        
        starting_shell[0] -= (12 - tur_pos)*2

        if starting_shell[1] > display_height - ground_height:
            print('Last shell:', starting_shell[0], starting_shell[1])
            hit_x = int((starting_shell[0]*display_height-ground_height)/starting_shell[1])
            hit_y = int(display_height-ground_height)
            print('Impact:', hit_x, hit_y)
            if enemy_tank_x + 10 > hit_x > enemy_tank_x - 10:
                print('Critical Hit')
                damage = 25
            elif enemy_tank_x + 15 > hit_x > enemy_tank_x - 15:
                print('Hard Hit')
                damage = 18
            elif enemy_tank_x + 25 > hit_x > enemy_tank_x - 25:
                print('Medium Hit')
                damage = 10
            elif enemy_tank_x + 35 > hit_x > enemy_tank_x - 35:
                print('Light Hit')
                damage = 5

            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = starting_shell[0] <= location_x + barrier_width
        check_x_2 = starting_shell[0] >= location_x
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print('Last shell:', starting_shell[0], starting_shell[1])
            hit_x = int(starting_shell[0])
            hit_y = int(starting_shell[1])
            print('Impact:', hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False


        starting_shell[1] += int((((starting_shell[0] - gun_position[0])*0.015/(gun_power/50))**2) - (tur_pos+tur_pos/(12-tur_pos)))
        pygame.display.update()
        clock.tick(50)
    return damage

def enemy_fire_shell(gun_position, tank_x, tank_y, tur_pos, gun_power, location_x, barrier_width, random_height, p_tank_x, p_tank_y):
    
    damage = 0
    
    current_power = 1 
    power_found = False

    while not power_found:
        current_power += 1
        if current_power > 100:
            power_found = True

        fire = True
        starting_shell = list(gun_position)

        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            # pygame.draw.circle(game_display, red, (starting_shell[0], starting_shell[1]), 5)
            
            starting_shell[0] += (12 - tur_pos)*2
            starting_shell[1] += int((((starting_shell[0] - gun_position[0])*0.015/(current_power/50))**2) - (tur_pos+tur_pos/(12-tur_pos)))

            if starting_shell[1] > display_height - ground_height:
                hit_x = int((starting_shell[0]*display_height-ground_height)/starting_shell[1])
                hit_y = int(display_height-ground_height)
                # explosion(hit_x, hit_y)
                if p_tank_x + 15 > hit_x > p_tank_x - 15:
                    print('Target Acquired')
                    power_found = True
                fire = False

            check_x_1 = starting_shell[0] <= location_x + barrier_width
            check_x_2 = starting_shell[0] >= location_x
            check_y_1 = starting_shell[1] <= display_height
            check_y_2 = starting_shell[1] >= display_height - random_height

            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(starting_shell[0])
                hit_y = int(starting_shell[1])
                # explosion(hit_x, hit_y)
                fire = False
     
    fire = True
    starting_shell = list(gun_position)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.draw.circle(game_display, red, (starting_shell[0], starting_shell[1]), 5)
        
        
        starting_shell[0] += (12 - tur_pos)*2

        gun_power = random.randrange(int(current_power*0.90), int(current_power*1.10))

        starting_shell[1] += int((((starting_shell[0] - gun_position[0])*0.015/(gun_power/50))**2) - (tur_pos+tur_pos/(12-tur_pos)))

        if starting_shell[1] > display_height - ground_height:
            hit_x = int((starting_shell[0]*display_height-ground_height)/starting_shell[1])
            hit_y = int(display_height-ground_height)
            if p_tank_x + 10 > hit_x > p_tank_x - 10:
                print('Critical Hit')
                damage = 25
            elif p_tank_x + 15 > hit_x > p_tank_x - 15:
                print('Hard Hit')
                damage = 18
            elif p_tank_x + 25 > hit_x > p_tank_x - 25:
                print('Medium Hit')
                damage = 10
            elif p_tank_x + 35 > hit_x > p_tank_x - 35:
                print('Light Hit')
                damage = 5

            explosion(hit_x, hit_y)
            fire = False

        check_x_1 = starting_shell[0] <= location_x + barrier_width
        check_x_2 = starting_shell[0] >= location_x
        check_y_1 = starting_shell[1] <= display_height
        check_y_2 = starting_shell[1] >= display_height - random_height

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int(starting_shell[0])
            hit_y = int(starting_shell[1])
            explosion(hit_x, hit_y)
            fire = False


        pygame.display.update()
        clock.tick(50)

    return damage


def power(level):
    text = small_font.render("Power: " + str(level) + "%", True, black)
    game_display.blit(text, [display_width/2, 0])

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.fill(white)
        message_to_screen("Welcome to Tanks!", green, -100, "large")
        message_to_screen("The objective is to shoot and destroy", black, -30)
        message_to_screen("the enemy tank before they destroy you.", black, 10)
        message_to_screen("The more enemies you destroy, the harder they get.", black, 50)
        # message_to_screen("Press C to play, P to pause or Q to quit", black, 180)

        button("play", 150,500,100,50, green, light_green, action="play")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,100,50, red, light_red, action="quit")

        pygame.display.update()
        clock.tick(FPS)

def end_game():
    end_game = True

    while end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)
        message_to_screen("Game Over", red, -100, "large")
        message_to_screen("You Died", black, -30)

        button("play again", 150,500,150,50, green, light_green, action="play")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,100,50, red, light_red, action="quit")

        pygame.display.update()
        clock.tick(FPS)

def you_win():
    you_win = True

    while you_win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)
        message_to_screen("You Win!", green, -100, "large")
        message_to_screen("Congratulations", black, -30)

        button("play again", 150,500,150,50, green, light_green, action="play")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,100,50, red, light_red, action="quit")

        pygame.display.update()
        clock.tick(FPS)



def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(game_display, player_health_color, (680,25, player_health, 25))
    pygame.draw.rect(game_display, enemy_health_color, (20,25, enemy_health, 25))


def gameLoop():
    game_exit = False
    game_over = False

    player_health = 100
    enemy_health = 100

    barrier_width = 50

    main_tank_x = display_width * 0.9
    main_tank_y = display_height * 0.9

    tank_move = 0

    current_tur_pos = 0
    change_tur = 0

    enemy_tank_x = display_width * 0.1
    enemy_tank_y = display_height * 0.9

    fire_power = 50
    power_change = 0

    location_x = (display_width/2) + random.randint(-0.1*display_width, 0.1*display_width)
    random_height = random.randrange(display_height*0.1, display_height*0.6)

    while not game_exit:
        

        if game_over:
            message_to_screen("Game over", red, -50, size="large")
            message_to_screen("Press C to play again or Q to quit", black, 50, size="medium")
            pygame.display.update()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.QUIT:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        gameLoop()
                elif event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tank_move = -5
                elif event.key == pygame.K_RIGHT:
                    tank_move = 5
                elif event.key == pygame.K_UP:
                    change_tur = 1
                elif event.key == pygame.K_DOWN:
                    change_tur = -1
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    damage = fire_shell(gun,main_tank_x, main_tank_y, current_tur_pos, fire_power, location_x, barrier_width, random_height, enemy_tank_x, enemy_tank_y)
                    enemy_health -= damage

                    possible_movement = ['f', 'r']
                    move_index = random.randrange(0,2)

                    for _ in range(random.randrange(0,10)):
                        if possible_movement[move_index] == 'f':
                            if display_width * 0.3 > enemy_tank_x:
                                enemy_tank_x += 5
                        elif possible_movement[move_index] == 'r':
                            if display_width * 0.03 < enemy_tank_x:
                                enemy_tank_x -= 5
                        

                        game_display.fill(white)
                        health_bars(player_health, enemy_health)
                        gun = tank(main_tank_x,main_tank_y, current_tur_pos)
                        enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, 8 )
                        fire_power += power_change
                        power(fire_power)   
                        barrier(location_x, random_height, barrier_width)
                        game_display.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])
                        pygame.display.update()
                        clock.tick(FPS)

                    damage = enemy_fire_shell(enemy_gun,enemy_tank_x, enemy_tank_y, 8, 50, location_x, barrier_width, random_height, main_tank_x, main_tank_y,)
                    player_health -= damage
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_move = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    change_tur = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0

        


        main_tank_x += tank_move

        current_tur_pos += change_tur

        if current_tur_pos > 8:
            current_tur_pos = 8
        elif current_tur_pos < 0:
            current_tur_pos = 0

        if main_tank_x - (tank_width/2) < location_x + barrier_width:
            main_tank_x += 5

        game_display.fill(white)
        health_bars(player_health, enemy_health)
        gun = tank(main_tank_x,main_tank_y, current_tur_pos)
        enemy_gun = enemy_tank(enemy_tank_x, enemy_tank_y, 8 )

        fire_power += power_change

        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power =1

        power(fire_power)
        
        barrier(location_x, random_height, barrier_width)
        game_display.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])

        pygame.display.update()

        if player_health < 1:
            end_game()
        elif enemy_health < 1:
            you_win()

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()