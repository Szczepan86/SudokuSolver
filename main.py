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
            # remove all other candidates when digit is known
            self.candidates[line_nb][col_nb] = set(element)

    def find_unique_candidates(self):
        counter = 0
        for line_nb in range(9):
            for col_nb in range(9):
                for candidate in self.candidates[line_nb][col_nb]:
                    if self.sudoku[line_nb][col_nb].isdigit():
                        continue
                    # horizontal scanning
                    other_candidates = -1
                    for i in range(9):
                        if candidate in self.candidates[line_nb][i]:
                            other_candidates += 1
                            if other_candidates > 0:
                                continue
                    if other_candidates:
                        # vertical scanning
                        other_candidates = -1
                        for i in range(9):
                            if candidate in self.candidates[i][col_nb]:
                                other_candidates += 1
                                if other_candidates > 0:
                                    continue
                    if other_candidates:
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
                        counter += 1
                        break

        if counter > 0:
            print(f'{counter} position(s) updated.')
            return True
        print(f'No positions updated.')
        return False

    def find_single_candidates(self):
        counter = 0
        for line_nb in range(9):
            for col_nb in range(9):
                if len(self.candidates[line_nb][col_nb]) == 1 and self.sudoku[line_nb][col_nb] == '.':
                    counter += 1
                    element = next(iter(self.candidates[line_nb][col_nb]))
                    self.sudoku[line_nb][col_nb] = str(element)
        if counter > 0:
            print(f'{counter} position(s) updated.')
            return True
        print(f'No positions updated.')
        return False

    def is_complete(self):
        for line in self.sudoku:
            if '.' in line:
                print(f'Sudoku is not solved completely!')
                return False
        return True

    def validate(self):
        for i in range(9):
            row = [self.sudoku[i][x] for x in range(9) if self.sudoku[i][x] != '.']
            if len(row) != len(set(row)):
                print(f'Row {row} is not an unique list')
                return False
            col = [self.sudoku[x][i] for x in range(9) if self.sudoku[x][i] != '.']
            if len(col) != len(set(col)):
                print(f'Column {col} is not an unique list')
                return False
        for y_section in range(3):
            for x_section in range(3):
                elements = []
                for y in range(y_section * 3, y_section * 3 + 3):
                    for x in range(x_section * 3, x_section * 3 + 3):
                        elements.append(self.sudoku[y][x])
                section = [element for element in elements if elements != '.']
                if len(elements) != len(set(elements)):
                    print(f'Section {[self.sudoku[x][i] for x in range(9)]} is not an unique list')
                    return False
        print(f'There is no mistake in the solution!')
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
    sudoku = SudokuSolver('tables\\wrong01.txt')
    print(sudoku)
    sudoku.eliminate_all_possible_candidates()
    while True:
        unique_candidates_found = sudoku.find_unique_candidates()
        print(sudoku)
        single_candidates_found = sudoku.find_single_candidates()
        print(sudoku)
        if not unique_candidates_found and not single_candidates_found:
            break
    sudoku.is_complete()
    sudoku.validate()