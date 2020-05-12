def new_board(n, p):
    board = []
    for x in range(n):
        temp_row = [0] * p
        temp_white_row = [1] * p
        temp_black_row = [2] * p

        if x == 0 or x == 1:
            board.append(temp_white_row)
        elif x == 2:
            board.append(temp_row)
        elif x == 3 or x == 4:
            board.append(temp_black_row)

    return board


def display(board, n, p):
    print(" ", end=" ")
    for col in range(p):
        print(col, end=" ")
    print()
    for row in range(n):
        print(row, end=" ")
        for col in range(p):
            pawn = board[row][col]
            if pawn == 0:
                print(".", end=" ")
            elif pawn == 1:
                print("x", end=" ")
            elif pawn == 2:
                print("o", end=" ")
        print()


def possible_pawn(board, n, p, player, i, j):
    forward_move, diagonal_left, diagonal_right = False, False, False
    forward_move_coords, diagonal_left_coords, diagonal_right_coords = (0, 0), (0, 0), (0, 0)

    is_possible = False

    pawn = board[i][j]
    way = 0

    # Pawn selected doesn't belong to player
    if pawn != player:
        return False, forward_move, diagonal_left, diagonal_right

    if pawn == 1:
        way = 1
    elif pawn == 2:
        way = -1

    # Avoid having a row equal to a minus value because it will
    # cause the list to be looped over and will return an actual value instead of an error.
    row = i + way
    if 0 < row < n:
        pass
    else:
        return False, forward_move, diagonal_left, diagonal_right

    # Defining the possible moves. Try except blocks are used in the case that
    # a move is outside of the board (which will return an index out of range error).
    try:
        forward_move = board[row][j]
        forward_move_coords = (row, j)
    except:
        pass

    try:
        diagonal_left = board[row][j - 1]
        diagonal_left_coords = (row, j - 1)
    except:
        pass

    try:
        diagonal_right = board[row][j + 1]
        diagonal_right_coords = (row, j + 1)
    except:
        pass

    # If the three of them are booleans and not ints it then all the moves checked failed,
    # which means that the selected pawn is in the last row of the enemy side.
    is_possible = type(forward_move) == int or type(diagonal_left) == int or type(diagonal_right) == int

    if is_possible:
        return True, forward_move_coords, diagonal_left_coords, diagonal_right_coords
    else:
        return False, forward_move, diagonal_left, diagonal_right


def select_pawn(board, n, p, player):
    row_coordinate = 0
    col_coordinate = 0

    row_is_invalid = True
    col_is_invalid = True

    while row_is_invalid or col_is_invalid:
        try:
            row_coordinate = int(input("Select a pawn, row: "))
            col_coordinate = int(input("Select a pawn, column: "))
        except:
            pass

        is_possible, fm, dl, dr = possible_pawn(board, n, p, player, row_coordinate, col_coordinate)

        if is_possible:
            row_is_invalid = False
            col_is_invalid = False

    return row_coordinate, col_coordinate


def possible_destination(board, n, p, player, i, j, row_coordinate, col_coordinate):
    is_possible, fm, dl, dr = possible_pawn(board, n, p, player, i, j)

    if fm[0] == row_coordinate and fm[1] == col_coordinate:
        return True
    elif dl[0] == row_coordinate and dl[1] == col_coordinate:
        return True
    elif dr[0] == row_coordinate and dr[1] == col_coordinate:
        return True
    else:
        return False


def select_destination(board, n, p, player, i, j):
    row_coordinate = 0
    col_coordinate = 0

    row_is_invalid = True
    col_is_invalid = True

    while row_is_invalid or col_is_invalid:
        try:
            row_coordinate = int(input("Select a destination, row: "))
            col_coordinate = int(input("Select a destination, column: "))
        except:
            pass

        if possible_destination(board, n, p, player, i, j, row_coordinate, col_coordinate):
            break

    return row_coordinate, col_coordinate


def put_pawn(board, from_row, from_col, to_row, to_col, player):
    board[from_row][from_col] = 0
    board[to_row][to_col] = player
    return board


def not_finished(board, n, player):
    start_index = 0
    raw_board = [item for sublist in board for item in sublist]

    # Check if player is eliminated from the board
    if player not in raw_board:
        return False

    if player == 1:
        start_index = 0
    elif player == 2:
        start_index = n - 1

    # Check if enemy player is in the last row of the enemy side
    if player == 1:
        if 2 in board[start_index]:
            print("waypoint 1")
            print(start_index)
            return False
    elif player == 2:
        if 1 in board[start_index]:
            print(start_index)
            print("waypoint 2")
            return False

    return True


def switch_player(current_player):
    if current_player == 1:
        return 2
    elif current_player == 2:
        return 1


def breaktrough(n, p):
    board = new_board(n, p)
    print("------------------------")
    print("Welcome to Breaktrough !")
    print("------------------------")
    display(board, n, p)

    current_player = 1

    print("It's Player {}'s turn !".format(current_player))
    from_row, from_col = select_pawn(board, n, p, current_player)
    to_row, to_col = select_destination(board, n, p, current_player, from_row, from_col)
    board = put_pawn(board, from_row, from_col, to_row, to_col, current_player)
    game_in_progress = not_finished(board, n, current_player)
    print(game_in_progress)
    display(board, n, p)
    current_player = switch_player(current_player)
    print("----------------------")

    while game_in_progress:
        print("It's Player {}'s turn !".format(current_player))
        from_row, from_col = select_pawn(board, n, p, current_player)
        to_row, to_col = select_destination(board, n, p, current_player, from_row, from_col)
        board = put_pawn(board, from_row, from_col, to_row, to_col, current_player)
        game_in_progress = not_finished(board, n, current_player)
        display(board, n, p)
        current_player = switch_player(current_player)
        print("----------------------")

    print("Player {} won !", current_player)


breaktrough(5, 4)