import sys, pygame
import model
from math import log2
from ai import *
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np

ai = False
depth = 2

size = width, height = 480, 500
playRegion = 480, 480
FPS = 60

black = (0,0,0)
white = (255,255,255)
fontColor = (82, 52, 42)
defaultTileColor = (232,232,232)
tileBoarderColor = fontColor

boardSize = 4
def drawBoard(screen, board):
    screen.fill(black)
    for i in range(board.boardSize):
        for j in range(board.boardSize):
            color = defaultTileColor
            numberText = ''
            if board.board[i][j] != 0:
                gComponent = 235 - log2(board.board[i][j])*((235 - 52)/(board.boardSize**2))
                color = (235, gComponent,52)
                numberText = str(board.board[i][j])
            rect = pygame.Rect(j*playRegion[0]/board.boardSize,
                                i*playRegion[1]/board.boardSize,
                                playRegion[0]/board.boardSize,
                                playRegion[1]/board.boardSize)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, fontColor, rect, 1)

            fontImage = tileFont.render(numberText, 0, fontColor)
            if fontImage.get_width() > playRegion[0]/board.boardSize:
                fontImage = pygame.transform.scale(fontImage,
                            (playRegion[0]/board.boardSize,
                            fontImage.get_height()/fontImage.get_width()*playRegion[0]/board.boardSize))
            screen.blit(fontImage,
                    (j*playRegion[0]/board.boardSize + (playRegion[0]/board.boardSize - fontImage.get_width())/2,
                    i*playRegion[1]/board.boardSize + (playRegion[1]/board.boardSize - fontImage.get_height())/2))
    fontImage = scoreFont.render("Score: {:,}".format(board.score) + (" [AI enabled, depth={}]".format(depth) if ai else ""), 1, white)
    screen.blit(fontImage, (1, playRegion[1]+1))

def handleInput(event, board):
    global ai

    if event.type == pygame.QUIT:
            pool.close()
            pool.terminate()
            sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            board.move(model.RIGHT)
        elif event.key == pygame.K_LEFT:
            board.move(model.LEFT)
        elif event.key == pygame.K_UP:
            board.move(model.UP)
        elif event.key == pygame.K_DOWN:
            board.move(model.DOWN)
        if event.key == pygame.K_r:
            board = model.Board(boardSize)
        elif event.key == pygame.K_ESCAPE:
            pool.close()
            pool.terminate()
            sys.exit()
        elif event.key == pygame.K_SPACE:
                ai = not ai

    return board

def run_game_and_get_score_with_greedy():
    global ai
    global depth
    global pool

    board = model.Board(boardSize)
    
    while not board.checkLoss():
        nextBestMove = getNextBestMoveGreedy(board)
        board.move(nextBestMove)

    return board.score 

def run_game_and_get_score_with_TD(num_episodes=100, alpha=0.1, gamma=0.9):
    global ai


    state_values = np.zeros((boardSize, boardSize))

    for episode in range(num_episodes):
        board = model.Board(boardSize)
        
        state = np.array(board.board)
        state_indices = np.clip(state, 0, boardSize - 1)

        while not board.checkLoss():
            epsilon = 0.1
            if np.random.rand() < epsilon:
                action = np.random.choice(4)
            else:
                action = np.argmax(state_values[state_indices[0], state_indices[1]])

            next_best_move = model.directions[action]
            score, _ = board.move(next_best_move)

            next_state = np.array(board.board)

            next_state_indices = np.clip(next_state, 0, boardSize - 1)

            current_value = state_values[state_indices[0], state_indices[1]]
            next_value = np.max(state_values[next_state_indices[0], next_state_indices[1]])

            state_values[state_indices[0], state_indices[1]] += alpha * (
                score + gamma * next_value - current_value
            )

            state = next_state
            state_indices = next_state_indices

    return board.score

def run_games_and_store_scores(use_reinforced_learning = False, num_games=50):
    scores = []
    
    if(use_reinforced_learning):
        for _ in range(num_games):
            score = run_game_and_get_score_with_TD()
            scores.append(score)
    else:
        for _ in range(num_games):
            score = run_game_and_get_score_with_greedy()
            scores.append(score) 

    return scores

def gameLoop():
    clock = pygame.time.Clock()
    board = model.Board(boardSize)

    while 1:
        for event in pygame.event.get():
            board = handleInput(event, board)

        if ai and not board.checkLoss():
            nextBestMove = getNextBestMoveGreedy(board)
            board.move(nextBestMove)

        drawBoard(screen, board)
        pygame.display.flip()
        clock.tick(FPS)

def plot_scores(scores, output_filename="histogram.png", num_games = 50, algorithm = "greedy"):
    plt.hist(scores, bins=20, edgecolor='black')
    plt.title('Histograma de pontuação: {} ({} jogos)'.format(algorithm, num_games))
    plt.xlabel('Pontuação')
    plt.ylabel('Frequência')
    plt.savefig(output_filename)
    plt.show()

if __name__ == '__main__':
    global screen
    global tileFont
    global scoreFont
    global pool
    mp.freeze_support()
    mp.set_start_method('spawn')
    pool = mp.Pool(processes=4)

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("2048")
    tileFont = pygame.font.SysFont("", 72)
    scoreFont = pygame.font.SysFont("", 22)

    num_games = 50

    # gameLoop()

    # scores = run_games_and_store_scores(use_reinforced_learning=True, num_games=num_games)
    # plot_scores(scores, output_filename="time_diffence_histogram.png", algorithm="diferença temporal", num_games=num_games)
    scores = run_games_and_store_scores(num_games=num_games)
    plot_scores(scores, output_filename="greedy_histogram.png", num_games=num_games)
    
