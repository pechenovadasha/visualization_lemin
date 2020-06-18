# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    visual.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: croxane <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/02 12:35:42 by croxane           #+#    #+#              #
#    Updated: 2020/03/07 12:28:32 by croxane          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import os
import time
import pygame
import sys
from pygame.locals import *

WIDTH = 1200
HIGH = 500
FPS = 60
SIZE_HOUSE = 200

if len(sys.argv) != 3:
    print("Usage: python3 visual.py <lem-in> <map>")
    exit()
f = os.popen('./' + sys.argv[1] + '<' + sys.argv[2])
if f:
    rd = f.read().split('\n')
    f.close()
else:
    print("Error")
    exit()
if len(rd) == 0:
    exit()
l_connection = []
l_way = []
d = dict()
d["ants"] = rd[0]
del rd[0]
k = 0
for i in range(len(rd)):
    if rd[i] == "##start":
        d["start"] = rd[i + 1]
    elif rd[i] == "##end":
        d["end"] = rd[i + 1]
    elif rd[i].find('#') != -1:
        i += 1
    elif rd[i].find('-') != -1 and rd[i].find(' -') == -1 and rd[i][0] != 'L':
        l_connection.append(rd[i])
    elif rd[i].find('-') != -1 and rd[i][0] == 'L':
        l_way.append(rd[i])
    elif rd[i] != '' and rd[i - 1] != "##start" and rd[i - 1] != "##end":
        d[k] = rd[i]
        k += 1
    i += 1
if d.get('start') is None or d.get('end') is None:
    print("Error")
    exit()
start = []
end = []
start.append(d["start"].split(' '))
end.append(d["end"].split(' '))
listik = []
conectic = []
for i in d:
    if i != 'ants':
        listik.append(d[i].split(' '))
for i in range(len(l_connection)):
    conectic.append(l_connection[i].split('-'))
max_x = 0
max_y = 0
zoom_x = 0
zoom_y = 0
min = int(listik[0][1])
for i in range(len(listik)):
    if min > int(listik[i][1]):
        min = int(listik[i][1])
    if min > int(listik[i][2]):
        min = int(listik[i][2])
if min < 0:
    for i in range(len(listik)):
        listik[i][1] = int(listik[i][1]) + min * (-1)
        listik[i][2] = int(listik[i][2]) + min * (-1)

for i in range(len(listik)):
    if max_x < int(listik[i][1]):
        max_x = int(listik[i][1])
    if max_y < int(listik[i][2]):
        max_y = int(listik[i][2])

if max_x != 0:
    zoom_x = (WIDTH - SIZE_HOUSE) / max_x
if max_y != 0:
    zoom_y = (HIGH - SIZE_HOUSE) / max_y
str0 = []
str1 = []
for i in range(len(l_way)):
    str0.append(l_way[i].split(' '))
for i in range(len(str0)):
    for j in range(len(str0[i])):
        str1.append(str0[i][j].split('-'))
for i in range(len(listik)):
    listik[i][1] = int(listik[i][1]) * zoom_x + 80
    listik[i][2] = int(listik[i][2]) * zoom_y + 80
a = [0] * (len(str1))
for i in range(len(str1)):
    a[i] = [0] * 2
mass = [0] * (len(str1))
for i in range(len(str1)):
    mass[i] = [0] * 4
for i in range(len(str1)):
    j = i - 1
    flag = 0
    while j >= 0:
        if str1[j][0] == str1[i][0]:
            last_step = str1[j][1]
            flag = 1
            break
        j -= 1
    if flag == 0:
        last_step = start[0][0]
    a[i][0] = last_step
    a[i][1] = str1[i][1]
for i in range(len(a)):
    for j in range(len(listik)):
        if a[i][0] == listik[j][0]:
            mass[i][0] = listik[j][1]
            mass[i][1] = listik[j][2]
        if a[i][1] == listik[j][0]:
            mass[i][2] = listik[j][1]
            mass[i][3] = listik[j][2]
pygame.init()
FPS = 60
sc = pygame.display.set_mode((WIDTH, HIGH + 300))
table = pygame.transform.scale(pygame.image.load('sources/gazon.png'), (WIDTH, HIGH))
sc.blit(table, (0, 0))
plate = pygame.transform.scale(pygame.image.load('sources/domik.png'), (200, 200))
clock = pygame.time.Clock()
beetle = pygame.image.load('sources/ant.png')
beetle = pygame.transform.scale(beetle, (70, 100))
x = int(start[0][1]) * zoom_x + 80
y = int(start[0][2]) * zoom_y + 80
xe = int(end[0][1]) * zoom_x + 80
ye = int(end[0][2]) * zoom_y + 80
ant = int(d['ants'])
ant_end = 0
# Initialize variables for text
font_start = pygame.font.Font('sources/font2.otf', 36)
text_start = font_start.render("Start", 1, (0, 0, 0))
place_start = text_start.get_rect(center=(x + 10, y + 80))
text_end = font_start.render("End", 1, (0, 0, 0))
place_end = text_end.get_rect(center=(xe + 10, ye + 80))
# Initialize variables for the menu
text_ant = font_start.render("Number of ants in the start = " + str(ant), 1, (255, 255, 255))
place_ant = text_ant.get_rect(topleft=(10, HIGH + 100))
text_ant_end = font_start.render("Number of ants in the end = " + str(ant_end), 1, (255, 255, 255))
place_ant_end = text_ant_end.get_rect(topleft=(10, HIGH + 200))
text_option0 = font_start.render("Tap 1 or 0 if you want to change the theme", 1, (255, 255, 255))
place_op0 = text_option0.get_rect(topleft=(WIDTH/4, HIGH + 10))
text_option1 = font_start.render("Tap '+' or '-' to control the speed", 1, (255, 255, 255))
place_op1 = text_option1.get_rect(topleft=(WIDTH/2, HIGH + 100))
text_option2 = font_start.render("Tap space to stop the movement for a second", 1, (255, 255, 255))
place_op2 = text_option2.get_rect(topleft=(WIDTH/2, HIGH + 200))
number_steps = len(mass)
j = 0
step_x = 0
step_y = 0
counter = 0
SPEED = 50
x_begin = 0
y_begin = 0
x_begin_end = 0
y_begin_end = 0
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_KP_PLUS and SPEED > 5:
                SPEED -= 5
            elif i.key == pygame.K_KP_MINUS and SPEED < 915:
                SPEED += 5
            elif i.key == pygame.K_SPACE:
                pygame.time.delay(1000)
            elif i.key == pygame.K_1:
                table = pygame.transform.scale(pygame.image.load('sources/space.png'), (WIDTH, HIGH))
                plate = pygame.transform.scale(pygame.image.load('sources/hole.png'), (200, 200))
                beetle = pygame.image.load('sources/asteroid.png')
                beetle = pygame.transform.scale(beetle, (70, 100))
            elif i.key == pygame.K_0:
                table = pygame.transform.scale(pygame.image.load('sources/gazon.png'), (WIDTH, HIGH))
                plate = pygame.transform.scale(pygame.image.load('sources/domik.png'), (200, 200))
                beetle = pygame.image.load('sources/ant.png')
                beetle = pygame.transform.scale(beetle, (70, 100))
    sc.fill((0, 0, 0))
    for i in range(len(conectic)):
        for k in range(len(listik)):
            if conectic[i][0] == listik[k][0]:
                x_begin = listik[k][1]
                y_begin = listik[k][2]
            if conectic[i][1] == listik[k][0]:
                x_begin_end = listik[k][1]
                y_begin_end = listik[k][2]
        pygame.draw.line(table, (0, 0, 0), [x_begin + 40, y_begin + 40], [x_begin_end + 40, y_begin_end + 40], 3)
    for i in range(len(listik)):
        table.blit(plate, (listik[i][1] - 80, listik[i][2] - 80))
        if listik[i][0] == start[0][0]:
            table.blit(text_start, place_start)
        elif listik[i][0] == end[0][0]:
            table.blit(text_end, place_end)
    sc.blit(table, (0, 0))


    text_ant = font_start.render("Number of ants in the start = " + str(ant), 1, (255, 255, 255))
    place_ant = text_ant.get_rect(topleft=(10, HIGH + 100))
    sc.blit(text_ant, place_ant)
    text_ant_end = font_start.render("Number of ants in the end = " + str(ant_end), 1, (255, 255, 255))
    place_ant_end = text_ant_end.get_rect(topleft=(10, HIGH + 200))
    sc.blit(text_ant_end, place_ant_end)
    sc.blit(text_option0, place_op0)
    sc.blit(text_option1, place_op1)
    sc.blit(text_option2, place_op2)
    if number_steps > j:
        step_x = (mass[j][2] - mass[j][0]) / SPEED
        step_y = (mass[j][3] - mass[j][1]) / SPEED
        if counter != SPEED:
            sc.blit(beetle, ((mass[j][0] + step_x * counter), (mass[j][1] + step_y * counter)))
            counter += 1
        if counter >= SPEED:
            if mass[j][0] == x and mass[j][1] == y:
                ant -= 1
            if mass[j][2] == xe and mass[j][3] == ye:
                ant_end += 1

            j += 1
            counter = 0
    pygame.display.update()
    clock.tick(FPS)
