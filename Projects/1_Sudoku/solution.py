from utils import *


row_units = [cross(r, cols) for r in rows]

column_units = [cross(rows, c) for c in cols]

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]

unitlist = row_units + column_units + square_units

diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))],
                  [rows[-(i+1)] + cols[i] for i in range(len(rows))]]

unitlist = unitlist + diagonal_units

# Must be called after all units (including diagonals) are added to the
# unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def remove(str1, str2):
    """Remove all characters in str1 from str2.

    Args:
        str1:  The string containing the characters to remove.
        str2:  The string to remove the characters from.

    Returns:
        str:  str2 with characters from str1 removed.
    """

    for c in str1:
        str2 = str2.replace(c, '')

    return str2


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated
    boxes in a unit and there are only two digits that can go in those two
    boxes, then those two digits can be eliminated from the possible
    assignments of all other boxes in the same unit.

    Args:
        values(dict): A dictionary of the form {'box_name': '123456789', ...}.

    Returns:
        dict: The values dictionary with values from naked twins removed from
            peers.
    """

    values = values.copy()

    for box1 in boxes:
        if len(values[box1]) == 2:
            for box2 in peers[box1]:
                if values[box2] == values[box1]:
                    for peer in (peers[box1] & peers[box2]):
                        values[peer] = remove(values[box1], values[peer])

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Args:
        values(dict): A dictionary of the form {'box_name': '123456789', ...}.

    Returns:
        dict: The values dictionary with the values from solved boxes removed
            from peers.
    """

    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]

    values = values.copy()

    for box in solved_boxes:
        for peer in peers[box]:
            values[peer] = values[peer].replace(values[box], '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a
    certain digit, then that box must be assigned that digit.

    Args:
        values(dict): A dictionary of the form {'box_name': '123456789', ...}.

    Returns:
        dict: The values dictionary where boxes with only one value choice are
            assigned that value.
    """

    values_string = '123456789'

    values = values.copy()

    for unit in unitlist:

        value_blist_dict = {v: [] for v in values_string}

        for box in unit:
            for v in values[box]:
                value_blist_dict[v].append(box)

        for v in value_blist_dict:
            blist = value_blist_dict[v]
            if len(blist) == 1:
                values[blist[0]] = v

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Args:
        values(dict): A dictionary of the form {'box_name': '123456789', ...}.
            The contents of the values parameter is modified by this function.

    Returns:
        dict or bool: The values dictionary, if the number of solved boxes
            has increased, otherwise False.
    """

    stalled = False
    while not stalled:

        solved_count_before = len([box for box in values.keys()
                                   if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_count_after = len([box for box in values.keys()
                                  if len(values[box]) == 1])

        stalled = (solved_count_before == solved_count_after)

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve
    puzzles that cannot be solved by repeated reduction alone.

    Args:
        values(dict): A dictionary of the form {'box_name': '123456789', ...}.
            The contents of the values parameter is modified by this function.

    Returns:
        dict or bool: The values dictionary, if all boxes have been solved,
            otherwise False.
    """

    values = reduce_puzzle(values)
    if values is False:
        return False

    if all(len(values[b]) == 1 for b in boxes):
        return values

    _, box = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)

    for v in values[box]:

        test_values = values.copy()
        test_values[box] = v

        test_values = search(test_values)
        if test_values:
            return test_values

    return False


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint
    propagation

    Args:
        grid(string): A string representing a sudoku grid.
            Ex. '2.............62....1....7.' \
                '..6..8...3...9...7...6..4..' \
                '.4....8....52.............3'

    Returns:
        dict or False: The dictionary representation of the final sudoku grid
            or False if no solution exists.
    """

    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7.' \
                       '..6..8...3...9...7...6..4..' \
                       '.4....8....52.............3'

    with open('test_data/other.txt', 'r') as f:
        puzzles = f.readlines()

    print()
    for i, p in enumerate(puzzles):
        p = p.rstrip()
        print('='*100)
        print()
        print('Puzzle {}: {}'.format(i, p))
        print()
        display(grid2values(p))
        print()
        print("Result...")
        print()
        result = solve(p)
        if result is False:
            print('No solution found.')
        else:
            display(result)
        print()

    # try:
    #     import PySudoku
    #     PySudoku.play(grid2values(diag_sudoku_grid), result, history)
    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. '
    #           + 'Not a problem! It is not a requirement.')
