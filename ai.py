import model
import copy
import multiprocessing as mp

INF = 2**64

PERFECT_SNAKE = [[2,   2**2, 2**3, 2**4],
                [2**8, 2**7, 2**6, 2**5],
                [2**9, 2**10,2**11,2**12],
                [2**16,2**15,2**14,2**13]]

def snakeHeuristic(board):
    h = 0
    for i in range(board.boardSize):
        for j in range(board.boardSize):
            h += board[i][j] * PERFECT_SNAKE[i][j]

    return h

def simple_heuristic(board):
    return sum(sum(row) for row in board)

def getNextBestMoveGreedy(board):
    bestScore = -INF
    bestNextMove = model.directions[0]

    for dir in model.directions:
        simBoard = copy.deepcopy(board)
        score, validMove = simBoard.move(dir, False)
        
        if validMove:
            heuristic_score = snakeHeuristic(simBoard)
            
            if heuristic_score > bestScore:
                bestScore = heuristic_score
                bestNextMove = dir

    return bestNextMove




