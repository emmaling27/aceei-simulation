import sys
import numpy as np

def main(args):
    n = 4 # Number of students
    caps = [2, 2]
    utilities = np.random.random_integers(0, 100, (n, 2))
    budgets = np.random.uniform(9, 11, n)
    prices = [11, 11]
    # Use integer program to get the clearing prices

    # for x in prices:

# def allocate(utilities, caps, budgets, prices):


if __name__ == "__main__":
    main(sys.argv)