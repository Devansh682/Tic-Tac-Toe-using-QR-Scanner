import cv2
import numpy as np
from pyzbar.pyzbar import decode

# initialize the tic-tac-toe board
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

# initialize the QR code symbols
symbol_x = 'X'
symbol_o = 'O'

# function to check if the board is full
def is_board_full(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                return False
    return True

# function to check if a player has won
def check_win(board, symbol):
    # check rows
    for row in range(3):
        if board[row][0] == symbol and board[row][1] == symbol and board[row][2] == symbol:
            return True
    # check columns
    for col in range(3):
        if board[0][col] == symbol and board[1][col] == symbol and board[2][col] == symbol:
            return True
    # check diagonals
    if board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
        return True
    if board[0][2] == symbol and board[1][1] == symbol and board[2][0] == symbol:
        return True
    # no win
    return False

# function to get the best move
def get_best_move(board, symbol):
    best_score = -np.inf
    best_row = -1
    best_col = -1
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = symbol
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_row = row
                    best_col = col
    return best_row, best_col

# function to evaluate the score of the board
def evaluate(board):
    if check_win(board, symbol_x):
        return 1
    elif check_win(board, symbol_o):
        return -1
    else:
        return 0

# function to implement minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, symbol_x):
        return 1
    elif check_win(board, symbol_o):
        return -1
    elif is_board_full(board):
        return 0
    if is_maximizing:
        best_score = -np.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = symbol_x
                    score = minimax(board, depth+1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = symbol_o
                    score = minimax(board, depth+1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score


# initialize the webcam
cap = cv2.VideoCapture(0)

# set the window size
cap.set(3, 640)
cap.set(4, 480)

# set the font for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# initialize the board
board = [[' ' for _ in range(3)] for _ in range(3)]

# initialize the symbols
symbol_x = 'X'
symbol_o = 'O'

# initialize the font for displaying text on the frame
font = cv2.FONT_HERSHEY_SIMPLEX

# initialize the variable to keep track of the last scanned symbol
last_symbol = None

while True:
    # read the frame from the webcam
    ret, frame = cap.read()

    # decode the QR code symbols in the frame
    symbols = decode(frame)

    # draw the tic-tac-toe board on the frame
    for row in range(3):
        for col in range(3):
            cv2.rectangle(frame, (col*120+20, row*120+20), ((col+1)*120-20, (row+1)*120-20), (255, 255, 255), 5)
            cv2.putText(frame, board[row][col], (col*120+50, row*120+85), font, 3, (255, 255, 255), 5)

    # check if the game is over
    if check_win(board, symbol_x):
        cv2.putText(frame, 'X wins!', (50, 450), font, 2, (0, 0, 255), 3)
        break
    elif check_win(board, symbol_o):
        cv2.putText(frame, 'O wins!', (50, 450), font, 2, (0, 0, 255), 3)
        break
    elif is_board_full(board):
        cv2.putText(frame, 'Tie!', (50, 450), font, 2, (0, 0, 255), 3)
        break

    # check if a symbol has been scanned
    if symbols:
        # get the symbol value
        symbol_value = symbols[0].data.decode('utf-8')

        # check if the symbol is different from the last scanned symbol
        if symbol_value != last_symbol:
            # get the best move for the symbol
            if symbol_value == symbol_x:
                row, col = get_best_move(board, symbol_x)
                board[row][col] = symbol_x
            elif symbol_value == symbol_o:
                row, col = get_best_move(board, symbol_o)
                board[row][col] = symbol_o

            # update the last scanned symbol
            last_symbol = symbol_value

    # display the frame
    cv2.imshow('Tic Tac Toe', frame)

    # check for key press
    key = cv2.waitKey(1)
    if key == 27:   # ESC key to exit
        break

# release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
