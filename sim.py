import sys
import cvxpy as cp
import numpy as np

def main(args):
    n = 4 # Number of students
    caps = [2, 2]
    utilities = np.random.random_integers(0, 100, (n, 2))
    budgets = np.random.uniform(9, 11, n)
    prices = [11, 11]
    # Use integer program to get the clearing prices

    # for x in prices:

def allocate(utilities, caps, budgets, prices):
	# Creates course allocation variable matrix with Boolean entries
	alloc = cp.Variable((n,2), boolean=True)
	
	enrollment = np.sum(alloc, axis=0)
	
	# Capacity constraint
	capacity_constraint = enrollment <= caps
	
	payments = np.matmul(alloc, prices)
	
	# Budget constraint
	budget_constraint = payments <= budgets
			
	
	total_util = utilities * alloc
	
	problem = cp.Problem(cp.Maximize(total_util), [capacity_constraint, budget_constraint])
	
	solution = problem.solve()
	
	return np.sum(solution, axis=0)

if __name__ == "__main__":
    main(sys.argv)
