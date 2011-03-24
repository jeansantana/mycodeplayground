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


# window settings
CAPTION = 'Sudoku Solver'
RESOLUTION = (600, 650)
FRAMERATE = 30

# board layout
BOARD_Y  = 100
BOARD_SIZE = 500

# help text
HELP_TEXT = \
"""hover mouse over a cell to select it
press 1-9 to fill the selected cell or 0 to unfill the selected cell
press <space> to solve the puzzle or <r> to reset
"""

HELP_TEXT_POS = (50, 30)
HELP_TEXT_Y_INCREMENT = 20

# colors
BACKGROUND_COLOR  = 'white'
THIN_LINE_COLOR   = 'gray50'
THICK_LINE_COLOR  = 'gray40'
FILLED_COLOR      = 'gray93'
MOUSE_OVER_COLOR  = 'lightcyan2'
GRID_TEXT_COLOR   = 'black'
GRID_ANSWER_COLOR = 'green3'
HELP_TEXT_COLOR   = 'grey30'

# fonts
FONT_NAME = 'freesansbold.ttf'
GRID_FONT_SIZE = 40
HELP_FONT_SIZE = 16
