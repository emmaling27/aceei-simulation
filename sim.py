import sys
import numpy as np
import cvxpy as cp


def main():
    n = 4 # Number of students
    caps = [2, 2] # Capacities of two courses
    utilities = np.array([[100, 0], [0, 100], [100, 90], [75, 100]])
    # utilities = np.random.random_integers(0, 100, (n, 2))
    budgets = np.random.uniform(9, 11, n)
    prices = np.repeat([[11,11]], n, axis=0)
    allocation = np.zeros((n, 2))
    print("Clearing prices: {}".format(prices))
    print("Utilities: {}".format(utilities))
    print("Budgets: {}".format(budgets))
    run_course_match(n, caps, utilities, budgets, prices, None)
    # Generate instructor preferences
    instructor_prefs = np.array([[1, .1], [.1, 1], [2, 1], [1, 2]])
    # instructor_prefs = np.random.uniform(.1, 2, (n, 2))
    print("Instructor Preferences: {}".format(instructor_prefs))
    run_course_match(n, caps, utilities, budgets, prices, instructor_prefs)

def run_course_match(n, caps, utilities, budgets, prices, instructor_prefs=None):

    # Find initial clearing prices
    prices = adjust_prices(utilities, caps, budgets, prices, n)
    print("Prices w/o prefs: {}".format(prices))
    # Prices should now be clearing
    allocation = allocate(utilities, caps, budgets, prices, n)
    print("Allocation w/o prefs: {}".format(allocation))
    # Generate instructor preferences
    if instructor_prefs is not None:
        prices = prices * instructor_prefs
        prices = adjust_prices(utilities, caps, budgets, prices, n)
        print("Instructor pref prices: {}".format(prices))
        allocation = allocate(utilities, caps, budgets, prices, n)
        print("Instructor prefs allocation: {}".format(allocation))
    return allocation

def adjust_prices(utilities, caps, budgets, prices, n):
    """return the new prices"""
    cleared_bool = clearing(np.sum(allocate(utilities, caps, budgets, prices, n), axis=0), utilities, caps)
    # Find clearing prices
    while not np.all(cleared_bool):
        if not cleared_bool[0]:
            for i in range(n):
            	prices[i][0] -= .1
            cleared_bool = clearing(np.sum(allocate(utilities, caps, budgets, prices, n), axis=0), utilities, caps)
        if not cleared_bool[1]:
            for i in range(n):
            	prices[i][1] -= .1
            cleared_bool = clearing(np.sum(allocate(utilities, caps, budgets, prices, n), axis=0), utilities, caps)
    return prices


def clearing(allocation_sums, utilities, caps):
    clearing_arr = np.array([False, False])
    nonzeros = np.count_nonzero(utilities, axis=0)
    for i in range(2):
        if allocation_sums[i] >= min(nonzeros[i], caps[i]):
            clearing_arr[i] = True
    return clearing_arr


def allocate(utilities, caps, budgets, prices, n):
    # Creates course allocation variable matrix with Boolean entries
    alloc = cp.Variable((n, 2), boolean=True)
    enrollment = cp.sum(alloc, axis=0)
    capacity_constraint = enrollment <= caps
    payments = cp.sum(cp.multiply(alloc, prices), axis=1)
    budget_constraint = payments <= budgets
    total_util = cp.sum(cp.multiply(utilities, alloc))
    problem = cp.Problem(cp.Maximize(total_util), [capacity_constraint, budget_constraint])
    problem.solve()
    for var in problem.variables():
        solution = var.value
    if solution is None:
        solution = np.zeros((n,2))
    return np.rint(solution)

if __name__ == "__main__":
    main()
