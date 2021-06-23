from itertools import islice


def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    x = [1,2,3,4,5,4,3,2,5,6]
    print(len(x))
    print(nth_index(x, 3, 1))

if __name__ == "__main__":
    main()
