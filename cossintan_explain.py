from turtle import color, right
from numpy import deg2rad
import pygame

import matplotlib as plt
import os
from time import time, sleep
import time
import pygame
from math import *
from screen.create import *
from screen.calc import *
from settings.settings import *

def factorial(number):
    value = 1
    for i in range(1, number + 1):
        value = value * i
    return value

def calc_sin(radians, precision=4):
    value = float(radians)
    for i in range(1, precision):
        value += (radians**(1 + 2 * i)) / factorial(2 * i + 1) * (-1)**i
    return value

def calc_cos(radians, precision=4):
    value = 1.0
    for i in range(1, precision):
        value += (radians**(2 * i)) / factorial(2 * i) * (-1)**i
    
    return value

# tan(x) = sin(x) / cos(x) 
# (x^(1 + 2n)) / (1 + 2n)! / x^(2n) / (2n)!
# (x^(2 + 2n) * (2n)!) / (x^(2n) * (1 + 2n)!)
# x * (2n)! / (1 + 2n)!
def calc_tan(radians, precision=4):
    value = float(radians)
    for i in range(1, precision):
        value = (value * factorial(2 * i)) / factorial(1 + 2 * i)
    return value

#mouse States
mousePressed = False 
leftMousePressed = False 
middleMousePressed = False 
rightMousePressed = False 



#game loop
running = True
clock = pygame.time.Clock()

#point on circle
currentCircleDegree = 60
graphPoints = []
circle_precision = 10

for i in range(circle_precision):
    graphPoints.append({})
    for i2 in range(360):
        graphPoints[-1][str(i2)] = None

#run gui till the program is quitted
while running:
    #setup for frame time calculation
    StartTime = time.time()
    time_delta = clock.tick(60)/1000.0

    #set the screen size if it has changed
    screenX = screen.get_size()[0]
    screenY = screen.get_size()[1]
    simFieldX1 = 10
    simFieldY1 = 10
    simFieldX2 = screen.get_width() / (screenlayout[0][0] + screenlayout[2][0]) * screenlayout[0][0]
    simFieldY2 = -10 + screen.get_height()  / (screenlayout[0][1] + screenlayout[1][1]) * screenlayout[0][1]
    screenXYratio = (simFieldY2 - simFieldY1) /  (simFieldX2 - simFieldX1)
    simFieldOrigin = ((simFieldX2 - simFieldX1) / 2, (simFieldY2 - simFieldY1) / 2)
    #event loop
    for event in pygame.event.get():

        #stop the program if someone exits
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(str(pygame.mouse.get_pos()) + str((calc_pixel_to_game_coords(pygame.mouse.get_pos()[0]), calc_pixel_to_game_coords(y=pygame.mouse.get_pos()[1]))))
            mousePressed = True
        
            state = pygame.mouse.get_pressed()
            #state = (leftclick, middleclick, rightclick) = (0, 0, 0)
            if state[0] == True:
                leftMousePressed = True
            elif state[1] == True:
                middleMousePressed = True
            elif state[2] == True:
                rightMousePressed = True

                

            #setup for draw arrow creation
            last_mous_clickpos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            selected_an_obj = False
            last_click_selected_obj = False
            mouseHoldLength = 0

            #set the start of the arrow if a player drags in an open space (or on an object)
            click_arrow_start = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            
        if event.type == pygame.MOUSEBUTTONUP:
            leftMousePressed = False 
            middleMousePressed = False
            rightMousePressed = False
            mousePressed = False

    #mouse pressed loop actions        
    if leftMousePressed == True:
        currentCircleDegree += 1
    if rightMousePressed == True:
        currentCircleDegree -= 1 
    
    
    
    #cossintan explenation
    circle_diameter = simFieldY1 + simFieldY2 / simfieldsizex
    pixel_to_radian = simFieldY1 + simFieldY2 / simfieldsizex - 2
    circle_center = ((simFieldX1 + simFieldX2) / 2, (simFieldY1 + simFieldY2) / 2)


    currentCircleDegree = currentCircleDegree % 360
    currentCircleRadian = (currentCircleDegree) * (pi/180) 
    
    triangleTan = calc_tan(currentCircleRadian, circle_precision)
    triangleSin = calc_sin(currentCircleRadian, circle_precision)
    triangleCos = calc_cos(currentCircleRadian, circle_precision)

    # x/y = sin(traingleSin)
    # sqrt(x**2 + y**2 = 1)
    # y = x / traingleSin
    # sqrt(x**2+ (x/triangleSin)**2)
    #onCirclePointX = sqrt(1 / (triangleTan**2 + 1))
    # sqrt((triangle * y)**2 + x**2)
    #onCirclePointY = sqrt(1 / (triangleTan**-2 + 1))
    
    circleTrianglePoint = (circle_center[0] + pixel_to_radian * triangleCos, circle_center[1] - pixel_to_radian * triangleSin)    
    
    circlePoint = (circle_center[0] + circle_diameter / 2, )

    #clear screen
    screen.fill((0, 0, 0))    
    
    #menu settings
    object_settings = [{'degrees': currentCircleDegree,
                       'radians' : currentCircleRadian,
                       'cos(radians)' :triangleCos,
                       'sin(radians)' :triangleSin,
                       'tan(radians)' :triangleTan,}]

    #menu blocks
    #setting menu
    #right
    rightMenuX1 = 20 + (screen.get_width() - 20) / (screenlayout[0][0] + screenlayout[2][0]) * screenlayout[0][0]
    rightMenuY1 = 10
    rightMenuX2 = rightMenuX1 - 10 + (screen.get_width() - 20) / (screenlayout[0][0] + screenlayout[2][0]) * screenlayout[2][0]
    rightMenuY2 = screen.get_height() - 10

    #under
    underMenuX1 = 10
    underMenuY1 = 20 + screen.get_height()  / (screenlayout[0][1] + screenlayout[1][1]) * screenlayout[0][1]
    underMenuX2 = screen.get_width() / (screenlayout[0][0] + screenlayout[2][0]) * screenlayout[0][0]
    underMenuY2 = screen.get_height() - 10

    #draw the menu's
    create_rectangle((simFieldX1, simFieldY1),(simFieldX2, simFieldY2))
    create_menu((rightMenuX1, rightMenuY1), (rightMenuX2, rightMenuY2), divisions=[1], names=['Data'], isVertical=True, settings=object_settings)
    
    #grafiek
    create_line(((simFieldX1 + simFieldX2) / 2, simFieldY1), ((simFieldX1 + simFieldX2) / 2, simFieldY2), width=3)
    create_line((simFieldX1,(simFieldY1 + simFieldY2) / 2) , (simFieldX2, (simFieldY1 + simFieldY2) / 2), width=3)
    
    #draw circle stuff 
    create_circle(center = circle_center, radius = circle_diameter, width = 3)
    
    #draw_explain_data
    #draw triangle in circle
    for precision in range(circle_precision, 1, -1):

        triangleTan = calc_tan(currentCircleRadian, precision)
        triangleSin = calc_sin(currentCircleRadian, precision)
        triangleCos = calc_cos(currentCircleRadian, precision)
        
        circleTrianglePoint = (circle_center[0] + pixel_to_radian * triangleCos, circle_center[1] - pixel_to_radian * triangleSin)    
    
        create_line((circleTrianglePoint[0], circle_center[1]), circleTrianglePoint, color = (0, 0, 255 * (precision / circle_precision)))
        create_line(circle_center, (circleTrianglePoint[0], circle_center[1]), color = (0, 255 * (precision / circle_precision), 0))
        if precision == circle_precision:
            create_line(circle_center, circleTrianglePoint, color = (255 * (precision / circle_precision), 0, 0))
        create_text(precision, circleTrianglePoint, color = green)
        
        graphPoints[precision - 1][str(currentCircleDegree)] = circleTrianglePoint
        
        currentGraph = list(graphPoints[precision - 1].values())
        
        for pointIndex in range(359):
            if currentGraph[pointIndex] != None:
                if currentGraph[pointIndex + 1] != None:
                    create_line(currentGraph[pointIndex], currentGraph[pointIndex + 1], color=(150 * (precision / circle_precision), 150 * (precision / circle_precision), 150 * (precision / circle_precision)))
        
        

    triangleTan = calc_tan(currentCircleRadian, circle_precision)
    triangleSin = calc_sin(currentCircleRadian, circle_precision)
    triangleCos = calc_cos(currentCircleRadian, circle_precision)

    circleTrianglePoint = (circle_center[0] + pixel_to_radian * triangleCos, circle_center[1] - pixel_to_radian * triangleSin)    
    
    
    create_point(circleTrianglePoint, 4, 4, color=green)

    #draw triangle data
    create_text('A', circle_center, color = liteblue)    
    create_text('B', (circleTrianglePoint[0], circle_center[1]), color = red)
    create_text('C', circleTrianglePoint, color = green)

    #update menus
    pygame.display.flip()
    #manager.draw_ui(screen)

    #counts total simulation steps
    TotalSteps = TotalSteps + 1

    #draw the entire picture to the screen
    pygame.display.update()

    #calculate simulation time
    EndTime = time.time()

    TotalIRLTime = TotalIRLTime + (time.time() - StartTime)
