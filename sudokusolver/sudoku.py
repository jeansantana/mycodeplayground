#!/usr/bin/env python

# Copyright (c) 2011 Xueqiao Xu <xueqiaoxu@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import division

from dlx import DLXSolver


class SudokuSolver(object):

    digits = set(map(str, range(1, 10)))

    GRID_OFFSET = 0
    ROW_OFFSET = 81
    COLUMN_OFFSET = 162
    BOX_OFFSET = 243

    def __init__(self):
        self._dlx_solver = DLXSolver()

    def solve(self, puzzle):
        """Solve the given Soduku puzzle

        :Parameters:
            puzzle: str

                The puzzle can either be single-lined or multi-lined.
                Use 1-9 to represent the filled numbers, any other printable
                characters will be considered as blanks.

        :Return:
            solution: [(row, col, val), ... ]
                
                The solution is a list of a 3-elements tuple.
                both row and col are 0-8, val is 1-9
        """

        dlx_matrix = self._construct(puzzle)
        solution = self._dlx_solver.solve(dlx_matrix, 324)
        return [(row, col, val + 1) for row, col, val in solution]

    def _construct(self, puzzle):
        """Helper function for constructing a matrix used by 
        DLXSolver from the given puzzle
        """
    
        linear_puzzle = ''.join(puzzle.split())
        if len(linear_puzzle) != 81:
            print 'Invalid puzzle.'
            return

        dlx_matrix = {}
        for i, c in enumerate(linear_puzzle):
            row, col = divmod(i, 9)
            if c in self.digits:
                val = int(c) - 1
                dlx_matrix[(row, col, val)] = self._get_ones(row, col, val)
            else:
                for val in xrange(9):
                    dlx_matrix[(row, col, val)] = self._get_ones(row, col, val)
        return dlx_matrix

    def _get_ones(self, row, col, val):
        """Helper function to generate a 4-elements list from the
        given row, col and val. The value of each element indicates 
        there's a node in the corresponding column in the DLX matrix.
        """

        ones = [9 * row + col + self.GRID_OFFSET,
                9 * row + val + self.ROW_OFFSET,
                9 * col + val + self.COLUMN_OFFSET ,
                (row // 3 * 3 + col // 3) * 9 + val + self.BOX_OFFSET]
        return ones


if __name__ == '__main__':

    import cStringIO
    
    sudoku_solver = SudokuSolver()
    matrix = [[x for x in xrange(9)] for y in xrange(9)]
    cnt = 1

    with open('top95sudoku') as f:
        for puzzle in f.readlines():
            solution = sudoku_solver.solve(puzzle)
            if not solution:
                print 'Cannot find the solution'
                continue
            for row, col, val in solution:
                matrix[row][col] = val

            output = cStringIO.StringIO()
            for r in xrange(9):
                if r % 3 == 0:
                    output.write('+-------' * 3 + '+\n')
                for c in xrange(9):
                    if c % 3 == 0:
                        output.write('| ')
                    output.write(str(matrix[r][c]) + ' ')
                output.write('|\n')
            output.write('+-------' * 3 + '+')
            print output.getvalue()
            output.close()
            
            print 'solved %d puzzles' % cnt
            cnt += 1
