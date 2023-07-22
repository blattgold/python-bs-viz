import pygame
import math
import random
import numpy as np

SCREEN_W = 1280
SCREEN_H = 720

class Bs:
    def __init__(self, ns=[]):
        self.current_search_index = 0 # unsigned integer
        self.unsorted_index = None
        self.to_sort = ns
        self.swapped = False
        self.runs = 0
        self.shown_off = False

    def step(self):
        '''
        runs a single step in the bubble sort algorithm
        '''
        if not self.is_sorted(self.to_sort):
            if self.current_search_index == len(self.to_sort)+ (-1 -self.runs):
                self.current_search_index = 0
                self.runs += 1

            if self.unsorted_index is None:
                self.swapped = False
                self.unsorted_index = self.search_step()
            else:
                self.swapped = True
                self.sort_step(self.to_sort, 
                               self.unsorted_index)
        else:
            if self.swapped:
                self.swapped = False
            self.show_off()

    def is_sorted(self, ns):
        '''
        takes: list to check
        returns: True if sorted, False otherwise
        0 element list counts as sorted
        lists are sorted lowest to greatest
        '''
        n_prev = -1
        for n in ns:
            if n_prev > n:
                return False
            else:
                n_prev = n
                continue

        return True

    def search_step(self):
        '''
        returns: None: if no unsorted element found in current step,
                 uInt: if it found an unsorted element, the index of it.
        '''
        if self.current_search_index < len(self.to_sort) + (-1 -self.runs):
            self.current_search_index += 1
        else:
            return None

        if self.to_sort[self.current_search_index] < self.to_sort[self.current_search_index -1]:
            return self.current_search_index

    def sort_step(self, ns, i):
        '''
        takes: ns: list to be sorted
               i:  index of the unsorted element
        moves number at given index to the start of the given list
        returns: the modified list
        '''
        ns.insert(i-1, ns.pop(i))
        self.unsorted_index = None
        return ns

    def show_off(self):
        '''
        iterates through the rest of the list one last time, 
        to 'show off' for the visualisation
        '''
        if self.current_search_index != len(self.to_sort) -1:
            self.current_search_index += 1
        else:
            self.shown_off = True

class Viz:
    def __init__(self, ns=100):
        self.bs = Bs([random.random() for x in range(ns)])

    def run(self):
        if not self.bs.shown_off:
            self.bs.step()
            self.synth(self.bs.to_sort[self.bs.current_search_index])

    def draw(self, screen):
        '''
        draws the sort list as rectangles
        element height: list_element * SCREEN_H
        element width: SCREEN_W / list_length  
        '''
        for x in range(len(self.bs.to_sort)):
            color = (0,0,0) # base color of all elements
            if self.bs.shown_off:
                color = (100,100,200) # replacement color for all elements after shown off (search completed)
            elif x == self.bs.current_search_index:
                color = (200,0,0) # color for current step item in search
            elif x+1 == self.bs.current_search_index and self.bs.swapped:
                color = (50,50,100) # color for swapped item

            pygame.draw.rect(screen,
                             color,
                             pygame.Rect(math.ceil(x * SCREEN_W / len(self.bs.to_sort)),
                                         math.ceil(SCREEN_H - self.bs.to_sort[x] * SCREEN_H),
                                         math.ceil(SCREEN_W / len(self.bs.to_sort)),
                                         math.ceil(self.bs.to_sort[x] * SCREEN_H)))

    def synth(self, frequency, duration=0.05, sampling_rate=44100):
        '''
        I yoinked this function from this project:
        https://github.com/FinFetChannel/Python_Synth
        '''
        frequency *= 1000
        frames = int(duration*sampling_rate)
        arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        arr = arr + np.cos(4*np.pi*frequency*np.linspace(0,duration, frames))
        arr = arr - np.cos(6*np.pi*frequency*np.linspace(0,duration, frames))
        arr = np.clip(arr*10, -1, 1) # squarish waves
        sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
        sound = pygame.sndarray.make_sound(sound.copy())

        sound.set_volume(0.1)
        sound.play()


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    running = True

    viz = Viz(20)

    while running:
        clock.tick(2)
        screen.fill((50,50,50))

        viz.run()
        viz.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
