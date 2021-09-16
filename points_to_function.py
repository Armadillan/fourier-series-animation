#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bisect import bisect
from copy import deepcopy

import numpy as np


def make_complex(points):
    """
    Makes a list of complex numbers from a list of points
    Treats y as the complex part.
    """
    
    return [complex(x, y) for x, y in points]


def get_x(L):
    """
    Gets equaly spaced numbers between 0 and 1
    to serve as inputs for outputs L.
    Returns a numpy.ndarray
    """

    return np.linspace(0, 1, num=len(L), endpoint=False)


def make_linear_function(p1,p2):
    """
    Returns the linear function defined by two points, p1 and p2
    For example make_linear_function((1,3), (2,5))
    returns the function f(x) = 2x + 1.
    """

    m = (p2[1]-p1[1])/(p2[0]-p1[0])

    k = p1[1] - p1[0] * m

    return lambda x: x * m + k

class Function:
    """
    Callable object to act as the final function.
    Takes two lists, input and output, as input to it's definition.
    Draws straight lines in between the points given in the input
    to define the function.

    Expects the domain of x_list to be 0 <= x < 1 (when defined)
    and the domain of the inputs to be 0 <= x <= 1 (when called)
    Where f(0) = f(1)
    """

    def __init__(self, x_list, y_list):

        # Adds the point (1, y[0])

        if not len(x_list) == len(y_list):
            raise ValueError("Arrays passed to Function() \
                             must be of equal size.")

        if isinstance(x_list, np.ndarray):
            self.x = np.append(x_list,1)
        else:
            self.x = deepcopy(x_list)
            self.x.append(1)

        if isinstance(y_list, np.ndarray):
            self.y = np.append(y_list, y_list[0])
        else:
            self.y = deepcopy(y_list)
            self.y.append(y_list[0])

        # List (dict) of line segments
        self.subfunctions = {}

        self.__num_points = len(x_list)

    @property
    def num_points(self):
        return self.__num_points

    def __call__(self,x):
        """
        Expects x <= 0 <= 1
        Where f(0) = f(1)
        """

        # Handles iterable inputs:
        # Maps function element and returns list
        try:
            return list(map(self, x))
        except TypeError:
            pass

        if not 0 <= x <= 1:
            raise ValueError(f"Expected 0 <= x <= 1, got x = {x}")

        # Tries to find value pre-defined (in function definition)
        try:
            return self.y[list(self.x).index(x)]
        except ValueError:
            pass

        # Finds which line segment x is in
        right_index = bisect(self.x, x)
        left_index = right_index - 1

        # Defines new line segment if that segment is not already defined
        if left_index not in self.subfunctions:
            self.subfunctions[left_index] = make_linear_function(
                (self.x[left_index], self.y[left_index]),
                (self.x[right_index], self.y[right_index])
            )

        # Evaluates the linear function of the
        # corresponding line segment at x
        return self.subfunctions[left_index](x)
