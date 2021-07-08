class SudokuSolver:
    def __init__(self, filename):
        self.sudoku = []
        with open(filename, encoding='utf-8') as file:
            for line in file:
                row = [d for d in line if d.isdigit() or d == '.']
                self.sudoku.append(row)
        self.initial_sudoku = self.sudoku
        self.candidates = [[set([str(d) for d in range(1, 10)]) for x in range(9)] for x in range(9)]

    def eliminate_all_possible_candidates(self):
        for line_nb in range(9):
            for col_nb in range(9):
                self.eliminate_aligned_candidates(line_nb, col_nb)

    def eliminate_aligned_candidates(self, line_nb, col_nb):
        element = self.sudoku[line_nb][col_nb]
        if element.isdigit():
            for i in range(9):
                # horizontal scanning
                self.candidates[line_nb][i].discard(element)
                # vertical scanning
                self.candidates[i][col_nb].discard(element)
            # section scanning
            for y in range(line_nb // 3 * 3, line_nb // 3 * 3 + 3):
                for x in range(col_nb // 3 * 3, col_nb // 3 * 3 + 3):
                    self.candidates[y][x].discard(element)
            # remove all candidates when digit is known
            self.candidates[line_nb][col_nb] = set()

    def find_unique_candidates(self):
        for line_nb in range(9):
            for col_nb in range(9):
                for candidate in self.candidates[line_nb][col_nb]:
                    # horizontal scanning
                    other_candidates = -1
                    for i in range(9):
                        if candidate in self.candidates[line_nb][i]:
                            other_candidates += 1
                            if other_candidates > 0:
                                continue
                    if not other_candidates:
                        self.sudoku[line_nb][col_nb] = candidate
                        self.eliminate_aligned_candidates(line_nb, col_nb)
                        break

                    # vertical scanning
                    other_candidates = -1
                    for i in range(9):
                        if candidate in self.candidates[i][col_nb]:
                            other_candidates += 1
                            if other_candidates > 0:
                                continue
                    if not other_candidates:
                        self.sudoku[line_nb][col_nb] = candidate
                        self.eliminate_aligned_candidates(line_nb, col_nb)
                        break

                    # section scanning
                    other_candidates = -1
                    for y in range(line_nb // 3 * 3, line_nb // 3 * 3 + 3):
                        for x in range(col_nb // 3 * 3, col_nb // 3 * 3 + 3):
                            if candidate in self.candidates[i][col_nb]:
                                other_candidates += 1
                                if other_candidates > 0:
                                    continue
                    if not other_candidates:
                        self.sudoku[line_nb][col_nb] = candidate
                        self.eliminate_aligned_candidates(line_nb, col_nb)
                        break

    def update(self):
        counter = 0
        for line_nb in range(9):
            for col_nb in range(9):
                if len(self.candidates[line_nb][col_nb]) == 1:
                    counter += 1
                    self.sudoku[line_nb][col_nb] = str(self.candidates[line_nb][col_nb].pop())
        if counter > 0:
            print(f'{counter} digit(s) updated.')
            return True
        print(f'No digits updated.')
        return False

    def validate(self):
        for line in self.sudoku:
            if '.' in line:
                print(f'Sudoku is not solved completely!')
                return False
        for i in range(9):
            if len(set([self.sudoku[i][x] for x in range(9)])) < 9:
                print(f'Row {[self.sudoku[i][x] for x in range(9)]} is not an unique list')
                return False
            if len(set([self.sudoku[x][i] for x in range(9)])) < 9:
                print(f'Column {[self.sudoku[x][i] for x in range(9)]} is not an unique list')
                return False
        for y_section in range(3):
            for x_section in range(3):
                elements = []
                for y in range(y_section * 3, y_section * 3 + 3):
                    for x in range(x_section * 3, x_section * 3 + 3):
                        elements.append(self.sudoku[y][x])
                if len(set(elements)) < 9:
                    print(f'Section {[self.sudoku[x][i] for x in range(9)]} is not an unique list')
                    return False
        print(f'Sudoku is solved properly!')
        return True

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
    sudoku.eliminate_all_possible_candidates()
    while True:
        print('find unique')
        sudoku.find_unique_candidates()
        print('update')
        if not sudoku.update():
            break
    sudoku.validate()