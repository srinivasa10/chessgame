import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 480, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Set up the chessboard
board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

# Load chess piece images
pieces = {}
for piece in ["wp", "bp", "wr", "br", "wn", "bn", "wb", "bb", "wq", "bq", "wk", "bk"]:
    img = pygame.image.load(f"pieces/{piece}.png")
    img = pygame.transform.scale(img, (60, 60))
    pieces[piece] = img

# Function to render the chessboard
def render_board():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = (240, 217, 181)
            else:
                color = (181, 136, 99)
            pygame.draw.rect(screen, color, (col * 60, row * 60, 60, 60))
            piece = board[row][col]
            if piece:
                screen.blit(pieces[piece], (col * 60, row * 60))

def is_move_legal(start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    # Check if the target square is occupied by a friendly piece
    if target and piece[0] == target[0]:
        return False

    # Check the specific rules for each piece
    if piece[1] == "p":  # Pawn
        if start_col == end_col:  # Move forward
            if piece[0] == "w":
                if start_row == 6 and end_row == 4 and not target:
                    return True
                if start_row - end_row == 1 and not target:
                    return True
            else:  # Black pawn
                if start_row == 1 and end_row == 3 and not target:
                    return True
                if end_row - start_row == 1 and not target:
                    return True
        else:  # Capture diagonally
            if piece[0] == "w" and start_row - end_row == 1 and abs(start_col - end_col) == 1 and target and target[0] == "b":
                return True
            elif piece[0] == "b" and end_row - start_row == 1 and abs(start_col - end_col) == 1 and target and target[0] == "w":
                return True

    if piece[1] == "r":  # Rook
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Move horizontally
                step = 1 if start_col < end_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col]:
                        return False
            else:  # Move vertically
                step = 1 if start_row < end_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col]:
                        return False
            return True

    if piece[1] == "n":  # Knight
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True

    if piece[1] == "b":  # Bishop
        if abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if start_row < end_row else -1
            step_col = 1 if start_col < end_col else -1
            row, col = start_row + step_row, start_col + step_col
            while row != end_row:
                if board[row][col]:
                    return False
                row += step_row
                col += step_col
            return True

    if piece[1] == "q":  # Queen
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Move horizontally
                step = 1 if start_col < end_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col]:
                        return False
            else:  # Move vertically
                step = 1 if start_row < end_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col]:
                        return False
            return True
        elif abs(start_row - end_row) == abs(start_col - end_col):  # Move diagonally
            step_row = 1 if start_row < end_row else -1
            step_col = 1 if start_col < end_col else -1
            row, col = start_row + step_row, start_col + step_col
            while row != end_row:
                if board[row][col]:
                    return False
                row += step_row
                col += step_col
            return True

    if piece[1] == "k":  # King
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True

    return False


# Main game loop
running = True
selected_piece = None
player = 1  # Current player (1 for Player 1, 2 for Player 2)
hints = []  # List to store hint positions

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                col = event.pos[0] // 60
                row = event.pos[1] // 60
                if selected_piece is None:
                    piece = board[row][col]
                    if piece and ((player == 1 and piece[0] == "w") or (player == 2 and piece[0] == "b")):
                        selected_piece = (row, col)
                        hints = []
                        for i in range(8):
                            for j in range(8):
                                if is_move_legal(selected_piece, (i, j)):
                                    hints.append((i, j))
                else:
                    if (row, col) in hints:
                        if is_move_legal(selected_piece, (row, col)):
                            board[row][col] = board[selected_piece[0]][selected_piece[1]]
                            board[selected_piece[0]][selected_piece[1]] = None
                            player = 2 if player == 1 else 1  # Switch turn to the other player
                        selected_piece = None
                        hints = []
                    else:
                        selected_piece = None
                        hints = []

    screen.fill((255, 255, 255))
    render_board()
    if selected_piece is not None:
        pygame.draw.rect(screen, (0, 255, 0), (selected_piece[1] * 60, selected_piece[0] * 60, 60, 60), 3)
    for hint in hints:
        pygame.draw.rect(screen, (0, 0, 255), (hint[1] * 60, hint[0] * 60, 60, 60), 1, 1)  # Draw a dotted rectangle
    pygame.display.update()

    # Check if the current player cannot move
    can_move = False
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece[0] == "w" and player == 1:
                for i in range(8):
                    for j in range(8):
                        if is_move_legal((row, col), (i, j)):
                            can_move = True
                            break
                    if can_move:
                        break
            elif piece and piece[0] == "b" and player == 2:
                for i in range(8):
                    for j in range(8):
                        if is_move_legal((row, col), (i, j)):
                            can_move = True
                            break
                    if can_move:
                        break
            if can_move:
                break
        if can_move:
            break

    if not can_move:
        print(f"Player {player} cannot move. Game Over!")
        running = False

# Quit Pygame
pygame.quit()
