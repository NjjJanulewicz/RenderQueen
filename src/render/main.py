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
        print('Usage: python nqueens.py NUMBER')
        return False

    limit_choice = input('Please set an iteration limit ')

    print('\nWhich algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing, 4: genetic algorithm \n')

    try:
        global LIMIT
        LIMIT = int(limitChoice)
        if LIMIT not in range(1, 1000000):
            raise ValueError

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
        #annealing_schedule = input('Please set an annealing schedule ')
        simulated_annealing(board)
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
