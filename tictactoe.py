import sys
import random
import copy


class TicTacToe:
    def __init__(self):
        self.board = None
        self.x = None
        self.o = None
        self.next_symbol = None
        self.next_player = None
        self.turn = None
        self.players = []

    def init_board_state(self):
        board_lst = [i for i in (" " * 9)]
        self.board = [board_lst[i:i + 3] for i in range(0, len(board_lst), 3)]
        self.next_symbol = "X"
        self.next_player = 0
        self.init_game_state()

    def init_game_state(self):
        while True:
            print("Type 'exit' to quit, or 'start' with two of the following: "
                  "'easy', 'medium', 'hard', or 'user'")
            state = [i.lower() for i in input("Input command: ").split()]
            action = state[0]
            if action == "exit":
                sys.exit()
            elif action == "start":
                try:
                    args = [state[1], state[2]]
                except Exception:
                    print("Bad parameters!")
                    continue
                self.players = []
                for i in args:
                    self.players.append(i)
                self.turn = self.players[self.next_player]
                break
            else:
                print("Bad parameters")

    def display_board(self):
        print("---------")
        for i in self.board:
            print("|", end=" ")
            for j in i:
                print(" ".join(j), end=" ")
            print("|")
        print("---------")

    def user_move(self):
        while True:
            try:
                y, x = input("Enter the coordinates as row and column: ").split()
                y, x = int(y) - 1, int(x) - 1
            except Exception:
                print("You should enter numbers!")
                continue
            if not 0 <= y < 3 or not 0 <= x < 3:
                print("Coordinates should be from 1 to 3!")
            elif self.board[y][x] != " ":
                print("This cell is occupied! Choose another one!")
            else:
                self.board[y][x] = self.next_symbol
                break

    def get_empties(self, board):
        empty_indexes = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    empty_indexes.append([i, j])
        return empty_indexes

    def check_win_condition(self, board, symbol):
        draw_check = []
        for i in range(3):
            column, diagonal = [], []
            for j in range(3):
                draw_check.append(board[i][j])
                column.append(board[j][i])
                diagonal.append(board[j][j])
            if column.count(symbol) == 3 or board[i].count(symbol) == 3 or \
                    diagonal.count(symbol) == 3 or \
                    [board[0][2], board[1][1], board[2][0]].count(symbol) == 3:
                return "wins"
        if " " not in draw_check:
            return "Draw"
        return False

    def ai_move(self):
        empty_spots = self.get_empties(self.board)
        while True:
            y, x = random.randint(0, 2), random.randint(0, 2)
            if self.turn == "easy":
                if [y, x] in empty_spots:
                    self.board[y][x] = self.next_symbol
                    print('Making move level "easy"')
                    return

            elif self.turn == "medium":
                # Look one turn ahead using a recursion depth limit of 1
                # and place symbol to win or prevent opponent from winning
                best_score = -1000
                move = None
                if len(empty_spots) < 8:
                    for i in empty_spots:
                        board_copy = copy.deepcopy(self.board)
                        board_copy[i[0]][i[1]] = self.next_symbol
                        score = self.minimax(board_copy, 0, False, 1)
                        if score > best_score:
                            best_score = score
                            move = [i[0], i[1]]
                if move:
                    self.board[move[0]][move[1]] = self.next_symbol
                    print('Making move level "medium"')
                    return

                # If no winning conditions exist one turn ahead, pick a random spot
                if [y, x] in empty_spots:
                    self.board[y][x] = self.next_symbol
                    print('Making move level "medium"')
                    return

            elif self.turn == "hard":
                best_score = -10000
                for i in empty_spots:
                    board_copy = copy.deepcopy(self.board)
                    board_copy[i[0]][i[1]] = self.next_symbol
                    score = self.minimax(board_copy, 0, False, 0)
                    if score > best_score:
                        best_score = score
                        move = [i[0], i[1]]
                self.board[move[0]][move[1]] = self.next_symbol
                print('Making move level "hard"')
                return

    def symbol_switch(self, symbol):
        if symbol == "X":
            return "O"
        else:
            return "X"

    def minimax(self, board, depth, is_maximizing, limit):
        hard_ai = self.next_symbol
        if hard_ai == "O":
            player = "X"
        else:
            player = "O"

        # Terminal state
        ai_result = self.check_win_condition(board, hard_ai)
        player_result = self.check_win_condition(board, player)
        if ai_result == "wins":
            return 10
        elif player_result == "wins":
            return -10
        elif ai_result == "Draw" or player_result == "Draw":
            return 0

        # Recursive state
        else:
            # return a draw if recursion depth limit is reached and terminal state is not
            empty_spots = self.get_empties(board)
            if limit and limit == depth:
                return 0
            if is_maximizing:
                best_score = -10000
                for i in empty_spots:
                    board[i[0]][i[1]] = hard_ai
                    score = self.minimax(board, depth + 1, False, limit)
                    board[i[0]][i[1]] = " "
                    best_score = max(best_score, score)
                return best_score
            else:
                best_score = 10000
                for i in empty_spots:
                    board[i[0]][i[1]] = player
                    score = self.minimax(board, depth + 1, True, limit)
                    board[i[0]][i[1]] = " "
                    best_score = min(best_score, score)
                return best_score

    def take_turn(self):
        if self.turn == "user":
            self.user_move()
        else:
            self.ai_move()

    def switch_turn(self):
        self.next_symbol = self.symbol_switch(self.next_symbol)
        if self.next_player == 0:
            self.next_player = 1
        else:
            self.next_player = 0
        self.turn = self.players[self.next_player]

    def game_loop(self):
        game_over = False
        while not game_over:
            self.take_turn()
            self.display_board()
            game_over = self.check_win_condition(self.board, self.next_symbol)
            if game_over == "Draw":
                print(game_over)
            elif game_over == "wins":
                print(f"{self.next_symbol} wins")
            self.switch_turn()

    def menu_loop(self):
        while True:
            self.init_board_state()
            self.display_board()
            self.game_loop()


if __name__ == '__main__':
    g1 = TicTacToe()
    g1.menu_loop()
