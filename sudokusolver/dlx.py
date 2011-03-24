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


__all__ = ['DLXSolver']

class Node(object):

    def __init__(self, left = None, right = None, up = None, down = None,
                 row_header = None, column_header = None):
        self.left = left or self
        self.right = right or self
        self.up = up or self
        self.down = down or self

        self.column_header = column_header
        self.row_header = row_header


    def nodes_in_direction(self, dir):
        """Generator for nodes in the given direction
        
        :Parameters:
            dir: str
                direction can be 'up', 'down', 'left' or 'right'
        """
        node = getattr(self, dir)
        while node != self:
            yield node
            node = getattr(node, dir)


class ColumnHeader(Node):

    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)

        self.count = 0


class RowHeader(Node):

    def __init__(self, value, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)

        self.value = value
        self.row_header = self


class DLXSolver(object):

    def __init__(self):
        pass


    def solve(self, matrix, num_columns):
        """Solve the exact cover problem of the given matrix.

        :Parameters:
            matrix : {k: [x0, x1, x2, ..., xn], ... }

                A sample matrix is:

                    matrix = {1: [2, 4, 5],
                              2: [0, 3, 6],
                              3: [1, 2, 5],
                              4: [0, 3],
                              5: [1, 6],
                              6: [3, 4, 6]}

                *Note*: the greatest item in the value list should not 
                exceed num_columns - 1

            num_columns : int
            
                indicate how many columns the target matrix have

        :Return:
            solution : [k]
                
                a list holding the keys/ids of the selected rows
        """
        self._partial_answer = {}
        self._k = 0
        self._construct(matrix, num_columns)
        self._search(0)
        
        return [self._partial_answer[k] for k in xrange(self._k)]
       

    def _construct(self, matrix, num_columns):
        """Helper function for constructing the linked nodes 
        from the given matrix.
        """
        
        self.root = Node()
        self.column_headers = []

        # construct column headers
        for i in xrange(num_columns):
            new_column_header = ColumnHeader(left = self.root.left, 
                                             right = self.root)
            self.root.left.right = new_column_header
            self.root.left = new_column_header
            self.column_headers.append(new_column_header)

        for k in matrix:

            if not matrix[k]: 
                continue

            # construct row header
            column_id_sorted = sorted(matrix[k])
            column_header = self.column_headers[column_id_sorted[0]]
            column_header.count += 1

            new_row_header = RowHeader(k, 
                                       up = column_header.up, 
                                       down = column_header,
                                       column_header = column_header)
            column_header.up.down = new_row_header
            column_header.up = new_row_header


            # construct remaining nodes
            column_id_sorted.pop(0)
            
            for column_id in column_id_sorted:

                column_header = self.column_headers[column_id]
                column_header.count += 1

                new_node = Node(left = new_row_header.left, 
                                right = new_row_header,
                                up = column_header.up,
                                down = column_header,
                                column_header = column_header,
                                row_header = new_row_header)

                new_row_header.left.right = new_node
                new_row_header.left = new_node
                column_header.up.down = new_node
                column_header.up = new_node


    def _cover(self, column_header):
        
        column_header.right.left = column_header.left
        column_header.left.right = column_header.right

        for col_node in column_header.nodes_in_direction('down'):
            for node in col_node.nodes_in_direction('right'):
                node.down.up = node.up
                node.up.down = node.down
                node.column_header.count -= 1
                

    def _uncover(self, column_header):

        for col_node in column_header.nodes_in_direction('up'):
            for node in col_node.nodes_in_direction('left'):
                node.down.up = node
                node.up.down = node
                node.column_header.count += 1

        column_header.right.left = column_header
        column_header.left.right = column_header


    def _search(self, k):

        if self.root.right == self.root:
            self._k = k
            return True

        column_header = min(
                [header for header in self.root.nodes_in_direction('right')],
                key = lambda h: h.count)

        self._cover(column_header)

        for col_node in column_header.nodes_in_direction('down'):
            self._partial_answer[k] = col_node.row_header.value

            for node in col_node.nodes_in_direction('right'):
                self._cover(node.column_header)

            if self._search(k + 1):
                return True

            for node in col_node.nodes_in_direction('left'):
                self._uncover(node.column_header)
             

        self._uncover(column_header)

        return False


if __name__ == '__main__':

    matrix = {1: [2, 4, 5],
              2: [0, 3, 6],
              3: [1, 2, 5],
              4: [0, 3],
              5: [1, 6],
              6: [3, 4, 6]}
    solver = DLXSolver()
    print solver.solve(matrix, 7)
