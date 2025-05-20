from tabnanny import check

import numpy as np
from tabulate import tabulate


class GomokuGame:
    def __init__(self, size=15, starting_player='B'):
        self.size = size
        self.board = np.full((size, size), ' ')
        self.current_player = starting_player  # 'B' or 'W'
        self.winner = None
        self.move_history = []  # to store moves

    def reset(self):
        self.board.fill(' ')
        self.current_player = 'B' if self.current_player == 'W' else 'W'
        self.winner = None
        self.move_history = []

    def make_move(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '):
            return False

        self.board[row][col] = self.current_player
        self.move_history.append((row, col, self.current_player))

        if self.check_winner(row, col):
            self.winner = self.current_player
        elif self.board_full():
            self.winner = 'Draw'

        self.current_player = 'W' if self.current_player == 'B' else 'B'
        return True

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        player = self.board[row][col]

        for drow, dcol in directions:  # to count consecutive moves for same player
            count = 1
            for i in range(1, 5):
                r, c = row + drow * i, col + dcol * i
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                r, c = row - drow * i, col - dcol * i
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False


    def get_valid_moves(self, window=2):
        valid_moves = set()

        if not self.move_history:
            # First move — suggest the center
            center = self.size // 2
            return [(center, center)]

        for r, c, _ in self.move_history: 
            for dr in range(-window, window + 1):
                for dc in range(-window, window + 1):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.size and 0 <= nc < self.size and
                            self.board[nr][nc] == ' '):
                        valid_moves.add((nr, nc))

        return list(valid_moves)

    def is_terminal(self):

        if self.winner is not None:  # B or W or Draw
            return True
        for row in self.board:  # there are empty spots so can't terminate
            if ' ' in row:
                return False

        return True  # if no winner but board is full

    def print_board(self):

        headers = [str(i) for i in range(self.size)]
        board_data = []
        for i in range(self.size):
            row_data = list(self.board[i])
            board_data.append([str(i)] + row_data)
        print("\nCurrent Board State:")
        print(tabulate(board_data, headers=[' '] + headers, tablefmt='grid'))
        print(f"\nCurrent player: {self.current_player}")
        if self.winner:
            print(f"Game over! Winner: {self.winner}")

    def board_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    # def player_win(self):

    def minimax(self, last_row=None, last_col=None, depth=4, player='B'):
        """
        Minimax Algorithm
        Black -> Maximizing player
        White -> Minimizing player
        """
        if last_row is not None and last_col is not None:
            if self.check_winner(last_row, last_col):
                return 1 if player == 'W' else -1  # The previous move was made by the opponent

        if depth == 0 or self.board_full():
            return 0

        next_player = 'W' if player == 'B' else 'B'

        if player == 'B':  # Maximizing
            best_score = -float('inf')
            for i, j in self.get_valid_moves():
                self.board[i][j] = player
                score = self.minimax(i, j, depth - 1, next_player)
                self.board[i][j] = ' '  # Undo move
                best_score = max(best_score, score)
            return best_score

        else:  # Minimizing
            best_score = float('inf')
            for i, j in self.get_valid_moves():
                self.board[i][j] = player
                score = self.minimax(i, j, depth - 1, next_player)
                self.board[i][j] = ' '  # Undo move
                best_score = min(best_score, score)
            return best_score

    def get_best_minimax(self, depth=6):
        """
        Returns the best move for the current player using minimax.
        """
        current = self.current_player
        best_score = -float('inf') if current == 'B' else float('inf')
        best_move = None

        for i, j in self.get_valid_moves():
            self.board[i][j] = current
            score = self.minimax(i, j, depth - 1, 'W' if current == 'B' else 'B')
            self.board[i][j] = ' '  # Undo move

            if current == 'B' and score > best_score:
                best_score = score
                best_move = (i, j)
            elif current == 'W' and score < best_score:
                best_score = score
                best_move = (i, j)

        return best_move

    def alpha_beta(self, alpha, beta,depth=5,last_row=None, last_col=None, player='B'):
        if last_row is not None and last_col is not None:
            if self.check_winner(last_row, last_col):
                return 1 if player == 'W' else -1  # The previous move was made by the opponent

        if depth == 0 or self.board_full():
            return 0

        next_player = 'W' if player == 'B' else 'B'

        if player == 'B':  # Maximizing
            best_score = -float('inf')
            for i, j in self.get_valid_moves():
                self.board[i][j] = player
                score = self.alpha_beta(alpha,beta,depth - 1,i,j,next_player)
                self.board[i][j] = ' '  # Undo move
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_score

        else:  # Minimizing
            best_score = float('inf')
            for i, j in self.get_valid_moves():
                self.board[i][j] = player
                score = self.alpha_beta(alpha,beta,depth - 1,i,j,next_player)
                self.board[i][j] = ' '  # Undo move
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score

    def get_best_alpha_beta(self, depth):
        current = self.current_player
        best_score = -float('inf') if current == 'B' else float('inf')
        best_move = None

        for i, j in self.get_valid_moves():
            self.board[i][j] = current
            alpha = -float('inf')
            beta = float('inf')
            score = self.alpha_beta(alpha,beta, depth - 1,i,j,'W' if current == 'B' else 'B')
            self.board[i][j] = ' '  # Undo move

            if current == 'B' and score > best_score:
                best_score = score
                best_move = (i, j)
            elif current == 'W' and score < best_score:
                best_score = score
                best_move = (i, j)

        return best_move



if __name__ == "__main__":

    game = GomokuGame(size=15, starting_player='W')
    # Play a simple game
    moves = [(0, 0), (1, 1), (0, 1), (2, 2), (0, 2), (3, 3), (0, 3), (4, 4), (0, 4)]

    print("Starting a new Gomoku game!")
    game.print_board()

    while True:
        print(f"--------Player {game.current_player} Turn---------")
        if game.current_player == 'B':
            i, j = game.get_best_minimax(depth=4)
        else:
           i,j= input().split()
           i  =  int(i)
           j = int(j)


        if not game.make_move(i, j):
            print("Invalid move! Try again.")
            continue

        game.print_board()

        if game.winner:
            if game.winner == 'Draw':
                print("It's a tie!")
            else:
                print(f"Player {game.winner} wins!")
            break

    if not game.winner:
        print("\nThe game ended in a draw!")
