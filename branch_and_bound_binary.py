from mip import Model, xsum, minimize, BINARY

class BranchAndBoundBinary:
    """
    This class implements the Branch and Bound algorithm for binary linear programming problems.
    """
    def __init__(self, c, A, b):
        """
        Initializes the BranchAndBoundBinary class.

        Parameters:
        c (list): A list of coefficients of the objective function.
        A (list): A list of coefficients of the constraints.
        b (list): A list of the right-hand side values of the constraints.
        """
        self.c = c
        self.A = A
        self.b = b
        self.n = len(c)
        self.m = len(b)
        self.lower_bounds = []
        self.upper_bounds = []
        self.nodes = []

    def solve(self):
        """
        Solves the binary linear programming problem using the Branch and Bound algorithm.

        Returns:
        list: A list of binary values that represents the optimal solution.
        """
        self.nodes.append((0, None))
        while self.nodes:
            node = self.nodes.pop()
            i, x = node
            if i == self.n:
                if self.is_feasible(x):
                    return x
                continue
            subproblems = self.branch(x, i)
            for j, subproblem in subproblems:
                lb = self.bound(subproblem)
                self.lower_bounds.append(lb)
                self.upper_bounds.append(None)
                self.nodes.append((j, subproblem))
            self.update_upper_bounds()

    def initialize(self):
        """
        Initializes the binary linear programming problem.
        """
        self.model = Model()
        self.x = [self.model.add_var(var_type=BINARY) for i in range(self.n)]
        self.model.objective = minimize(xsum(self.c[i] * self.x[i] for i in range(self.n)))
        for j in range(self.m):
            self.model += xsum(self.A[j][i] * self.x[i] for i in range(self.n)) <= self.b[j]

    def solve_subproblem(self, x):
        """
        Solves a subproblem of the binary linear programming problem.

        Parameters:
        x (list): A list of binary values that represents the solution of the subproblem.

        Returns:
        list: A list of binary values that represents the optimal solution of the subproblem.
        """
        for i in range(self.n):
            self.x[i].start = x[i]
        self.model.optimize()
        return [self.x[i].x for i in range(self.n)]

    def branch(self, x, i):
        """
        Branches the binary linear programming problem.

        Parameters:
        x (list): A list of binary values that represents the solution of the problem.
        i (int): The index of the variable to be branched.

        Returns:
        list: A list of subproblems.
        """
        subproblems = []
        subproblem0 = x.copy()
        subproblem0[i] = 0
        subproblems.append((i+1, subproblem0))
        subproblem1 = x.copy()
        subproblem1[i] = 1
        subproblems.append((i+1, subproblem1))
        return subproblems

    def bound(self, x):
        """
        Calculates the lower bound of the binary linear programming problem.

        Parameters:
        x (list): A list of binary values that represents the solution of the problem.

        Returns:
        float: The lower bound of the problem.
        """
        return sum(self.c[i] * x[i] for i in range(self.n))

    def update_upper_bounds(self):
        """
        Updates the upper bounds of the binary linear programming problem.
        """
        self.upper_bounds = []
        for i in range(len(self.lower_bounds)):
            if i == 0:
                self.upper_bounds.append(self.lower_bounds[i])
            else:
                self.upper_bounds.append(min(self.upper_bounds[i-1], self.lower_bounds[i]))

    def is_feasible(self, x):
        """
        Checks if a solution is feasible.

        Parameters:
        x (list): A list of binary values that represents the solution of the problem.

        Returns:
        bool: True if the solution is feasible, False otherwise.
        """
        return all(0 <= x[i] <= 1 for i in range(self.n))
