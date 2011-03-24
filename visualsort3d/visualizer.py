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

import time
import random
import thread
import functools
import collections

from visual.controls import *

from sortalgos import *

FRAMERATE = 30

BOX_START_X = 0
BOX_START_Y = -50
BOX_START_Z = 0
BOX_INTERVAL = 10
BOX_LENGTH = 5
BOX_HEIGHT_UNIT = 5
BOX_HEIGHT_MIN = 30
BOX_WIDTH = 5
BOX_MATERIAL = materials.plastic
BOX_OPACITY = 0.6

FLOOR_HEIGHT = 2
FLOOR_LENGTH = 300
FLOOR_WIDTH = 100
FLOOR_MATERIAL = materials.wood

MOVEOUT_A = 15
MOVEOUT_B = -15

MOVE_SPEED = 5

WINDOW_SIZE = (720, 504)
CONTROL_SIZE = (240, 504)

WINDOW_POS = (200, 200)
CONTROL_POS = (190 + 720, 200)



class Visualizer(object):
    
    def __init__(self, window_size, window_pos, problem_size):
        
        # configure scene
        global scene
        scene.x, scene.y = window_pos
        scene.width, scene.height = window_size
        scene.title = 'Sorting Algorithms Visualization'
        
        # number of boxes
        self.size = problem_size
        
        # generate random heights
        self.heights = range(self.size)
        random.shuffle(self.heights)
        
        # create a list of boxes according to heights
        self.box_list = [box(pos = (BOX_START_X + BOX_INTERVAL * \
                                        (i - self.size // 2), 
                                    BOX_START_Y + \
                                        (BOX_HEIGHT_MIN + \
                                        BOX_HEIGHT_UNIT * self.heights[i]) // 2,
                                    BOX_START_Z),
                             length = BOX_LENGTH,
                             height = BOX_HEIGHT_MIN + \
                                      BOX_HEIGHT_UNIT * self.heights[i],
                             width = BOX_WIDTH,
                             color = (1 - self.heights[i] / self.size, 
                                      0.9,
                                      self.heights[i] / self.size),
                             opacity = BOX_OPACITY,
                             material = BOX_MATERIAL)
                         for i in xrange(self.size)]

        # create floor
        self.floor = box(pos = (0,
                                BOX_START_Y - FLOOR_HEIGHT / 2,
                                0),
                         length = FLOOR_LENGTH,
                         height = FLOOR_HEIGHT,
                         width = FLOOR_WIDTH,
                         material = FLOOR_MATERIAL)

        # temp box, will be used by LOAD and STORE
        self.stored_box = None
        
        # map from operation name to their handlers
        self.operation_dict = {SWAP: self.swap_handler,
                               LOAD: self.load_handler,
                               STORE: self.store_handler,
                               SHIFT: self.shift_handler}


    def shuffle(self):
        """Shuffle the boxes.
        """

        for i in xrange(self.size):
            j = random.randint(i, self.size - 1)
            self.heights[i], self.heights[j] = self.heights[j], self.heights[i]
            self.box_list[i].height, self.box_list[j].height = \
                self.box_list[j].height, self.box_list[i].height
            self.box_list[i].pos[1], self.box_list[j].pos[1] = \
                self.box_list[j].pos[1], self.box_list[i].pos[1]
            self.box_list[i].color, self.box_list[j].color = \
                self.box_list[j].color, self.box_list[i].color


    def operate(self, operation, operand):
        """Distribute commands to the handlers.
        """

        self.operation_dict[operation](operand)


    def swap_handler(self, (a, b)):
        """Swap the position of the two boxes a and b.
        """

        if a == b:
            return

        # make sure a < b
        if a > b:
            a, b = b, a

        box_a = self.box_list[a]
        box_b = self.box_list[b]

        pos_a = vector(box_a.pos)
        pos_b = vector(box_b.pos)

        dir_a = 1 if (pos_b - pos_a)[0] > 0 else -1
        dir_b = -dir_a

        # take a and b out of the sequence
        while box_a.pos[2] <= MOVEOUT_A:
            box_a.pos[2] += MOVE_SPEED
            box_b.pos[2] += MOVE_SPEED / MOVEOUT_A * MOVEOUT_B
            time.sleep(1 / FRAMERATE)

        # swap the x coord of a and b
        while box_a.pos[0] <= pos_b[0]:
            box_a.pos[0] += dir_a * MOVE_SPEED
            box_b.pos[0] += dir_b * MOVE_SPEED
            time.sleep(1 / FRAMERATE)

        # put a and b back to the sequence
        while box_a.pos[2] >= 0:
            box_a.pos[2] -= MOVE_SPEED
            box_b.pos[2] -= MOVE_SPEED / MOVEOUT_A * MOVEOUT_B
            time.sleep(1 / FRAMERATE)

        # avoid accumulating floating point error
        box_a.pos[0] = pos_b[0]
        box_a.pos[2] = pos_b[2]
        box_b.pos[0] = pos_a[0]
        box_b.pos[2] = pos_a[2]

        self.box_list[a], self.box_list[b] = self.box_list[b], self.box_list[a]


    def load_handler(self, x):
        """Take the box positioned at x from the sequence.
        """

        self.stored_box = self.box_list[x]

        while self.stored_box.pos[2] <= MOVEOUT_A:
            self.stored_box.pos[2] += MOVE_SPEED
            time.sleep(1 / FRAMERATE)

    
    def store_handler(self, x):
        """Store a previous loaded box to the position x.
        """

        dest_x = BOX_START_X + BOX_INTERVAL * (x - self.size // 2)

        dir = 1 if (dest_x - self.stored_box.pos[0]) > 0 else -1 

        while cmp(dest_x, self.stored_box.pos[0]) == dir:
            self.stored_box.pos[0] += dir * MOVE_SPEED
            time.sleep(1 / FRAMERATE)

        while self.stored_box.pos[2] >= 0:
            self.stored_box.pos[2] -= MOVE_SPEED
            time.sleep(1 / FRAMERATE)

        # avoid accumulating floating point error
        self.stored_box.pos[2] = 0

        self.box_list[x] = self.stored_box


    def shift_handler(self, (a, b)):
        """Shift a box from position a to b.
        If a and b are adjacent, a will be moved to b directly.
        Otherwise, take a out of the sequence and then put it to b.
        """

        box = self.box_list[a]
        dest_x = BOX_START_X + BOX_INTERVAL * (b - self.size // 2)
        dir = 1 if (dest_x - box.pos[0]) > 0 else -1 

        if abs(a - b) == 1:
            # if a and b are adjacent
            while cmp(dest_x, box.pos[0]) == dir:
                box.pos[0] += dir * MOVE_SPEED
                time.sleep(1 / FRAMERATE)
            box.pos[0] = dest_x


        else:
            # take a out of the sequence
            while box.pos[2] >= MOVEOUT_B:
                box.pos[2] -= MOVE_SPEED
                time.sleep(1 / FRAMERATE)

            # swap the x coord of a and b
            while cmp(dest_x, box.pos[0]) == dir:
                box.pos[0] += dir * MOVE_SPEED
                time.sleep(1 / FRAMERATE)

            # put a and b back to the sequence
            while box.pos[2] <= 0:
                box.pos[2] += MOVE_SPEED
                time.sleep(1 / FRAMERATE)

        box.pos[2] = 0
        self.box_list[b] = box



class Controller(object):

    def __init__(self, window_size, window_pos, visualizer):

        # reference to the visualizer
        self.visualizer = visualizer
        
        # create control window
        self.control = controls(x = window_pos[0],
                                y = window_pos[1],
                                width = window_size[0],
                                height = window_size[1],
                                title = 'Control Panel')
        
        # map from the names to functions
        algo_dict = {'Bubble': bubble_sort,
                     'Cocktail': cocktail_sort,
                     'Odd-even': odd_even_sort,
                     'Comb': comb_sort,
                     'Gnome': gnome_sort,
                     'Quick': quick_sort,
                     'Selection': selection_sort,
                     'Heap': heap_sort,
                     'Cycle': cycle_sort,
                     'Insertion': insertion_sort,
                     'Shell': shell_sort}

        # order the dict by key
        self.algo_dict = collections.OrderedDict(
                sorted(algo_dict.items(), key = lambda t: t[0]))
        
        # create a button for shuffling the boxes
        self.shuffle_button = button(pos = (0, 80),
                                     width = 70,
                                     height = 24,
                                     text = "Shuffle",
                                     action = self.shuffle_handler)
        
        # create buttons for executing the algorithms
        self.button_list = []
        x, y = 0, 60 # start position (centered)
        for k in self.algo_dict:
            func = functools.partial(self.algo_handler, k)    
            new_button = button(pos = (x, y),
                                width = 70,
                                height = 25,
                                text = k,
                                action = func)
            self.button_list.append(new_button)
            y -= 14 # line offset


    def shuffle_handler(self):

        self.visualizer.shuffle()
        

    def algo_handler(self, algo_name):

        for operation, operand in self.algo_dict[algo_name](
                self.visualizer.heights):
            self.visualizer.operate(operation, operand)


    def run(self):

        while True:
            self.control.interact()
            rate(FRAMERATE)


def main():

    vis = Visualizer(WINDOW_SIZE, WINDOW_POS, 20)
    con = Controller(CONTROL_SIZE, CONTROL_POS, vis)
    con.run()



main()
