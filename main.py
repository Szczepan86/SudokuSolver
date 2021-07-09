import time

class SudokuSolver:
    def __init__(self, filename):
        self.sudoku = []
        with open(filename, encoding='utf-8') as file:
            for line in file:
                row = [d for d in line if d.isdigit() or d == '.']
                self.sudoku.append(row)
        self.initial_sudoku = self.sudoku
        self.candidates = [[set([str(d) for d in range(1, 10)]) for x in range(9)] for x in range(9)]
        self.iterations = 0

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

    def is_complete(self, debug=False):
        for line in self.sudoku:
            if '.' in line:
                if debug:
                    print(f'Sudoku is not solved completely!')
                return False
        return True

    def is_valid(self, debug=False):
        for i in range(9):
            row = [self.sudoku[i][x] for x in range(9) if self.sudoku[i][x] != '.']
            if len(row) != len(set(row)):
                if debug:
                    print(f'Row {row} is not an unique list')
                return False
            col = [self.sudoku[x][i] for x in range(9) if self.sudoku[x][i] != '.']
            if len(col) != len(set(col)):
                if debug:
                    print(f'Column {col} is not an unique list')
                return False
        for y_section in range(3):
            for x_section in range(3):
                elements = []
                for y in range(y_section * 3, y_section * 3 + 3):
                    for x in range(x_section * 3, x_section * 3 + 3):
                        elements.append(self.sudoku[y][x])
                section = [element for element in elements if element != '.']
                if len(section) != len(set(section)):
                    if debug:
                        print(f'Section {section} is not an unique list')
                    return False
        if debug:
            print(f'There is no mistake in the solution!')
        return True

    def brute_force(self):
        action_list = []
        while not self.is_complete() or not self.is_valid():
            if self.is_valid():
                #print(self.iterations)
                #print(self.__str__())
                next_line, next_col = self.find_last_empty()
                self.sudoku[next_line][next_col] = '1'
                self.iterations += 1
                action_list.append((next_line, next_col, 1))
            else:
                last_action = action_list.pop()
                while action_list and last_action[2] == '9':
                    self.sudoku[last_action[0]][last_action[1]] = '.'
                    last_action = action_list.pop()
                if last_action[2] == '9' and not action_list:
                    print(f'No solution found! Wrong dataset?')
                    return False
                self.sudoku[last_action[0]][last_action[1]] = str(int(last_action[2]) + 1)
                self.iterations += 1
                action_list.append((last_action[0], last_action[1], str(int(last_action[2]) + 1)))
        return True

    def find_last_empty(self):
        for line_nb in range(8, -1, -1):
            for col_nb in range(8, -1, -1):
                if self.sudoku[line_nb][col_nb] == '.':
                    return line_nb, col_nb
        return None

    def brute_force_recursive(self):
        #print(self.iterations)
        #print(self.__str__())
        if self.is_complete():
            return True
        line_nb, col_nb = self.find_last_empty()
        for i in range(1, 10):
            self.sudoku[line_nb][col_nb] = str(i)
            self.iterations += 1
            if self.is_valid() and self.brute_force_recursive():
                return True
        self.sudoku[line_nb][col_nb] = '.'
        return False

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
    start = time.time()
    sudoku = SudokuSolver('tables\\expert01.txt')
    sudoku.eliminate_all_possible_candidates()
    #sudoku.brute_force()
    sudoku.brute_force_recursive()
    print(sudoku)
    end = time.time()
    print(end - start)
    print(sudoku.iterations)
    """
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
    sudoku.is_valid()
    """
