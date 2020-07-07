# write your code here
def get_new_coord(current_move):
    while True:
        new_input = input('Enter the coordinates:')

        if new_input.isalpha():
            print('You should enter numbers!')
            continue
        if not all([1 <= int(coord) <= 3 for coord in new_input.split()]):
            print('Coordinates should be from 1 to 3!')
            continue
        col, row = [int(coord) for coord in new_input.split()]
        if user_input_array[3-row][col-1] != '_':
            print("This cell is occupied! Choose another one!")
            continue
        break
    user_input_array[3-row][col-1] = current_move
    current_move = 'O' if current_move == 'X' else 'X'
    return user_input_array, current_move

def check_status(user_input_array):
    user_input = get_string_from_array(user_input_array)

    first_row = user_input[:3]
    second_row = user_input[3:6]
    third_row = user_input[6:]
    first_col = '{0}{3}{6}'.format(*user_input)
    second_col = '{1}{4}{7}'.format(*user_input)
    third_col = '{2}{5}{8}'.format(*user_input)
    forward_diag = '{2}{4}{6}'.format(*user_input)
    back_diag = '{0}{4}{8}'.format(*user_input)
    all_seq = [first_row,
            second_row,
            third_row,
            first_col,
            second_col,
            third_col,
            forward_diag,
            back_diag
           ]

    result_X = check_X(all_seq)
    result_O = check_O(all_seq)
    if result_O and result_X or (abs(user_input.count('O') - user_input.count('X')) >= 2):
        return 'Impossible'
    elif result_O:
        return 'O wins'
    elif result_X:
        return 'X wins'
    else:
        if '_' in user_input:
            return 'Game not finished'
        else:
            return 'Draw'
def check_X(all_seq):
    return any(['XXX' == seq for seq in all_seq])
def check_O(all_seq):
    return any(['OOO' == seq for seq in all_seq])
def print_tic_tac(user_input_array):
    print('---------')
    print('|', end=' ')
    for idx, char in enumerate(get_string_from_array(user_input_array)):
        if idx!= 0 and idx % 3 == 0:
            print('|')
            print('|', end=' ')
        print(char, end=' ')

    print('|')
    print('---------')

def get_string_from_array(user_input_array):
    return [move for row in user_input_array for move in row]


user_input = '_'*9

first_row = user_input[:3]
second_row = user_input[3:6]
third_row = user_input[6:]
user_input_array = [list(row) for row in [first_row, second_row, third_row]]
print_tic_tac(user_input_array)

move = 'X'
while True:
    user_input_array, move = get_new_coord(move)
    print_tic_tac(user_input_array)
    status = check_status(user_input_array)
    if status != 'Game not finished':
        break
print(status)
