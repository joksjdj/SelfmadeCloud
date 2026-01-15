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

pygame.init()
window_width = 1000
window_height = 600

window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

style = {
    "header": { "color": (20, 20, 20), "width": 1, "height": 120, "link_width": "window", "link_height": None, "pos": (0, 0) },
    "sidebar": { "color": (30, 30, 30), "width": 200, "height": 0.8, "link_width": None, "link_height": "window", "pos": (0, 120) },
}
files = {
    "files": { "color": (255, 255, 255), "width": 200, "height": 60, "link_width": None, "link_height": None, "pos": (0, 120) },
}

def mouse_hover():
    while True:
        x, y = pygame.mouse.get_pos()
        for el in files:
            width = files[el]["width"] if files[el]["link_width"] != "window" else window_width * files[el]["width"]
            height = files[el]["height"] if files[el]["link_height"] != "window" else window_height * files[el]["height"]
            pos = files[el]["pos"]
            if x > pos[0] and x < pos[0] + width and y > pos[1] and y < pos[1] + height:
                print("hovering")
threading.Thread(target=mouse_hover, daemon=True).start()

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

    for el in files:
        color = files[el]["color"]
        width = files[el]["width"] if files[el]["link_width"] != "window" else window_width * files[el]["width"]
        height = files[el]["height"] if files[el]["link_height"] != "window" else window_height * files[el]["height"]
        pos = files[el]["pos"]

        pygame.draw.rect(window, color, (pos[0], pos[1], width, height))

    pygame.display.flip()