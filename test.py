from itertools import islice
import numpy as np

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    x = np.zeros(48, dtype=float)
    y = list(range(18,66))
    print(len(y))
    print(x)


if __name__ == "__main__":
    main()
