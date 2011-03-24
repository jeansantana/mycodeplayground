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

import math
import random

import pygame
from pygame.locals import *

from vec2d import Vec2d


MAX_VELOCITY = 100
MIN_VELOCITY = 0

MAX_INIT_POS_OFFSET = 50
MIN_INIT_POS_OFFSET = -50

INERTIA_WEIGHT = 1

ACCELERATION_CONSTANT_1 = 2
ACCELERATION_CONSTANT_2 = 2

REBELLION_FACTOR = 0.90


class Particle(object):

    def __init__(self, position, target_position):

        # initialize postion
        x = random.randint(MIN_INIT_POS_OFFSET, MAX_INIT_POS_OFFSET)
        y = random.randint(MIN_INIT_POS_OFFSET, MAX_INIT_POS_OFFSET)
        self.position = Vec2d(position[0] + x, position[1] + y)
        
        # initialize velocity
        vx = random.randint(MIN_VELOCITY, MAX_VELOCITY)
        vy = random.randint(MIN_VELOCITY, MAX_VELOCITY)
        self.velocity = Vec2d(vx, vy)
        
        # initialize best known position
        self.best_position = Vec2d(self.position)
        
        # update distance
        self.target_position = Vec2d(target_position)
        self.distance = self.position.get_distance(self.target_position)
        self.best_distance = self.distance
        
        
    def step(self, time_span):

        rand_1 = random.randint(0, 1000) / 1000
        rand_2 = random.randint(0, 1000) / 1000

        # there're possibilities that the particle will not
        # follow the leader
        if rand_1 < REBELLION_FACTOR:
            self.velocity = INERTIA_WEIGHT * self.velocity + \
                            ACCELERATION_CONSTANT_1 * rand_1 * \
                                (self.best_position - self.position)
        else:
            self.velocity = INERTIA_WEIGHT * self.velocity + \
                            ACCELERATION_CONSTANT_1 * rand_1 * \
                                (self.best_position - self.position) + \
                            ACCELERATION_CONSTANT_2 * rand_2 * \
                                (self.global_best_position - self.position)
        
        # guarantees that the speed will not exceed maximum
        if self.velocity.length > MAX_VELOCITY:
            self.velocity.length = MAX_VELOCITY

        # update position
        self.position += self.velocity * time_span
        
        # update best known position
        self.distance = self.position.get_distance(self.target_position)
        if self.distance < self.best_distance:
            self.best_position = Vec2d(self.position)
            self.best_distance = self.distance
            
        # the swarm must get the particles' best distance now
        # and set the global best position
        

    def set_target_position(self, position):

        self.target_position = position

        self.distance = self.position.get_distance(self.target_position)
        self.best_distance = self.distance
        self.best_position = Vec2d(self.position)


    def set_global_best_position(self, global_best_position):

        self.global_best_position = global_best_position


class Swarm(object):

    def __init__(self, num_particles, source_position, target_position):

        self.particles = [Particle(source_position, target_position)
                for i in xrange(num_particles)]


    def step(self, time_span):

        # get global best position
        best_particle = min(self.particles, key = lambda p: p.best_distance)
        global_best_position = best_particle.best_position

        # update particles 
        for particle in self.particles:
            particle.set_global_best_position(global_best_position)
            particle.step(time_span)


    def set_target_position(self, position):

        for particle in self.particles:
            particle.set_target_position(position)


    def draw(self, screen):

        for particle in self.particles:
            pygame.draw.circle(screen, Color('red'), 
                    map(int, particle.position), 2)


class PSO(object):

    def __init__(self, num_particles, source_position, target_position):

        self.swarm = Swarm(num_particles, source_position, target_position)
        
        # GUI stuff
        self.screen = pygame.display.set_mode((640, 640))
        pygame.display.set_caption(
                'Flock Simulation Using Particle Swarm Optimization')
        self.clock = pygame.time.Clock()


    def run(self):

        while True:

            # events handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == MOUSEMOTION:
                    self.swarm.set_target_position(event.pos)
            
            # draw
            self.screen.fill(Color('white'))
            self.swarm.draw(self.screen)

            pygame.display.update()
            
            # step
            self.swarm.step(1 / 30)
            self.clock.tick(30)


if __name__ == '__main__':

    demo = PSO(100, (50, 50), (600, 600))
    demo.run()
