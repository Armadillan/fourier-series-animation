#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Vectors:
    """
    Holds all the vectors.
    Can be called as a function
    """
    class Vector:
        """
        An individual vector
        """
        def __init__(self, rate, coefficient):
            self.__function = lambda t: (
                coefficient * np.exp(rate * 2 * np.pi * (1j) * t)
                )
            self.__rate = rate
            self.__coefficient = coefficient

        def __call__(self, t):
            return self.__function(t)

        @property
        def coefficient(self):
            return self.__coefficient

        coeff = coefficient

        @property
        def rate(self):
            return self.__rate

    # Vectors class definitions

    def __init__(self, coefficients):
        self.__vectors = {}
        for key, val in coefficients.items():
            self.__vectors[key] = self.Vector(key, val)
            self.__coefficients = coefficients

    def __call__(self, t):
        out = complex()
        for vector in self.__vectors.values():
            out += vector(t)
        return out

    def __getitem__(self, vector):
        return self.__vectors[vector]

    def __iter__(self):
        self.__iter_key = 0
        self.__iter_negative = False
        return self

    def __next__(self):
        if self.__iter_key == 0:
            out = self.__vectors[0]
            self.__iter_key += 1
            return out
        if self.__iter_key <= 0.5 * (self.num_vectors - 1):

            if self.__iter_negative:
                out = self.__vectors[-self.__iter_key]
                self.__iter_negative = False
                self.__iter_key += 1
                return out

            self.__iter_negative = True
            return self.__vectors[self.__iter_key]
        raise StopIteration


    @property
    def num_vectors(self):
        return len(self.__vectors)

    @property
    def coefficients(self):
        return self.__coefficients

    coeffs = coefficients
