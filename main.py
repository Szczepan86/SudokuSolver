import time


class SudokuSolver:
    def __init__(self, filename, debug=False):
        """
        Read sudoku table and create basic attributes during object creation
        :param filename: filename of sudoku array (9 lines x 9 digits, where 0 = empty place)
        :param debug: additional printing for debug purpose
        """
        # sudoku is a two dimensional 9x9 array to store sudoku content
        self.sudoku = []
        with open(filename, encoding='utf-8') as file:
            for line in file:
                row = [int(d) for d in line if d.isdigit()]
                assert len(row) == 9, 'Incorrect row length'
                self.sudoku.append(row)
            assert len(self.sudoku) == 9, 'Incorrect number of lines'
        # initial_sudoku - copy of sudoku table, just in case rollback is needed
        self.initial_sudoku = list(map(list, self.sudoku))
        # 9x9 array of sets with all candidates for selected element
        # candidate set contains all possible digits which were not excluded by the algorithm
        self.candidates = [[set([d for d in range(1, 10)]) for x in range(9)] for x in range(9)]
        self.debug = debug

    def solve(self):
        """
        Tries to solve sudoku table. Rollback to initial table if no solution found.
        :return: True when sudoku is solved, False otherwise
        """
        # first, iterate over table and exclude all obvious candidates based on initial sudoku table
        self.eliminate_all_possible_candidates()
        while True:
            # repeat searching for unique and single candidates as long as we have any results
            unique_candidates_found = self.find_unique_candidates()
            single_candidates_found = self.find_single_candidates()
            if not unique_candidates_found and not single_candidates_found:
                break
        # sudoku still not complete? time to launch brute force
        if not sudoku.is_complete() and not sudoku.brute_force_recursive():
            self.sudoku = list(map(list, self.initial_sudoku))
            return False
        return True

    def eliminate_all_possible_candidates(self):
        """
        Iterate over whole sudoku table and eliminate all unnecessary candidates.
        :return: None
        """
        for line_nb in range(9):
            for col_nb in range(9):
                self.eliminate_aligned_candidates(line_nb, col_nb)

    def eliminate_aligned_candidates(self, line_nb, col_nb):
        """
        If digit is known, then it's removed from candidate list for line, column and section.
        :param line_nb: line number of selected digit
        :param col_nb: column number of selected digit
        :return: None
        """
        element = self.sudoku[line_nb][col_nb]
        if element:
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
            self.candidates[line_nb][col_nb] = set([element])

    def find_unique_candidates(self):
        """
        Iterate over sudoku table and check if any of the candidates is unique within a line, column or section.
        If it is - then it's a match.
        :return: None
        """
        # counter just to track if there was any progress using this method
        counter = 0
        # iterate over whole 9x9 matrix
        for line_nb in range(9):
            for col_nb in range(9):
                # check all candidates if they're unique in their context (line / column / section)
                for candidate in self.candidates[line_nb][col_nb]:
                    if self.sudoku[line_nb][col_nb]:
                        continue
                    # horizontal scanning
                    # other_candidates initialized with -1 to avoid counting current candidate as the other one
                    other_candidates = -1
                    for i in range(9):
                        if candidate in self.candidates[line_nb][i]:
                            other_candidates += 1
                            if other_candidates > 0:
                                continue
                    if other_candidates:
                        # vertical scanning - launched only if previous range was not unique
                        other_candidates = -1
                        for i in range(9):
                            if candidate in self.candidates[i][col_nb]:
                                other_candidates += 1
                                if other_candidates > 0:
                                    continue
                    if other_candidates:
                        # section scanning - launched only if previous ranges were not unique
                        other_candidates = -1
                        for y in range(line_nb // 3 * 3, line_nb // 3 * 3 + 3):
                            for x in range(col_nb // 3 * 3, col_nb // 3 * 3 + 3):
                                if candidate in self.candidates[i][col_nb]:
                                    other_candidates += 1
                                    if other_candidates > 0:
                                        continue
                    if not other_candidates:
                        # no other candidates found in line / column / section - so it's a match!
                        self.sudoku[line_nb][col_nb] = candidate
                        # as new digit was revealed - we have to eliminate all corresponding candidates
                        self.eliminate_aligned_candidates(line_nb, col_nb)
                        counter += 1
                        break
        # check if we were lucky this time
        if counter > 0:
            return True
        return False

    def find_single_candidates(self):
        """
        Iterate over sudoku table and check if there are no other candidates for specific position.
        If there are not - then it's a match.
        :return:
        """
        counter = 0
        # iterate over whole sudoku table
        for line_nb in range(9):
            for col_nb in range(9):
                # if only one candidate and sudoku not updated for this pos - it's a new match!
                if len(self.candidates[line_nb][col_nb]) == 1 and self.sudoku[line_nb][col_nb] == 0:
                    counter += 1
                    element = next(iter(self.candidates[line_nb][col_nb]))
                    self.sudoku[line_nb][col_nb] = element
        if counter > 0:
            if self.debug:
                print(f'{counter} position(s) updated.')
            return True
        if self.debug:
            print(f'No positions updated.')
        return False

    def is_complete(self):
        """
        Check if sudoku table is solved.
        :return: None
        """
        for line in self.sudoku:
            if 0 in line:
                if self.debug:
                    print(f'Sudoku is not solved completely!')
                return False
        return True

    def is_valid(self):
        """
        Check if sudoku table is valid (no duplicates in lines / rows / sections)
        :return: True when table is valid, False otherwise
        """
        for i in range(9):
            # verify there's no duplication in rows
            row = [self.sudoku[i][x] for x in range(9) if self.sudoku[i][x] != 0]
            if len(row) != len(set(row)):
                if self.debug:
                    print(f'Row {row} is not an unique list')
                return False
            # verify there's no duplication in cols
            col = [self.sudoku[x][i] for x in range(9) if self.sudoku[x][i] != 0]
            if len(col) != len(set(col)):
                if self.debug:
                    print(f'Column {col} is not an unique list')
                return False
        # verify there's no duplication in sections
        for y_section in range(3):
            for x_section in range(3):
                elements = []
                for y in range(y_section * 3, y_section * 3 + 3):
                    for x in range(x_section * 3, x_section * 3 + 3):
                        elements.append(self.sudoku[y][x])
                section = [element for element in elements if element != 0]
                if len(section) != len(set(section)):
                    if self.debug:
                        print(f'Section {section} is not an unique list')
                    return False
        if self.debug:
            print(f'There is no mistake in the solution!')
        return True

    def brute_force_recursive(self):
        """
        Recursive brute force algorithm. It's optimized to look only for available candidates based on the rest of
        confirmed sudoku digits.
        :return: True when solved and validated, False otherwise
        """
        # sudoku complete? so we're done here
        if self.is_complete():
            return True
        # get the last empty element
        line_nb, col_nb = self.find_last_empty()
        # iterate over candidates for empty element
        for i in self.candidates[line_nb][col_nb]:
            self.sudoku[line_nb][col_nb] = i
            # is it valid after using selected candidate? if so - go for the next one
            if self.is_valid() and self.brute_force_recursive():
                return True
        # no candidates looks correct for current position - we have to go back and change previous value
        self.sudoku[line_nb][col_nb] = 0
        return False

    def find_last_empty(self):
        """
        Find the last empty element in sudoku table.
        :return: line number and column number of the last empty element, None if none found
        """
        for line_nb in range(8, -1, -1):
            for col_nb in range(8, -1, -1):
                if self.sudoku[line_nb][col_nb] == 0:
                    return line_nb, col_nb
        return None

    def __str__(self):
        """
        Str override method, returns easy to read sudoku visualisation
        :return: sudoku table as string
        """
        output = ''
        for line_nb, line in enumerate(self.sudoku):
            if line_nb % 3 == 0 and line_nb < len(line) and line_nb:
                output += f'{21 * "-"}\n'
            for col_nb, element in enumerate(line):
                if col_nb % 3 == 0 and col_nb < len(line) and col_nb:
                    output += f'| '
                if element:
                    output += f'{element} '
                else:
                    output += f'. '
            output += f'\n'
        return output


if __name__ == '__main__':
    # just to track a computation time
    start = time.time()
    # create sudoku instance and read sudoku file
    sudoku = SudokuSolver('tables\\test01.txt')
    print(sudoku)
    # try to solve sudoku and print it when solved
    if sudoku.solve():
        print(sudoku)
    else:
        print("No solution found - impossible dataset?")
    end = time.time()
    print(end - start)
