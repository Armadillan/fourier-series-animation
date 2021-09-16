#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

import numpy as np

VECTOR_COLOR = (220,220,220)
DRAWING_COLOR = (248,255, 60)
BACKGROUND = (30,30,30)
CIRCLE_COLOR = (100,100,100)
ORIGINAL_COLOR = (0,100, 0)


def complex_to_coord(num, flip=600):
    """
    Transform a complex number to pygame coordinate.

    Parameters
    ----------
    num : complex
        The complex number to transformm.
    flip : int, optional
        The height of the drawing, or the height of the original
        pygame window. That is, the maximum value that num.complex can
        have. Used to flip the coordinate over the x-axis to comply with
        how the pygame coordinate system works. The default is 600.

    Returns
    -------
    x : float
        The x-coordinate.
    y : float
        The y-coordinate.

    """
    x = num.real
    y = flip - num.imag
    return (x,y)


def animate(vectors,
            fps=60, time=10, ticks_per_frame=10,
            width=600, height=600,
            circles = True, original=None,
            delete=5
            ):
    """
    Animates the Fourier series "drawing"

    Parameters
    ----------
    vectors : vectors.Vectors
        The Vectors object to animate.
    fps : int, optional
        Maximum fps.
        The default is 60.
    time : int, optional
        Minimum time the animation should run in seconds.
        The default is 10.
    ticks_per_frame : int, optional
        How many line segments to compute very frame.
        The default is 10.
    width : int, optional
        The width of the original drawing.
        The default is 600.
    height : int, optional
        The height of the original drawing.
        The default is 600.
    circles : bool, optional
        Whether to draw the circles the vectors trace out.
        The default is True.
    original : iterable, optional
        List of the points of the original drawing, if you want it to be
        drawn on the background for reference. The default is None.
    delete : float, optional
        delete * fps / 60 future frames worth of line segments will be
        deleted in front of the tip of the vectors If set to 0, nothing is
        deleted. If set to a negative value, the whole drawing will be
        deleted at the start of each animation loop.
        The default is 5.

    Returns
    -------
    None.

    """
    pygame.init()

    pygame.display.set_caption(
        f"Animation with {vectors.num_vectors} "
        + f"vectors. (fps: {fps}, time: {time}, "
        + f"ticks: {ticks_per_frame})"
        )

    clock = pygame.time.Clock()
    ticks = fps * time * ticks_per_frame
    input_array = np.linspace(0,1, ticks, False)

    win = pygame.display.set_mode((width, height))
    win.fill(BACKGROUND)

    drawing_surface = win.copy()
    drawing_surface.set_colorkey(BACKGROUND)

    vector_surface = win.copy()
    vector_surface.set_colorkey(BACKGROUND)

    drawing_surface.fill(BACKGROUND)

    done = False

    while not done:

        drawing_points = []
        count=0

        if delete < 0:
            drawing_surface.fill(BACKGROUND)

        for i, x in enumerate(input_array):

            if count == ticks_per_frame -1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        done = True
                        break
                if done:
                    break


            previous = complex_to_coord(vectors(input_array[i-1]))

            vector_surface.fill(BACKGROUND)

            current = (0+0j)
            vector_points = []

            for vector in vectors:
                current += vector(x)
                coordinate = complex_to_coord(current)
                vector_points.append(coordinate)
                if len(vector_points) > 1 and circles:
                    pygame.draw.circle(
                        surface=vector_surface,
                        color=CIRCLE_COLOR,
                        center=vector_points[-2],
                        radius=abs(vector.coeff),
                        width=1)

            if count == ticks_per_frame - 1:

                drawing_points.append(coordinate)

                pygame.draw.lines(
                    vector_surface, VECTOR_COLOR, False, vector_points
                    )


                pygame.draw.lines(
                    surface=drawing_surface,
                    color=DRAWING_COLOR,
                    closed=False,
                    points=drawing_points
                    )

                #Reset stuff
                count = 0
                drawing_points = []

                win.fill(BACKGROUND)
                if original is not None:
                    pygame.draw.lines(win, ORIGINAL_COLOR, True, original)

                if delete > 0:
                    remove_list = []
                    for remove_index in range(
                            i, i + round(ticks_per_frame * delete * fps/60)
                            ):
                        try:
                            remove_list.append(
                                complex_to_coord(
                                    vectors(input_array[remove_index])
                                    )
                                )
                        except IndexError:
                            remove_list.append(
                                complex_to_coord(
                                    vectors(input_array[remove_index - ticks - 1])
                                    )
                                )

                    pygame.draw.lines(
                        surface=drawing_surface,
                        color=BACKGROUND,
                        closed=False,
                        points=remove_list
                        )


                win.blit(drawing_surface, (0,0))
                win.blit(vector_surface, (0,0))

                pygame.display.flip()
                clock.tick(fps)
            else:
                if count == 0:
                    drawing_points.append(previous)
                drawing_points.append(coordinate)
                count += 1
