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

import os
import cStringIO

import pygame
from pygame.locals import *

from sudoku import SudokuSolver
from config import *

__all__ = ['SudokuSolverGUI']


# the status the grid may have
S_BLANK     = 0
S_FILLED    = 1
S_MOUSEOVER = 2
S_ANSWER    = 4


class Grid(Rect):

    def __init__(self, *arg, **args):
        Rect.__init__(self, *arg, **args)
        
        self.number = None
        self.status = S_BLANK


class SudokuSolverGUI(object):

    def __init__(self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        
        pygame.display.set_caption(CAPTION)
        self._screen = pygame.display.set_mode(RESOLUTION)
        self._clock = pygame.time.Clock()
        self._grid_font = pygame.font.Font(FONT_NAME, GRID_FONT_SIZE)
        self._help_font = pygame.font.Font(FONT_NAME, HELP_FONT_SIZE)

        # board settings 
        self._board_pos = (RESOLUTION[0] - BOARD_SIZE) // 2, BOARD_Y
        self._grid_size = BOARD_SIZE // 9 

        # calculate grid lines' coordinates
        grid_xs = [x * self._grid_size + self._board_pos[0] 
                for x in xrange(10)]
        grid_ys = [y * self._grid_size + self._board_pos[1]
                for y in xrange(10)]

        vertical_lines_top = [(x, self._board_pos[1])
                for x in grid_xs]
        vertical_lines_bottom = [(x, self._board_pos[1] + BOARD_SIZE - 4)
                for x in grid_xs]
        horizontal_lines_top = [(self._board_pos[0], y)
                for y in grid_ys]
        horizontal_lines_bottom = [(self._board_pos[0] + BOARD_SIZE - 4, y)
                for y in grid_ys]

        self._vertical_lines = zip(vertical_lines_top, 
                vertical_lines_bottom)
        self._horizontal_lines = zip(horizontal_lines_top, 
                horizontal_lines_bottom)

        # set grids
        self._grids = [Grid(grid_xs[j], grid_ys[i], 
                       self._grid_size, self._grid_size)
                           for j in xrange(9) for i in xrange(9)]
        self._reset_grids()

        # selection
        self._selected_grid = None

        # solver
        self._solver = SudokuSolver()

        
    def run(self):

        while True:
            # events handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == MOUSEMOTION:
                    self._handle_mouse(event)
                elif event.type == KEYDOWN:
                    self._handle_keyboard(event)
                    
            
            # draw stuffs
            self._draw_background()
            self._draw_grids()
            self._draw_grid_lines()
            self._draw_help_text()
            
            # step
            pygame.display.update()
            self._clock.tick(FRAMERATE)


    def _handle_mouse(self, event):

        # set mose over status
        if event.type == MOUSEMOTION:
            for grid in self._grids:
                grid.status &= ~S_MOUSEOVER
                if grid.collidepoint(event.pos):
                    grid.status |= S_MOUSEOVER
                    self._selected_grid = grid


    def _handle_keyboard(self, event):

        key_name = pygame.key.name(event.key)

        if key_name in map(str, xrange(1, 10)):
            # fill grid
            self._selected_grid.number = key_name
            self._selected_grid.status |= S_FILLED
            self._selected_grid.status &= ~S_ANSWER
        elif key_name == '0':
            # clear grid
            self._selected_grid.status &= ~(S_FILLED | S_ANSWER)
            self._selected_grid.number = None
        elif event.key == K_ESCAPE:
            # quit
            pygame.quit()
            raise SystemExit
        elif event.key == K_r:
            # reset
            self._reset_grids()
        elif event.key == K_SPACE:
            # solve
            self._solve()


    def _reset_grids(self):

        for grid in self._grids:
            grid.status = S_BLANK
            grid.number = None



    def _draw_background(self):

        self._screen.fill(Color(BACKGROUND_COLOR))
        

    def _draw_grids(self):

        for grid in self._grids:
            if grid.status & S_FILLED:
                pygame.draw.rect(self._screen, Color(FILLED_COLOR), grid)
            if grid.status & S_MOUSEOVER:
                pygame.draw.rect(self._screen, Color(MOUSE_OVER_COLOR), grid)
            if grid.number:
                color = GRID_ANSWER_COLOR if grid.status & S_ANSWER else \
                        GRID_TEXT_COLOR
                    
                text = self._grid_font.render(grid.number, 
                            True, Color(color))

                x = grid.center[0] - text.get_width() // 2
                y = grid.center[1] - text.get_height() // 2

                self._screen.blit(text, (x, y))


    def _draw_grid_lines(self):

        # draw thin lines
        for i, (start_pos, end_pos) in enumerate(self._vertical_lines):
            if i % 3 != 0:
                pygame.draw.line(self._screen, 
                                 Color(THIN_LINE_COLOR),
                                 start_pos,
                                 end_pos,
                                 1)
        for i, (start_pos, end_pos) in enumerate(self._horizontal_lines):
            if i % 3 != 0:
                pygame.draw.line(self._screen, 
                                 Color(THIN_LINE_COLOR), 
                                 start_pos,
                                 end_pos,
                                 1)
        # draw thick lines
        for i, (start_pos, end_pos) in enumerate(self._vertical_lines):
            if i % 3 == 0:
                pygame.draw.line(self._screen, 
                                 Color(THICK_LINE_COLOR), 
                                 start_pos,
                                 end_pos,
                                 2)

        for i, (start_pos, end_pos) in enumerate(self._horizontal_lines):
            if i % 3 == 0:
                pygame.draw.line(self._screen, 
                                 Color(THICK_LINE_COLOR), 
                                 start_pos,
                                 end_pos,
                                 2)


    def _draw_help_text(self):

        x, y = HELP_TEXT_POS

        for line in HELP_TEXT.split('\n'):
            text = self._help_font.render(line, True, Color(HELP_TEXT_COLOR))
            self._screen.blit(text, (x, y))
            y += HELP_TEXT_Y_INCREMENT


    def _solve(self):

        s = cStringIO.StringIO()
        for grid in self._grids:
            if not grid.status & S_FILLED:
                grid.status &= ~S_ANSWER
                grid.number = None
                s.write('.')
            else:
                s.write(grid.number)
        puzzle = s.getvalue()
        matrix = self._solver.solve(puzzle)
        
        for row, col, val in matrix:
            grid = self._grids[row * 9 + col]
            if not grid.number:
                grid.number = str(val)
                grid.status |= S_ANSWER
            


if __name__ == '__main__':
    app = SudokuSolverGUI()
    app.run()
