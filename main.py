class SudokuSolver:
    def __init__(self, filename):
        self.sudoku = []
        with open(filename, encoding='utf-8') as file:
            for line in file:
                row = [d for d in line if d.isdigit() or d == '.']
                self.sudoku.append(row)
        self.initial_sudoku = self.sudoku
        self.candidates = [[set(range(1, 10)) for x in range(9)] for x in range(9)]
        print(self.candidates)

    def scanning(self):
        for line_nb, line in enumerate(self.sudoku):
            for col_nb, element in enumerate(line):
                if element.isdigit() and self.candidates[line_nb][col_nb]:
                    for i in range(9):
                        # horizontal scanning
                        self.candidates[line_nb][i].discard(int(element))
                        # vertical scanning
                        self.candidates[i][col_nb].discard(int(element))
                    # section scanning
                    for y in range(line_nb // 3 * 3, line_nb // 3 * 3 + 3):
                        for x in range(col_nb // 3 * 3, col_nb // 3 * 3 + 3):
                            self.candidates[y][x].discard(int(element))
                    # remove all candidates when digit is known
                    self.candidates[line_nb][col_nb] = set()

    def __str__(self):
        output = ''
        for line_nb, line in enumerate(self.sudoku):
            if line_nb % 3 == 0 and line_nb < len(line) and line_nb:
                output += f'{21 * "-"}\n'
            for col_nb, element in enumerate(line):
                if col_nb % 3 == 0 and col_nb < len(line) and col_nb:
                    output += f'| '
                output += f'{element} '
            output += f'\n'
        return output


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sudoku = SudokuSolver('tables\\sudoku01.txt')
    print(sudoku)
    sudoku.scanning()
