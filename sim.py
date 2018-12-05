import sys
import numpy as np
import cvxpy as cp


def main():
    n = 4 # Number of students
    caps = [2, 2]
    utilities = np.random.random_integers(0, 100, (n, 2))
    budgets = np.random.uniform(9, 11, n)
    prices = [11, 11]
    # Use integer program to get the clearing prices
    allocation = np.zeros((n, 2))
    cleared_bool = clearing(np.sum(allocate(utilities, caps, budgets, prices, n), axis=0))
    # Find clearing prices
    while not np.all(cleared_bool):
        if not cleared_bool[0]:
            prices[0] -= .1
            cleared_bool = clearing(np.sum(allocate(utilities, caps, budgets, prices, n), axis=0))
        if not cleared_bool[1]:
            prices[1] -= .1
            cleared_bool = clearing(np.sum(allocate(utilities, caps, budgets, prices, n), axis=0))

    # Prices should now be clearing
    allocation = allocate(utilities, caps, budgets, prices)

    # instructor_prefs = np.random.uniform(.1, 2, (n, 2))
    # print("Instructor Preferences: {}".format(instructor_prefs))
    # prices = np.repeat(prices, n, axis=0) * instructor_prefs
    # Allocate again at new prices
    print("Clearing prices: {}".format(prices))
    print("Utilities: {}".format(utilities))
    print("Budgets: {}".format(budgets))
    print("Allocation: {}".format(allocation))

    # for x in prices:
def clearing(allocation_sums):
    clearing_arr = np.array([False, False])
    for i in range(2):
        if allocation_sums[i] >= min(np.count_nonzeros(utilities[:][i]), caps[i]):
            clearing_arr[i] = True
    return clearing_arr


def allocate(utilities, caps, budgets, prices, n):
    # Creates course allocation variable matrix with Boolean entries
    alloc = cp.Variable((n, 2), boolean=True)
    print(alloc)
    enrollment = cp.sum(alloc, axis=0)
    # enrollment = cp.sum_entries(np.array(alloc), axis=0)
    print(enrollment)
    capacity_constraint = enrollment <= caps
    prices = np.repeat([prices], n, axis=0)
    print(prices.shape)
    payments = cp.multiply(alloc, prices)
    budget_constraint = payments <= budgets
    total_util = utilities * alloc
    problem = cp.Problem(cp.Maximize(total_util), [capacity_constraint, budget_constraint])
    solution = problem.solve()

    return solution

if __name__ == "__main__":
    # main(sys.argv)
    main()
