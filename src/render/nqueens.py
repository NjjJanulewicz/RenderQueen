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


def random_restart(nqueens):

    board = init_board(nqueens)

    for column, row in enumerate(board):  # For each column, place the queen in a random row
        board[column] = random.randint(0, len(board) - 1)

        return board


def expand(board, nqueens):
    """
    Note: changed_board = board, makes changed_board point to board, where, board.copy ensures that changed_board
    is pointing to a copy, not effecting the current board
    Generates all neighbors of the current state and returns the best option.
    :param board:
    :param nqueens:
    :return: The highest valued successor of the current state
    """

    move_list = []
    neighbors = []

    for column, row in enumerate(board):  # Generates moves
        if row + 1 <= nqueens:  # Move up
            move_up = (column, row + 1)
            move_list.append(move_up)
        elif row - 1 >= 0:  # Move down
            move_down = (column, row - 1)
            move_list.append(move_down)

    for move in move_list:  # Generates neighbors
        changed_board = board.copy()
        changed_board[move[0]] = move[1]
        neighbors.append(changed_board)

    for state in neighbors:  # Picks the best neighbor
        if evaluate_state(state) > evaluate_state(board):
            board = state

    return board


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
    should succeed 14% of the time w?out sideways moves. 84% with
    """

    # Variables #
    iteration = 0
    optimum = (len(board) - 1) * len(board) / 2

    # Algorithm #
    while evaluate_state(board) != optimum:
        iteration += 1
        print('iteration ' + str(iteration) + ': evaluation = ' + str(evaluate_state(board))
              + ' conflicts ' + str(count_conflicts(board)))

        if iteration == LIMIT:  # Give up after 1000 tries.
            break

        neighbor = expand(board, nqueens)

        if evaluate_state(neighbor) > evaluate_state(board):
            board = neighbor

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)


def schedule(k=20, lam=0.005, limit=100):
    """One possible schedule function for simulated annealing"""
    return lambda t: (k * math.exp(-lam * t) if t < limit else 0)


def probability(delta, t):
    e = math.e
    dec_prob = (e * delta) / t    # decimal probability represented as a decimal > 1, 1 = 100%
    percent = dec_prob * 100
    prob = random.randint(0, 100)

    if prob <= percent:
        return True
    else:
        return False


def simulated_annealing(board, nqueens):
    """
    TODO: gets stuck on shoulders, figure out sideways moves.
    Iteration of hill climbing that aims to "structure" random walking.
    The innermost loop of the simulated-annealing algorithm is quite similar to hill climbing.
    Instead of picking the best move, however, it picks a random move. If the move improves the situation,
    it is always accepted. Otherwise, the algorithm accepts the move with some probability less than 1 (Artificial Intelligence p. 125).
    :param nqueens: The number of queens in the problem, also affects board size.
    :param board: list/array representation of columns and the row of the queen on that column
    :return: A solution if found or, the final state in a human readable format.
    """

    # Variables
    annealing = schedule()
    optimum = (len(board) - 1) * len(board) / 2
    iterator = 0

    # Logic
    while evaluate_state(board) != optimum:
        iterator += 1
        print('iteration ' + str(iterator) + ': evaluation = ' + str(evaluate_state(board))
              + ' conflicts ' + str(count_conflicts(board)))

        if iterator == LIMIT:  # Give up after 1000 tries.
            break

        for x in range(sys.maxsize):
            t = annealing(x)
            if t == 0:
                break

            new_board = random_restart(nqueens)

            delta = evaluate_state(new_board) - evaluate_state(board)

            if delta > 0 or probability(delta, t):
                board = new_board.copy()

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')
    print('Final state is:')
    print_board(board)




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