def is_empty(board):


    # Returns True if the board is empty (no stones placed), False otherwise.
    for row in board:
        if any(cell != " " for cell in row):
            return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):

    n = len(board)
    y_start = y_end - (length - 1) * d_y
    x_start = x_end - (length - 1) * d_x
    
    # Checks positions before and after the sequence
    y_before = y_start - d_y
    x_before = x_start - d_x
    y_after = y_end + d_y
    x_after = x_end + d_x
    
    # Checks if positions are within board bounds
    before_valid = 0 <= y_before < n and 0 <= x_before < n
    after_valid = 0 <= y_after < n and 0 <= x_after < n
    
    # Checks if positions are empty
    before_empty = before_valid and board[y_before][x_before] == " "
    after_empty = after_valid and board[y_after][x_after] == " "
    
    if not before_valid and not after_valid:
        return "CLOSED"
    if before_empty and after_empty:
        return "OPEN"
    if before_empty or after_empty:
        return "SEMIOPEN"
    return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    
    open_seq_count = 0
    semi_open_seq_count = 0
    n = len(board)
    
    y = y_start
    x = x_start
    
    while 0 <= y < n and 0 <= x < n:
        # Checks if sequence can fit
        end_y = y + (length-1)*d_y
        end_x = x + (length-1)*d_x
        if not (0 <= end_y < n and 0 <= end_x < n):
            break
            
        # Checks for sequence
        sequence = True
        # Checks if this is part of a longer sequence
        longer_seq = False
        
        # Checks if previous position has same colour
        prev_y = y - d_y
        prev_x = x - d_x
        if 0 <= prev_y < n and 0 <= prev_x < n and board[prev_y][prev_x] == col:
            longer_seq = True
            
        # Checks if next position after sequence has same colour
        next_y = end_y + d_y
        next_x = end_x + d_x
        if 0 <= next_y < n and 0 <= next_x < n and board[next_y][next_x] == col:
            longer_seq = True
            
        if not longer_seq:
            # Checks the sequence itself
            for i in range(length):
                curr_y = y + i*d_y
                curr_x = x + i*d_x
                if board[curr_y][curr_x] != col:
                    sequence = False
                    break
            
            if sequence:
                bound_type = is_bounded(board, end_y, end_x, length, d_y, d_x)
                if bound_type == "OPEN":
                    open_seq_count += 1
                elif bound_type == "SEMIOPEN":
                    semi_open_seq_count += 1
        
        # Moves to next position
        if d_x == 0:  # vertical
            y += 1
        elif d_y == 0:  # horizontal
            x += 1
        else:  # diagonal
            y += 1
            x += d_x
    
    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):

    open_seq_count, semi_open_seq_count = 0, 0
    n = len(board)

    # Horizontal
    for i in range(n):
        o, s = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += o
        semi_open_seq_count += s

    # Vertical
    for j in range(n):
        o, s = detect_row(board, col, 0, j, length, 1, 0)
        open_seq_count += o
        semi_open_seq_count += s

    # Diagonal (top-left to bottom-right)
    # Starts from leftmost column
    for i in range(n):
        o, s = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += o
        semi_open_seq_count += s
    # Starts from top row (except leftmost cell)
    for j in range(1, n):
        o, s = detect_row(board, col, 0, j, length, 1, 1)
        open_seq_count += o
        semi_open_seq_count += s

    # Diagonal (top-right to bottom-left)
    # Starts from rightmost column
    for i in range(n):
        o, s = detect_row(board, col, i, n-1, length, 1, -1)
        open_seq_count += o
        semi_open_seq_count += s
    # Starts from top row (except rightmost)
    for j in range(n-2, -1, -1):
        o, s = detect_row(board, col, 0, j, length, 1, -1)
        open_seq_count += o
        semi_open_seq_count += s

    return open_seq_count, semi_open_seq_count

def search_max(board):
    n = len(board)
    
    # If board is empty, return center position
    if is_empty(board):
        return (n // 2, n // 2)
    
    # First checks if we can win with this move
    for y in range(n):
        for x in range(n):
            if board[y][x] == " ":
                # Checks if this move would win
                board[y][x] = "b"
                
                # Checks horizontal (right)
                if x <= n-5:
                    if all(board[y][x+i] == "b" for i in range(5)):
                        board[y][x] = " "
                        return (y, x)
                
                # Checks vertical (down)
                if y <= n-5:
                    if all(board[y+i][x] == "b" for i in range(5)):
                        board[y][x] = " "
                        return (y, x)
                
                # Checks diagonal (down-right)
                if x <= n-5 and y <= n-5:
                    if all(board[y+i][x+i] == "b" for i in range(5)):
                        board[y][x] = " "
                        return (y, x)
                
                # Checks diagonal (up-right)
                if x <= n-5 and y >= 4:
                    if all(board[y-i][x+i] == "b" for i in range(5)):
                        board[y][x] = " "
                        return (y, x)
                
                # General win check
                if is_win(board) == "Black won":
                    board[y][x] = " "
                    return (y, x)
                    
                board[y][x] = " "
    
    # Then checks if we need to block opponent
    for y in range(n):
        for x in range(n):
            if board[y][x] == " ":
                # Checks vertical sequence above
                if y > 0:
                    count = 0
                    for i in range(1, min(5, y + 1)):
                        if board[y-i][x] == "w":
                            count += 1
                        else:
                            break
                    if count >= 3:
                        return (y, x)
                
                # Checks horizontal sequence to the left
                if x > 0:
                    count = 0
                    for i in range(1, min(5, x + 1)):
                        if board[y][x-i] == "w":
                            count += 1
                        else:
                            break
                    if count >= 3:
                        return (y, x)
                
                # Checks diagonal \ sequence above-left
                if y > 0 and x > 0:
                    count = 0
                    for i in range(1, min(5, min(y, x) + 1)):
                        if board[y-i][x-i] == "w":
                            count += 1
                        else:
                            break
                    if count >= 3:
                        return (y, x)
                
                # Checks diagonal / sequence above-right
                if y > 0 and x < n-1:
                    count = 0
                    for i in range(1, min(5, min(y, n-x))):
                        if board[y-i][x+i] == "w":
                            count += 1
                        else:
                            break
                    if count >= 3:
                        return (y, x)
                
                # General win check (catches any remaining cases)
                board[y][x] = "w"
                if is_win(board) == "White won":
                    board[y][x] = " "
                    return (y, x)
                board[y][x] = " "
    
    # Otherwise evaluate moves normally
    max_score = float('-inf')
    best_move = None
    for y in range(n):
        for x in range(n):
            if board[y][x] == " ":
                board[y][x] = "b"
                current_score = score(board)
                board[y][x] = " "
                if current_score > max_score:
                    max_score = current_score
                    best_move = (y, x)
    
    return best_move

def is_win(board):

    # Checks for 5 in a row
    for col in ['b', 'w']:
        # Checks horizontal
        for y in range(len(board)):
            for x in range(len(board)-4):
                if all(board[y][x+i] == col for i in range(5)):
                    return "Black won" if col == "b" else "White won"
        
        # Checks vertical
        for x in range(len(board)):
            for y in range(len(board)-4):
                if all(board[y+i][x] == col for i in range(5)):
                    return "Black won" if col == "b" else "White won"
        
        # Checks diagonal \
        for y in range(len(board)-4):
            for x in range(len(board)-4):
                if all(board[y+i][x+i] == col for i in range(5)):
                    return "Black won" if col == "b" else "White won"
        
        # Checks diagonal /
        for y in range(4, len(board)):  # Start from bottom, go up
            for x in range(len(board)-4):  # Go right
                if all(board[y-i][x+i] == col for i in range(5)):
                    return "Black won" if col == "b" else "White won"
    
    # Checks for draw
    if not any(" " in row for row in board):
        return "Draw"
    
    return "Continue playing"

def make_empty_board(size):
    return [[" "]*size for _ in range(size)]

def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def print_board(board):
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_size // 2
            move_x = board_size // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

if __name__ == '__main__':
    play_gomoku(8)
