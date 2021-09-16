#!/usr/bin/env python
# -*- coding: utf-8 -*-

import drawing
import animation
import get_coefficients
import points_to_function
import vectors

# Defines the dimensions of the drawing
WIDTH = 600
HEIGHT = 600

# Gets points from drawing (input)
points_in = drawing.main(WIDTH, HEIGHT)

# Converts to list of complex numbers
complex_points = points_to_function.make_complex(points_in)

# Gets input values for those numbers
x = points_to_function.get_x(complex_points)

# Creates the function
f = points_to_function.Function(x, complex_points)

# Sets tolerances and limit for integration step
epsrel = 1e-1
epsabs = 2
limit = 500

# Computes coefficients for integration step
# 41 vectors in this case
# "verbose" means it will print progress to console.
coeffs = get_coefficients.get_coefficients(
            f, 20, verbose=True, epsrel=epsrel, epsabs=epsabs, limit=limit
            )

# Creates the Vectors object
vectors_obj = vectors.Vectors(coeffs)

# Creates a list of points (pygame coordinates) for the original drawing
# (Converts y-coordinates to pygame coordinates by
# subtracting them from the height
original = [(x, HEIGHT - y) for x, y in points_in]

# Animates it all:
# needs the "Vectors" object

# "time" is the MINIMUM time of the animation in seconds
# "fps" is MAXIMUM frames per seconds
# "ticks_per_frame" is how many line segments to
# compute every frame
# Increasing any of them increases the quality of the drawing
# Defaults are 60, 10, 10, respectively.

# I recommend using higher fps with lower ticks_per_frame
# and lowering ticks_per_frame when increasing time.
# Use higher ticks_per_frame when using low time or
# low fps.

# "ticks_per_frame" is what you increase to get better
# animations, if your computer can handle it.
# If more fps doesn't make a difference and you don't
# want the animation to be any slower.

# WIDTH and HEIGHT
# MUST be the same as the original pygame window
# so the same as in "dpffs.main(WIDTH, HEIGHT)"

# "original" is the points from the original drawing,
# to put "behind" the drawing, for reference.
# If none are given, just doesn't draw the original.

# "circles" is whether to draw circles around
# each vector (the path the vector traces out).

# "delete" works this way:
# if delete < 0, the whole drawing will be deleted
# at the start of every loop (redrawing every time)
# if delete = 0, nothing will be deleted,
# if delete > 0, delete * fps/60 (i.e. delete at 60 fps,
# 2 * delete at 120 fps, 0.5 * delete at 30 fps etc)
# frames worth of line will be deleted in front of
# the end of the vectors every frame, for aesthetic reasons.
# I recommend a value between 5 and 10

animation.animate(
    vectors_obj,
    time=10,
    fps=60,
    ticks_per_frame=20,
    width=WIDTH,
    height=HEIGHT,
    original=original,
    circles = True,
    delete=7
    )
