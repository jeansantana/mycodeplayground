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


# The classifications of sorting algorithms are based on 
# http://en.wikipedia.org/wiki/Sorting_algorithm 

from __future__ import division
import random
import collections


SWAP  = 0
SHIFT = 1
LOAD  = 2
STORE = 3


# ==========================
# Exchange sorts
# ==========================


def bubble_sort(array):

    indexes = range(len(array) - 1)
    swapped = True

    while swapped:
        swapped = False
        for i in indexes:
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                yield (SWAP, (i, i + 1))


def cocktail_sort(array):

    # a variant of bubble sort which sorts bi-directionally

    indexes = range(len(array) - 1)
    neg_indexes = indexes[::-1]
    swapped = True

    while swapped:
        swapped = False
        for i in indexes:
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                yield (SWAP, (i, i + 1))
        if not swapped:
            break

        for i in neg_indexes:
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                yield (SWAP, (i, i + 1))


def odd_even_sort(array):

    # a variant of bubble sort wich compares all (odd, even)-indexed
    # paris of adjacent elements

    odd_indexes = xrange(1, len(array) - 1, 2)
    even_indexes = xrange(0, len(array) - 1, 2)
    swapped = True

    while swapped:
        swapped = False
        for i in odd_indexes:
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                yield (SWAP, (i, i + 1))
        for i in even_indexes:
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                yield (SWAP, (i, i + 1))


def comb_sort(array):

    SHRINK_FACTOR = 1.247330950103979
    gap = length = len(array)
    swapped = True

    while gap > 1 or swapped:
        if gap > 1:
            gap = int(gap / SHRINK_FACTOR)
        swapped = False
        i = 0
        while gap + i < length:
            if array[i] > array[i + gap]:
                array[i], array[i + gap] = array[i + gap], array[i]
                swapped = True
                yield (SWAP, (i, i + gap))
            i += 1
        

def gnome_sort(array):

    length = len(array)
    i = 1
    while i < length:
        if array[i] > array[i - 1]:
            i += 1
        else:
            array[i], array[i - 1] = array[i - 1], array[i]
            yield (SWAP, (i, i - 1))
            i += -1 if i > 1 else 1


def _quick_sort(array, begin, end, record):

    if begin < end:
        pivot_index = random.randint(begin, end)
        
        array[begin], array[pivot_index] = array[pivot_index], array[begin]
        record.append((SWAP, (begin, pivot_index)))

        pivot = array[begin]
        pivot_index = begin
        record.append((LOAD, (begin)))

        for i in xrange(begin + 1, end + 1):
            if array[i] <= pivot:
                pivot_index += 1
                array[pivot_index], array[i] = array[i], array[pivot_index]
                record.append((SWAP, (pivot_index, i)))

        array[begin] = array[pivot_index]
        record.append((SHIFT, (pivot_index, begin)))

        array[pivot_index] = pivot
        record.append((STORE, (pivot_index)))

        _quick_sort(array, pivot_index + 1, end, record)

        while pivot_index > begin and \
                array[pivot_index] == array[pivot_index - 1]:
            pivot_index -= 1

        _quick_sort(array, begin, pivot_index - 1, record)


def quick_sort(array):

    record = collections.deque()
    _quick_sort(array, 0, len(array) - 1, record)
    for r in record:
        yield r


# ==========================
# Selection sorts
# ==========================


def selection_sort(array):

    length = len(array)
    index = 0

    while index < length:
        min_ele_index = min(xrange(index, length), key = array.__getitem__)
        array[index], array[min_ele_index] = array[min_ele_index], array[index]
        yield (SWAP, (index, min_ele_index))
        index += 1


def heap_sort(array):

    n = length = len(array)
    i = n // 2
    t = None

    while True:
        if i > 0:
            i -= 1
            t = array[i]
            yield (LOAD, i)
        else:
            n -= 1
            if n == 0:
                break 
            t = array[n]
            yield (LOAD, n)
            array[n] = array[0]
            yield (SHIFT, (0 , n))

        parent = i
        child = i * 2 + 1

        while child < n:
            if child + 1 < n and array[child + 1] > array[child]:
                child += 1
            if array[child] > t:
                array[parent] = array[child]
                yield (SHIFT, (child, parent))
                parent = child
                child = parent * 2 + 1
            else:
                break
        array[parent] = t
        yield (STORE, parent)


def cycle_sort(array):

    # Code is based on 
    # http://en.wikipedia.org/wiki/Cycle_sort
    
    length = len(array)

    for cycle_start in xrange(0, length - 1):
        item = array[cycle_start]

        pos = cycle_start
        for i in xrange(cycle_start + 1, length):
            if array[i] < item:
                pos += 1

        if pos == cycle_start:
            continue
        
        while item == array[pos]:
            pos += 1
        array[pos], item = item, array[pos]
        yield (SWAP, (pos, cycle_start))
        yield (LOAD, cycle_start)

        while pos != cycle_start:
            pos = cycle_start
            for i in xrange(cycle_start + 1, length):
                if array[i] < item:
                    pos += 1

            while item == array[pos]:
                pos += 1
            array[pos], item = item, array[pos]
            yield (SHIFT, (pos, cycle_start))
            yield (STORE, pos)
            yield (LOAD, cycle_start)
        yield (STORE, cycle_start)


# ==========================
# Insertion sorts
# ==========================


def insertion_sort(array):

    for i in xrange(1, len(array)):
        key = array[i]
        j = i - 1
        yield (LOAD, i)
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            yield (SHIFT, (j, j + 1))
            j -= 1
        array[j + 1] = key
        yield (STORE, j + 1)


def shell_sort(array):

    length = len(array)
    inc = length // 2
    while inc:
        for i in xrange(length):
            j = i
            tmp = array[i]
            yield (LOAD, i)
            while j >= inc and array[j - inc] > tmp:
                array[j] = array[j - inc]
                yield (SHIFT, (j - inc, j))
                j -= inc
            array[j] = tmp
            yield (STORE, j) 
        inc = inc // 2 if inc // 2 else (0 if inc == 1 else 1)
