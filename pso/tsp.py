#!/usr/bin/env python

from __future__ import division

try:
    import psyco
    psyco.full()
except ImportError:
    pass


import os
import random
import threading

import pygame
from pygame.locals import *

from vec2d import Vec2d


class Velocity(object):

    MAX_VELOCITY = 3

    def __init__(self, num_nodes, *args):

        self.num_nodes = num_nodes

        if len(args) == 0:
            # construct a random swap sequence
            swap_sequence = [(random.randint(0, num_nodes - 1),
                              random.randint(0, num_nodes - 1))
                              for i in xrange(random.randint(
                                  0, self.MAX_VELOCITY))]
            # convert the swap sequence into a basic swap sequence
            self.swap_sequence = self.to_basic(num_nodes, 
                                               swap_sequence)

        elif len(args) == 1:
            if isinstance(args[0], Velocity):
                # copy from another instance of Velocity
                self.swap_sequence = args[0].swap_sequence[:]
            else:
                # copy from the given list of swap sequence
                self.swap_sequence = args[0][:]


    @staticmethod
    def to_velocity(num_nodes, travel_from, travel_to):
        """Return the basic swap sequence for converting from 
        one travelling sequence to another
        """
        a = travel_to[:]
        b = travel_from[:]
        bss = []
        for i in xrange(num_nodes):
            if a[i] != b[i]:
                j = b.index(a[i])
                bss.append((i, j))
                b[i], b[j] = b[j], b[i]

        # make sure that the length of the swap sequence does not
        # exceed the MAX_VELOCITY
        length = len(bss)
        while length > Velocity.MAX_VELOCITY:
            # randomly deletes an element in the swap sequence
            del bss[random.randint(0, Velocity.MAX_VELOCITY - 1)]
            length -= 1

        return Velocity(num_nodes, bss)



    @staticmethod
    def to_basic(num_nodes, swap_sequence):
        """Return the Basic Swap Sequence for a given swap sequence
        """
        
        # calculate the basic swap sequence from b to a
        a = range(num_nodes)
        b = a[:]
        bss = []
        for i, j in swap_sequence:
            a[i], a[j] = a[j], a[i]
        for i in xrange(num_nodes):
            if a[i] != b[i]:
                j = b.index(a[i])
                bss.append((i, j))
                b[i], b[j] = b[j], b[i]
        return bss


    def __add__(self, other):

        swap_sequence = self.swap_sequence[:]
        swap_sequence.extend(other.swap_sequence)
        bss = self.to_basic(self.num_nodes, swap_sequence)
         
        # make sure that the length of the swap sequence does not
        # exceed the MAX_VELOCITY
        length = len(bss)
        while length > self.MAX_VELOCITY:
            # randomly deletes an element in the swap sequence
            del bss[random.randint(0, self.MAX_VELOCITY - 1)]
            length -= 1
             
        return Velocity(self.num_nodes, bss)


    def __mul__(self, fraction):

        return Velocity(self.num_nodes, 
                        [x for x in self.swap_sequence 
                         if random.randint(0, 10000) / 10000 < fraction])


    __rmul__ = __mul__ 

    def __iter__(self):
        return iter(self.swap_sequence)

        
    def __str__(self):
        
        return str(self.swap_sequence)


class Particle(object):

    def __init__(self, matrix):
        
        self.matrix = matrix
        self.num_nodes = len(matrix)
        
        # generate a random travelling sequence
        self.travel = range(self.num_nodes)
        random.shuffle(self.travel)

        # generate a random velocity(Swap Sequence) of length MAX_VELOCITY
        self.velocity = Velocity(self.num_nodes)

        # set default best known travelling sequence 
        self.best_travel = self.travel[:]

        self.update_distance()
        self.best_distance = self.distance
        self.update_best_distance()


    def set_global_best_travel(self, travel):
        self.global_best_travel = travel

    
    def step(self):
        """Step the iteration

        In each iteration, this method should be called after
        setting the global_best_travel
        """
        travel = self.travel

        rand = random.randint(0, 10000) / 10000

        rand_1 = random.randint(0, 10000) / 10000
        rand_2 = random.randint(0, 10000) / 10000
        
        if rand > 0.85:
            # 15 % mutation
            rand_x = random.randint(0, self.num_nodes - 1)
            rand_y = random.randint(0, self.num_nodes - 1)
            self.velocity = self.velocity + \
                        rand_1 * Velocity.to_velocity(self.num_nodes,
                             self.travel, self.best_travel) + \
                        rand_2 * Velocity.to_velocity(self.num_nodes,
                             self.travel, self.global_best_travel) + \
                        Velocity(self.num_nodes,[(rand_x, rand_y)])
        elif rand > 0.3:
            # 45 % individual
            self.velocity = self.velocity + \
                        rand_1 * Velocity.to_velocity(self.num_nodes,
                             self.travel, self.best_travel)
        else:
            # 40% social + individual
            self.velocity = self.velocity + \
                        rand_2 * Velocity.to_velocity(self.num_nodes,
                             self.travel, self.global_best_travel) + \
                        rand_1 * Velocity.to_velocity(self.num_nodes,
                             self.travel, self.best_travel) 
       
        for i, j in self.velocity:
            travel[i], travel[j] = travel[j], travel[i]

        self.update_distance()
        self.update_best_distance()


    def update_distance(self):

        matrix = self.matrix
        travel = self.travel

        self.distance = 0
        for i in xrange(self.num_nodes - 1):
            self.distance += matrix[travel[i]][travel[i + 1]]
        self.distance += matrix[travel[self.num_nodes - 1]][travel[0]]


    def update_best_distance(self):

        if self.distance < self.best_distance:
            self.best_distance = self.distance
            self.best_travel = self.travel[:]

    

class PSO(threading.Thread):

    def __init__(self, num_particles, nodes):
        threading.Thread.__init__(self)
        
        self.num_particles = num_particles
        self.nodes = nodes
        self.matrix = [[0 for x in nodes] for y in nodes]
        for i in xrange(len(nodes)):
            for j in xrange(len(nodes)):
                self.matrix[i][j] = nodes[i].get_distance(nodes[j])
        self.particles = [Particle(self.matrix) for i in xrange(num_particles)]
        self.global_best_travel = []
        self.global_best_distance = None

        self.running = True
    

    def run(self):

        self.iteration = 0

        while self.running:

            #best_particle = min(self.particles, key = lambda p: p.best_distance)
            particles = self.particles
            best_particle = particles[0]
            worst_particle = particles[0]
            best_best_particle = particles[0]
            total_distance = 0


            for particle in self.particles:
                #if self.opt2(particle.travel):
                #    particle.update_distance()
                #    particle.update_best_distance()
                if particle.distance < best_particle.distance:
                    best_particle = particle
                if particle.distance > worst_particle.distance:
                    worst_particle = particle
                if particle.best_distance < best_best_particle.best_distance:
                    best_best_particle = particle
                total_distance += particle.distance
            
            self.average_value = total_distance / self.num_particles
            self.best_value = best_particle.distance
            self.worst_value = worst_particle.distance

            self.global_best_travel = best_best_particle.best_travel


            if best_best_particle.best_distance != self.global_best_distance:
                self.global_best_distance = best_particle.best_distance

            for particle in self.particles:
                particle.set_global_best_travel(self.global_best_travel)
                particle.step()

            self.iteration += 1


    def stop(self):

        self.running = False


    def opt2(self, travel):

        length = len(travel)
        dist = self.matrix

        for i in xrange(length - 3):
            for j in xrange(i + 2, length - 1):
                a = travel[i]
                b = travel[i + 1]
                c = travel[j]
                d = travel[j + 1]
                if dist[a][b] + dist[c][d] > dist[a][c] + dist[d][b]:
                    travel[a], travel[c] = travel[c], travel[a]
                    return True
        return False



class Visual():

    RUNNING = 1
    STOPPED = 0

    def __init__(self):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((640, 500))
        pygame.display.set_caption('TSP PSO')
        self.clock = pygame.time.Clock()
        self.coords = []
        self.status = self.STOPPED
        self.lines = []
        self.font = pygame.font.Font(None, 20)
        self.iteration = 0

    def run(self):

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    if hasattr(self, 'pso'):
                        self.pso.stop()
                    pygame.quit()
                    raise SystemExit
                elif event.type == MOUSEBUTTONDOWN:
                    self.coords.append(event.pos)
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if self.status == self.STOPPED:
                            self.status = self.RUNNING
                            nodes = [Vec2d(c) for c in self.coords]
                            self.pso = PSO(50, nodes)
                            self.pso.setDaemon(True)
                            self.pso.start()
                        else:
                            self.pso.stop()
                            self.status = self.STOPPED
                    elif event.key == K_r:
                        self.iteration = 0
                        self.pso.stop()
                        self.status = self.STOPPED
                        self.coords = []
                        self.lines = []

            self.screen.fill(Color('white')) 

            for coord in self.coords:
                pygame.draw.circle(self.screen, Color('blue'), 
                        coord, 3)

            if self.status == self.RUNNING:
                if hasattr(self.pso, 'average_value'):

                    self.iteration = self.pso.iteration
                    order = self.pso.global_best_travel
                    self.lines = [self.coords[i] for i in order]
                    first_order = self.pso.particles[0].travel[:]
                    first_lines = [self.coords[i] for i in first_order]
                    pygame.draw.lines(self.screen, Color('gray90'), True, 
                                      first_lines, 1)

            if self.lines:
                pygame.draw.lines(self.screen, Color('grey'), True, 
                                  self.lines, 2)

            text = self.font.render('iterations: %d' % self.iteration,
                                    True, Color('black'))
            self.screen.blit(text, (20, 20))

            pygame.display.update()
            self.clock.tick(30)

    
if __name__ == '__main__':

    vis = Visual()
    vis.run()
