from itertools import islice
from AdditionalFunctions import TieBreakerProbability
import numpy as np
import matplotlib.pyplot as plt
import csv

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    # Test stuff:
    x = [1,4,5,6]

if __name__ == "__main__":
    main()
