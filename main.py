def get_sudoku(filename):
    sudoku_table = []
    with open(filename, encoding='utf-8') as file:
        for line in file:
            row = [d for d in line if d.isdigit()]
            sudoku_table.append(row)
        return sudoku_table
    return None


def print_sudoku(sudoku):
    for line_nb, line in enumerate(sudoku):
        if line_nb % 3 == 0 and line_nb < len(line) and line_nb:
            print(21 * '-')
        for col_nb, element in enumerate(line):
            if col_nb % 3 == 0 and col_nb < len(line) and col_nb:
                print('|', end=' ')
            if element == '0':
                element = '.'
            print(element, end=' ')
        print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sudoku = get_sudoku('tables\\sudoku01.txt')
    print_sudoku(sudoku)
