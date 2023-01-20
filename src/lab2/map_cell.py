'''
Extra Credit Task-

Tic tac toe input
Here's the backstory for this challenge: imagine you're writing a tic-tac-toe game,
where the board looks like this:

1:  X | O | X
   -----------
2:    |   |
   -----------
3:  O |   |
    A   B   C
The board is represented as a 2D list:

board = [
    ["X", "O", "X"],
    [" ", " ", " "],
    ["O", " ", " "],
]
Imagine if your user enters "C1" and you need to see if there's an X or O in that cell
on the board. To do so, you need to translate from the string "C1" to row 0 and column
2 so that you can check board[row][column].

Your task is to write a function that can translate from strings of length 2 to a tuple
(row, column). Name your function get_row_col; it should take a single parameter which is
a string of length 2 consisting of an uppercase letter and a digit.

For example, calling get_row_col("A3") should return the tuple (2, 0) because A3 corresponds
to the row at index 2 and column at index 0in the board.
'''

from itertools import product

ascii_base = ord('A')
def get_row_col(idx):
    """
    > This function takes a single parameter which is represents a position on the board
    and translates it into coordinates (row, column).

    :param idx: the position on the board as a string of length 2 consisting of an uppercase
    letter and a digit
    :return: A tuple of x and y coordinates on the board.
    """

    return (int(idx[1]) - 1, ord(idx[0]) - ascii_base)

def main():
    """
    Main entrance to the program.
    Validates the function get_row_col works as intended.
    """

    board = [
        ["X", "O", "X"],
        [" ", " ", " "],
        ["O", " ", " "],
    ]
    x_labels = ['A', 'B', 'C'] # left -> right
    y_labels = [3, 2, 1]       # bottom -> up
    n_x_labels = len(x_labels)

    # labels/board validation
    assert n_x_labels == len(y_labels) and (n_x_labels ** 2) == (len(board) * len(board[0]))

    # Python's best value sell: ridiculous one-liners
    test_board = list(zip(*[[f"{x}{str(y)}" for x, y in product(x_labels, y_labels)][i:i + n_x_labels] for i in range(0, n_x_labels ** 2, n_x_labels)]))[::-1]

    # string representation of each cell
    for test_row in test_board:
        print(test_row)

    # coords representation of each cell
    for test_row in test_board:
        print([get_row_col(test) for test in test_row])

    # contents of each cell in the og board to show the coords align
    for test_row in test_board:
        coords = [get_row_col(test) for test in test_row]
        print([board[x][y] for x, y in coords])

if __name__ == "__main__":
    main()
 