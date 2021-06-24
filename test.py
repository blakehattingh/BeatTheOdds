from itertools import islice
import numpy as np

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    x = np.array([1,2,3])
    y = np.array([4,5,6])
    y = np.append([y], [x], axis = 1)

    dist = []
    x1 = [1,2,3]
    y1 = [4,5,6]
    dist.append(x1)
    dist.append(y1)
    print(dist)

if __name__ == "__main__":
    main()
