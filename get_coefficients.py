#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quadpy import quad
from quadpy.c1._adaptive import IntegrationError

import numpy as np

# Remove this?
# Or use to default to bounds 0, 1?
def integral(
        f, a, b, epsrel=1.49e-08, epsabs=1.49e-08, limit=50):
    """
    Computes definite integral of function f over the interval from a to b.
    Equivalent to quadpy.quad(f, a, b)[0].
    The tolerances and limit can be adjusted to adjust speed/accuracy balance.
    """

    return quad(f, a, b, epsrel=epsrel, epsabs=epsabs, limit=limit)[0]


def get_coefficients(
        f, num, verbose=False, epsrel=1.49e-08, epsabs=1.49e-08, limit=50):
    """
    Gets the coefficients for function f for num pairs of vectors
    and vector 0.
    Returns dict of size 2 * num + 1

    For example num=2 returns the coefficients for vectors
    -2, -1, 0, 1, 2 like so:
    {0: complex, 1: complex, 2: complex, -1: complex, -2: complex}

    The tolerances and limit for the integration
    can be changed to adjust speed/accuracy balance.
    """

    coefficients = {}

    max_len = len(str(num))+1

    for vector in range(-num, num+1):


        # Multiply the function by a constant before integration
        # so that the resulting function is f(x) * e**-2vector*pi*i*x
        # and the integral is the coefficient of the vecotor.
        integrand = lambda x: f(x) * np.exp(vector * -2 * np.pi * (1j) * x)

        while True:
            try:
                coeff = integral(
                    integrand, 0, 1, epsrel=epsrel, epsabs=epsabs, limit=limit)
            except IntegrationError:
                if verbose:
                    print(f"Vector {vector} failed integration with",
                          f"epsrel: {epsrel} epsabs: {epsabs} limit: {limit}")
                epsrel *= 10
                epsabs *= 10
                limit += 1000
                if verbose:
                    print(f"Continuing with with epsrel: {epsrel} epsabs:",
                          f"{epsabs} limit: {limit}\n")
                continue
            else:
                break

        coefficients[vector] = coeff

        if verbose:
            print(f"{str(vector).zfill(max_len)}, {str(vector + num + 1).zfill(max_len - 1)}/{str(2*num + 1)}:",
                  f"{((vector+num+1)/(2 * num+1) * 100):2.2f}%")

    return coefficients
