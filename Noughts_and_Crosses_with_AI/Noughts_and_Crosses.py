## Requires python3

import pygame
import random

current_zone = 0

zone_centrepoints = [(160,260), (400,260), (640,260), (160,500), (400,500), (640, 500), (160, 740), (400, 740), (640,740)]

boundaries = [(40, 280, 140, 380), (280, 520, 140, 380), (520, 760, 140, 380 ), (40, 280, 380, 620), (280, 520, 380, 620), (520, 760, 380, 620), (40, 280, 620, 860), (280, 520, 620, 860), (520, 760, 620, 860)]

zone_win_conditions = [(1,2,3), (1,4,7), (2,5,8), (3,6,9), (4,5,6), (7,8,9), (1,5,9), (3,5,7)]

def Create_Winner_Line(coord1, coord2, colour):
    pygame.draw.line(window, colour, coord1, coord2, line_thickness)


def Draw_cross(centrepoint, colour):
    
    pygame.draw.line(window, colour, (centrepoint[0] - 60, centrepoint[1] - 60),
        (centrepoint[0] + 60, centrepoint[1] + 60), 15)

    pygame.draw.line(window, colour, (centrepoint[0] + 60, centrepoint[1] - 60),
        (centrepoint[0] - 60, centrepoint[1] + 60), 15)

def Player_2_turn():
    evaluation_list = []
    iteration = 0
    largest_line = 3
    chosen_zone = 0

    for win_condition_list in zone_win_conditions:
        iteration += 1
        evaluation_list.append([])
        o_active_eval = []
        x_in_o_eval = False

        for x in win_condition_list:
            if(x in o_active_zones):
                o_active_eval.append(x)

            if(x in x_active_zones):
                x_in_o_eval = True

        if(len(o_active_eval) == 2 and x_in_o_eval == False):
            for x in win_condition_list:
                if(x in zones):
                                     
                    zones.remove(x)
                    o_active_zones.append(x)
            return True

        else: 
            for win_condition in win_condition_list:    
                
                if(win_condition in o_active_zones):
                    for x in range(1,5):
                        evaluation_list[iteration - 1].append(0)
                    break
                
                if(win_condition not in x_active_zones):
                    
                    evaluation_list[iteration - 1].append(win_condition)

    for entry in evaluation_list:
        
        
        if(len(entry) == largest_line):
            if(random.random() >= 0.5):
                chosen_entry = entry
        if(len(entry) < largest_line):
            chosen_entry = entry
            largest_line = len(chosen_entry)
       


    chosen_zone = random.choice(chosen_entry)
    zones.remove(chosen_zone)
    o_active_zones.append(chosen_zone)
    return True
        






def Valid_zone():     

    zone = 0

    mouse_pos = pygame.mouse.get_pos()

    for boundary in boundaries:
        
        zone += 1
        
        if(mouse_pos[0] >= boundary[0] and mouse_pos[0] <= boundary[1] and 
        mouse_pos[1] >= boundary[2] and mouse_pos[1] <= boundary[3]):
            break
        

    if(zone in zones):
        return zone
    
    else:
        return 0


    



pygame.init()

player1turn = True

run = True

line_thickness = 12

myfont = pygame.font.SysFont('timesnewromanboldttf', 30)

window = pygame.display.set_mode((800,900))

pygame.display.set_caption("Noughts & Crosses")

winner_evaluation_complete = False

player_1_winner = False

player_2_winner = False

tie = False

reveal_winner =  False

while run:

    zones = [1,2,3,4,5,6,7,8,9]

    x_active_zones = []

    o_active_zones = []

    

    game_finished = False

    while(game_finished == False):

        if(winner_evaluation_complete == False):
                for win_condition in zone_win_conditions:
                    if(win_condition[0] in x_active_zones and win_condition[1] in x_active_zones
                        and win_condition[2] in x_active_zones):
                            player_1_winner = True
                            print("player1")
                            line_coords = (zone_centrepoints[win_condition[0] - 1], zone_centrepoints[win_condition[2] - 1])
                            winner_colour = (0,0,200)
                            winner_evaluation_complete = True
                            reveal_winner = True
                            break
                    
                    if(win_condition[0] in o_active_zones and win_condition[1] in o_active_zones
                        and win_condition[2] in o_active_zones):
                            print("player2")
                            player_2_winner = True
                            line_coords = (zone_centrepoints[win_condition[0] - 1], zone_centrepoints[win_condition[2] - 1])
                            winner_colour = (200,0,0)
                            winner_evaluation_complete = True
                            reveal_winner = True
                            break

                    if(len(zones) <= 0):
                        reveal_winner = True


        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game_finished = True
        
        window.fill((255,255,255))
        pygame.draw.lines(window, (0,0,0), True, [(40, 140), (760, 140), (760, 860), (40, 860)], line_thickness)
        pygame.draw.line(window, (0,0,0), (280, 140), (280, 860), line_thickness)
        pygame.draw.line(window, (0,0,0), (520, 140), (520, 860), line_thickness)
        pygame.draw.line(window, (0,0,0), (40, 380), (760, 380), line_thickness)
        pygame.draw.line(window, (0,0,0), (40, 620), (760, 620), line_thickness)
        

        if(reveal_winner == False):
        
            if(player1turn):
                textsurface = myfont.render('Player 1\'s turn', False, (0, 0, 200))
            
            else:
                textsurface = myfont.render('Player 2\'s turn', False, (200, 0, 0))
            
            
            valid_zone = Valid_zone()
            
            
            if(player1turn == False):
                pygame.time.delay(1000)
                player1turn = Player_2_turn()
            
            if(valid_zone > 0 and player1turn):
                
                centrepoint = zone_centrepoints[valid_zone - 1]

                mouse_position = pygame.mouse.get_pos()


                if(mouse_position[0] > 40 and mouse_position[0] < 760 and mouse_position[1] > 140 and mouse_position[1] < 860):
                    Draw_cross(centrepoint, (122,122,122))

                if(pygame.mouse.get_pressed()[0]):
                    zones.remove(valid_zone)
                    x_active_zones.append(valid_zone)
                    player1turn = False
            
        
        if(reveal_winner == True):
            
            
            if(player_2_winner == False and player_1_winner == False):
                tie = True
                winner_evaluation_complete = True
            
            if(player_1_winner):
                textsurface = myfont.render('Player 1 Wins!', False, (0, 0, 200))
                Create_Winner_Line(line_coords[0], line_coords[1], winner_colour)

            if(player_2_winner):
                textsurface = myfont.render('Player 2 Wins!', False, (200, 0, 0))
                Create_Winner_Line(line_coords[0], line_coords[1], winner_colour)

            if(tie):
                textsurface = myfont.render('It\'s a tie!', False, (0, 0, 0))

        for zone in x_active_zones:
            Draw_cross(zone_centrepoints[zone - 1], (0, 0, 150))

        for zone in o_active_zones:
            pygame.draw.circle(window, (150, 0, 0), zone_centrepoints[zone - 1], 60)
            pygame.draw.circle(window, (255, 255, 255), zone_centrepoints[zone - 1], 40)


        window.blit(textsurface,(40,80))


        pygame.display.update()

pygame.quit()