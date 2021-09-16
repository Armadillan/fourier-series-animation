#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time

def main(width, height):

    pygame.init()
    pygame.display.set_caption("Draw! Press space when done")

    points =[]

    win = pygame.display.set_mode((width, height))
    win.fill("#FFFFFF")
    pygame.display.flip()

    over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
        if pygame.mouse.get_pressed()[0] and not over:
            mouse_pos = pygame.mouse.get_pos()
            if points:
                pygame.draw.line(
                    win,
                    "#000000",
                    mouse_pos,
                    points[-1],
                    2,
                    )
                pygame.display.flip()
            points.append(mouse_pos)
        elif pygame.key.get_pressed()[pygame.K_SPACE]:
            if over:
                pygame.quit()
                return [(x, height - y) for x, y in points]
            else:
                over = True
                pygame.draw.line(
                    win,
                    "#000000",
                    points[-1],
                    points[0],
                    2,
                )
                pygame.display.flip()
                pygame.display.set_caption(
                    "Done! Press space again to start computation"
                    )
                time.sleep(.1)

# added check here /Antoni
if __name__ == "__main__":
    a = main(600, 600)
    print(a)