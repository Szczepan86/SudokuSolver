def get_sudoku(filename):
    sudoku_table = []
    with open(filename, encoding='utf-8') as file:
        for line in file:
            row = [d for d in line if d.isdigit()]
            sudoku_table.append(row)
        return sudoku_table
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sudoku = get_sudoku('tables\\sudoku01.txt')
    print(sudoku)
