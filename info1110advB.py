class Board:
    def __init__(self, rows: int, columns: int): #initalising Board parameters for it's size as integers
        #defining instance variables
        self.rows = rows
        self.columns = columns
        self.grid = [[" " for _ in range(columns)] for _ in range(rows)] #grid instance variable of a list of rows, each containing a list of items in that row's columns

    def __repr__(self): #implementing repr method to create and return the board when a Board object is created
        #creating the column number headline with correct spacing between column numbers
        headline = "  "
        for i in range(1, self.columns):
            headline += f"{i}   "
        headline += f"{self.columns}"

        horizontal_border = "+" + "---+" * self.columns #defining string for the boarder above and below each row of board spaces

        #initalising list of board lines, starting with the headline
        board_lines = [headline] 
        #looping through each row of board spaces, to add to the list of board board_lines
        for row in self.grid: # number of rows
            h_row = "| " + " | ".join(row) + " |" # creates a line of boxes with correct item in each column for each row
            board_lines.append(horizontal_border) #adding boarder to list of board lines...
            board_lines.append(h_row) #before adding each row of board spaces
        board_lines.append(horizontal_border) #adding base boarder to list of lines

        return "\n".join(board_lines) + "\n" #returning each line of the grid with correct newlines


class Piece:
    def __init__(self, symbol: str): #initalising Piece symbol parameter as a string
        self.symbol = symbol #defining symbol as an instance variable

    #defining instance method to insert a piece to the board
    def insert(self, board: Board, column: int): #also taking on parameters of a Board object and column (integer) where the piece is placed
        for row in range(board.rows, 0, -1): #looping through the rows starting from the bottom
            if board.grid[row-1][column-1] == " ": 
                board.grid[row-1][column-1] = f"{self.symbol}"
                return True #finishing loop by returning true once the lowest empty slot found in the chosen column, and changed to the symbol
        return False #returning false if the column is all filled up with pieces (runs if the if statement block doesn't run)


#the rest of the comments for this class within other section
class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.current_pieces = []

    def add_piece(self, symbol: str, quantity: int):
        for i in range(quantity):
            self.current_pieces.append(Piece(symbol))

    def __str__(self):
        unique_symbols = set(piece.symbol for piece in self.current_pieces)
        hand_dict = {}
        for symbol in unique_symbols:
            amount = sum(1 for piece in self.current_pieces if piece.symbol == symbol)
            hand_dict[symbol] = amount
        parts = [f"{k}: {v}" for k, v in sorted(hand_dict.items())]
        return f"{self.name}'s pieces -> " + ", ".join(parts)
    
    def choose_piece(self):
        print(self) #runs and prints the return value of the __str__() special method
        user_input = input("Choose a piece to play (symbol and column): ").split()
        if len(user_input) != 2:
            return None

        piece_using = str(user_input[0])
        try:
            column_using = int(user_input[1])
        except ValueError:
            return None

        for index, piece in enumerate(self.current_pieces):
            if piece.symbol == piece_using:
                return [self.current_pieces.pop(index), column_using]

        return None

#defining class to run for the game being setup and played
class Game:
    def __init__(self, rows: int, columns: int):
        self.players = []
        self.current_player = None
        self.board = Board(rows, columns)

    #method to setup the players and their pieces
    def setup(self):
        #setting up first player
        while True:
            user_1 = input("Enter player one's name and symbol: ").split()
            if len(user_1) == 2:
                name_1, symbol_1 = user_1
                if len(symbol_1) == 1:
                    break

        #setting up second player
        while True:
            user_2 = input("Enter player two's name and symbol: ").split()
            if len(user_2) == 2:
                name_2, symbol_2 = user_2
                if symbol_1 == symbol_2:
                    continue
                if len(symbol_2) == 1:
                    break

        #adding the players as Player objects
        player_1 = Player(name_1, symbol_1)
        player_2 = Player(name_2, symbol_2)

        self.players.append(player_1)
        self.players.append(player_2)

        #determining how many regular pieces each player gets
        total_spaces = self.board.rows * self.board.columns
        player_1_pieces = total_spaces // 2
        if total_spaces % 2 == 1:
            player_1_pieces += 1
        player_2_pieces = total_spaces // 2

        #using the add_piece method to set up each players pieces and amounts
        player_1.add_piece(symbol_1, player_1_pieces)
        player_2.add_piece(symbol_2, player_2_pieces)

        self.current_player = self.players[0]

    def begin(self):
        #setting up game
        self.setup()

        # checking who is going to win
        def check_winner(symbol):
            grid = self.board.grid
            rows = self.board.rows
            cols = self.board.columns
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

            for r in range(0, rows):
                for c in range(0, cols):
                    if grid[r][c] == symbol:
                        for dr, dc in directions:
                            count = 0
                            for i in range(4):
                                nr, nc = r + dr*i, c + dc*i
                                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == symbol:
                                    count += 1
                                else:
                                    break
                            if count == 4:
                                return True
            return False

        while True:
            print(self.board)
            move = self.current_player.choose_piece()

            if move is None:
                continue

            piece, col = move
            if piece.insert(self.board, col):
                if check_winner(piece.symbol):
                    print(f"{self.current_player.name} wins!")
                    print(self.board)
                    return

                self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
            else:
                # Could not insert: return piece to player's hand
                self.current_player.current_pieces.append(piece)

            # Check for draw
            if all(len(player.current_pieces) == 0 for player in self.players):
                print(self.board)
                print("It was a draw!")
                return

def main():
    print("Welcome to Connect 4!")

    # Get board dimensions, re-prompting until valid input is given
    while True:
        try:
            rows = int(input("Enter number of rows: "))
            columns = int(input("Enter number of columns: "))
            if rows >= 4 and columns >= 4:
                break
            print("The board must be at least 4x4 to allow a winning line.")
        except ValueError:
            print("Please enter whole numbers.")

    game = Game(rows, columns)
    game.begin()


if __name__ == "__main__":
    main()