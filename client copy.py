# ===== Third-party libraries (need pip install) =====
# pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install pygame
import pygame

# ===== Python standard library (NO pip install needed) =====
from fileinput import filename
from xmlrpc import client
import time
import socket
import json
import os
import threading
from pathlib import Path
import base64

printed = None
printed_count = 1
def safe_print(line):
    global printed, printed_count
    if line != printed:
        print("\n"+line)
        printed = line
        printed_count = 1
    elif printed_count < 10000:
        printed_count += 1
        print(f'\033[2K\r{printed_count}', end="")


pygame.init()
window_width = 1100
window_height = 600

window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

style = {
    "header": { "color": (20, 20, 20), "width": 1, "height": 120, "link_width": "window", "link_height": None, "pos": (0, 0) },
    "sidebar": { "color": (30, 30, 30), "width": 200, "height": 0.8, "link_width": None, "link_height": "window", "pos": (0, 120) },
}
files = {
    "file1": { "default_color": (30, 30, 30), "color": None, "width": 200, "height": 60, "link_width": None, "link_height": None, "pos": (0, 120) },
    "file2": { "default_color": (30, 30, 30), "color": None, "width": 200, "height": 60, "link_width": None, "link_height": None, "pos": (0, 120) },
}

def container_hitbox_check(x, x_hitbox_start, x_hitbox_end, y, y_hitbox_start, y_hitbox_end): 
    if (
        x > x_hitbox_start - 5 and 
        x < x_hitbox_end + 5 and 
        y > y_hitbox_start - 5 and 
        y < y_hitbox_end + 5
        ):
        return True 
    else: 
        return False
def sidebar_hitbox_check(x,y): return True if x > style["sidebar"]["pos"][0] and x < style["sidebar"]["width"] +10 and y > style["sidebar"]["pos"][1] -10 and y < window_height else False
def file_hitbox_check(x,y,width,height,pos,file_number): return True if x > pos[0] and x < pos[0] + width and y > pos[1] + height * file_number and y < pos[1] + height + height * file_number else False
def file_sizing(el):
    width = files[el]["width"]
    height = files[el]["height"]
    pos = files[el]["pos"]
    return width, height, pos
def mouse_event():
    mouse_click = False
    while True:
        x, y = pygame.mouse.get_pos()

        # Hover event ================================================
        if sidebar_hitbox_check(x,y):
            file_number = 0
            for el in files:
                width, height, pos = file_sizing(el)

                if file_hitbox_check(x,y,width,height,pos,file_number):
                    safe_print("hovering "+ el)
                    new_color = (files[el]["default_color"][0]+20, files[el]["default_color"][1]+20, files[el]["default_color"][2]+20)
                    files[el]["color"] = new_color
                else:
                    files[el]["color"] = None
                file_number += 1

        # click sidebar event =========================================
        if pygame.mouse.get_pressed()[0] and not mouse_click:
            mouse_click = True
            if sidebar_hitbox_check(x,y):
                file_number = 0
                
                for el in files:
                    width, height, pos = file_sizing(el)

                    if file_hitbox_check(x,y,width,height,pos,file_number):
                        safe_print("Mouse clicked "+el)

                        if files[el]["default_color"] == (30, 30, 30):
                            for other in files:
                                if el != other:
                                    files[other]["default_color"] = (30, 30, 30)

                            new_color = (files[el]["default_color"][0]+20, files[el]["default_color"][1]+20, files[el]["default_color"][2]+20)
                            files[el]["default_color"] = new_color

                    file_number += 1
        elif not pygame.mouse.get_pressed()[0]:
            mouse_click = False

threading.Thread(target=mouse_event, daemon=True).start()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    window.fill((0, 0, 0))

    for el in style:
        color = style[el]["color"]
        width = style[el]["width"] if style[el]["link_width"] != "window" else window_width * style[el]["width"]
        height = style[el]["height"] if style[el]["link_height"] != "window" else window_height * style[el]["height"]
        pos = style[el]["pos"]

        pygame.draw.rect(window, color, (pos[0], pos[1], width, height))

    file_number = 0
    for el in files:
        color = files[el]["color"] if files[el]["color"] else files[el]["default_color"]
        width, height, pos = file_sizing(el)

        pygame.draw.rect(window, color, (pos[0], pos[1] + height * file_number, width, height))
        font = pygame.font.Font(None, 36)  # None = default font
        text_surface = font.render(el, True, (255, 255, 255))
        window.blit(text_surface, (pos[0], pos[1] + height * file_number))
        file_number += 1

    pygame.display.flip()