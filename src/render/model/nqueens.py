import sys
import random
import math

MAXQ = 100
LIMIT = 1000


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens.py-1)*nqueens.py/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens.py-1)*nqueens.py/2 - countConflicts().

    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Do not change the code above! ------------------
"""


def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens.py problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board)-1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)


def hill_climbing(board, nqueens):
    """
    From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better.
    :param nqueens: The number of queens in the problem, also affects board size.
    :param board: list/array representation of columns and the row of the queen on that column, 2d array.
    :return: A solution if found or, the final state in a human readable format.
    """

    """
    def hill_climbing(problem):
    From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]
    current = Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) <= problem.value(current.state):
            break
        current = neighbor
    return current.state
    """

    # Variables #
    iteration = 0
    optimum = (len(board) - 1) * len(board) / 2
    move_list = []
    neighbors = []
    explored = []

    # Algorithm #
    while evaluate_state(board) != optimum:

        # Limit check #
        print('iteration = ' + str(iteration) + ': evaluation = ' + str(evaluate_state(board))
              + ' conflicts = ' + str(count_conflicts(board)))
        if iteration == LIMIT:  # Give up after limit
            print('limit reached')
            break

        iteration += 1
        move = False
        explored.append(board)
        new_board = board.copy()

        if board in explored:    # If we get stuck in a loop random restart
            for column, row in enumerate(board):  # For each column, place the queen in a random row
                board[column] = random.randint(0, len(board) - 1)

        for column, row in enumerate(board):
            if in_conflict_with_another_queen(row, column, board):

                if not in_conflict_with_another_queen(row + 1, column, board):  # Move up
                    if row + 1 <= nqueens:
                        move_up = (column, row + 1)
                        move_list.append(move_up)
                        move = True

                elif not in_conflict_with_another_queen(row - 1, column, board):  # Move down
                    if row - 1 >= 0:
                        move_down = (column, row - 1)
                        move_list.append(move_down)
                        move = True

        if not move:
            for column, row in enumerate(board):  # For each column, place the queen in a random row
                new_board[column] = random.randint(0, len(board) - 1)
                neighbors.append(new_board)
        else:
            for move in move_list:
                changed_board = board.copy()
                changed_board[move[0]] = move[move[1]]
                neighbors.append(changed_board)

        for state in neighbors:
            if state not in explored:
                if evaluate_state(state) > evaluate_state(board):
                    board = state

        move_list.clear()
        neighbors.clear()

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')
    print('Final state is:')
    print_board(board)


def schedule(k = 20, lam = 0.005, limit = 100):
    """
    One possible schedule function for simulated annealing uses pythons functional paradigm
    """
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)


def simulated_annealing(board, nqueens):
    """
    Iteration of hill climbing that aims to "structure" random walking.
    The innermost loop of the simulated-annealing algorithm is quite similar to hill climbing.
    Instead of picking the best move, however, it picks a random move. If the move improves the situation,
    it is always accepted. Otherwise, the algorithm accepts the move with some probability less than 1 (Artificial Intelligence p. 125).
    :param nqueens: The number of queens in the problem, also affects board size.
    :param board: list/array representation of columns and the row of the queen on that column
    :return: A solution if found or, the final state in a human readable format.
    """

    """
    Python implamentation from the text's github
    def simulated_annealing(problem, schedule=exp_schedule()):
    current = Node(problem.initial)
    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return current.state
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(math.exp(delta_e / T)):
            current = next_choice
    pseudocode from the text (Artificial Intelligence p.126)
        function SIMULATED-ANNEALING(problem, schedule) returns a solution state
            inputs: problem, a problem
                    schedule, a mapping from time to “temperature”
            current ← MAKE-NODE(problem.INITIAL-STATE)
            for t = 1 to ∞ do
                T ← schedule(t)
                if T = 0 then return current
                next ← a randomly selected successor of current
                ΔE ← next.VALUE – current.VALUE
                if ΔE > 0 then current ← next
                else current ← next only with probability eΔE/T
    available functions
    in_conflict_with_another_queen(row, column, board)
    in_conflict(column, row, other_column, other_row)
    count_conflicts(board)
    evaluate_state(board)
    print_state(board)
    """

    # Variables
    annealing = schedule()
    optimum = (len(board) - 1) * len(board) / 2
    i = 0
    explored = []
    neighbors = []
    successor_list = []

    # Logic
    while evaluate_state(board) != optimum:
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board))
              + ' conflicts ' + str(count_conflicts(board))) # + ' Schedule ' + str(t))
        if i == LIMIT:  # Give up after 1000 tries.
            break

        move = False
        i += 1
        explored.append(board)
        new_board = board.copy()

        # for x in range(sys.maxsize):

        if board in explored:  # if we get stuck in a loop step left in a place or 2
            for column, row in enumerate(board):
                if column / random.randint(1, 2) == 0:
                    board[column] = board[column] - 1

        for x in range(0, LIMIT):
            t = annealing(x)
            if t == 0:
                if evaluate_state(board) == optimum:
                    print('Solved puzzle!')
                    print_board(board)
                    return
                else:
                    break

            for column, row in enumerate(board):
                if in_conflict_with_another_queen(row, column, board):
                    if not in_conflict_with_another_queen(row + 1, column, board):  # move up
                        if row + 1 < nqueens:
                            successor = (column, row + 1)
                            successor_list.append(successor)
                            move = True

                    elif not in_conflict_with_another_queen(row - 1, column, board):  # move down
                        if row - 1 >= 0:
                            successor = (column, row - 1)
                            successor_list.append(successor)
                            move = True

            if not move:
                for column, row in enumerate(board):  # For each column, place the queen in a random row
                    new_board[column] = random.randint(0, len(board) - 1)
            else:
                for move in successor_list:
                    changed_board = board.copy()
                    changed_board[move[0]] = move[1]
                    neighbors.append(changed_board)

            for state in neighbors:
                if state not in explored:
                    if evaluate_state(state) > evaluate_state(board):
                        new_board = state

            delta = evaluate_state(new_board) - evaluate_state(board)

            if delta > 0:
                board = new_board.copy()
            elif probability(delta, t):
                board = new_board.copy()

            successor_list.clear()
            neighbors.clear()

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')
    print('Final state is:')
    print_board(board)


def probability(delta, t):
    e = math.e
    dec_prob = (e * delta) / t    # decimal probability represented as a decimal > 1, 1 = 100%
    percent = dec_prob * 100
    prob = random.randint(0, 100)

    if prob <= percent:
        return True
    else:
        return False


def reproduce(x, y):
    # a[-2:]   last two items in the array
    # a[:-2]   everything except the last two items
    n = len(x)
    c = random.randint(1, n-1)
    x = x[:-c]
    y = y[-c:]
    x = x+y
    return x


def check_pop(population):
    optimum = ((len(population[0]) - 1) * len(population[0])) / 2
    for board in population:
        if evaluate_state(board) == optimum:
            return board
    return None


def mutate(individual):
    n = random.randint(0, len(individual)-1)
    r = random.randint(0, len(individual)-1)
    individual[n] = r
    return individual


def max_new_pop(population):
    max = -1
    for item in population:
        x = evaluate_state(item)
        if x>max:
            max = x
    return max


# takes 50000+ iterations to find a solution for N=8, be careful
def genetic_algorithm(population):
    iteration = 0
    while True:
        iteration += 1
        new_population = []
        for i in range(0, len(population)):
            j = random.randint(0, 3)
            x = population[j]
            k = random.randint(0, 3)
            y = population[k]
            child = reproduce(x, y)
            mutate(child)
            new_population.append(child)
        population = new_population
        if iteration == 100000:
            break
        max_evaluate = max_new_pop(population)
        print('iteration ' + str(iteration) + ': evaluation = ' + str(max_evaluate))
        a = check_pop(population)
        if a is not None:
            print('Solved puzzle!')
            break
    print('Final state is:')
    if a is not None:
        print_board(a)
    else:
        print_board(population[0])


def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) is not 2:
            raise ValueError

        nqueens = int(sys.argv[1])
        if nqueens < 1 or nqueens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python nqueens.py.py NUMBER')
        return False

    print('Which algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing, 4: genetic algorithm \n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 5):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False

    board = init_board(nqueens)
    print('Initial board: \n')
    print_board(board)

    if algorithm is 1:
        random_search(board)
    if algorithm is 2:
        hill_climbing(board, nqueens)
    if algorithm is 3:
        simulated_annealing(board, nqueens)
    if algorithm is 4:
        board1 = init_board(nqueens)
        board2 = init_board(nqueens)
        board3 = init_board(nqueens)
        board4 = init_board(nqueens)
        population = []
        population.insert(0, board1)
        population.insert(1, board2)
        population.insert(2, board3)
        population.insert(3, board4)
        genetic_algorithm(population)


# This line is the starting point of the program.
if __name__ == "__main__":
    main()