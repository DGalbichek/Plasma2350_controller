import random

import rgb_colours

from abstract import Colour, Program, Scene
from grid66 import green_pine_image, blank_image


class BlankScene(Scene):
    def next_frame(self, strip):
        for i in range(66):
            strip.set_hsv(i, 0, 1.0, 0)


class Pulsar(object):
    def __init__(self, lifespan=1, stepper = 0.1):
        self.intensity = 0.1
        self.stepper = stepper
        self.lifespan = lifespan
        self.age = 0

    def tick(self):
        self.intensity += self.stepper
        if self.intensity > 1:
            self.stepper *= -1
        elif self.intensity < 0.1 + abs(self.stepper) and self.age < self.lifespan - 1:
            self.age += 1
            self.stepper *= -1
        elif self.intensity < 0:
            return True

        return False


class LonelyPulsarScene(Scene):
    def __init__(self, colour=rgb_colours.RGB_SILVER, lifespan=2, stepper=0.05):
        self.colour = Colour(*colour)
        self.lifespan = lifespan
        self.stepper = stepper
        self.position = 10
        self.pulsar = Pulsar(lifespan, stepper)

    def next_frame(self, strip):
        for n in range(66):
            if n == self.position:
                hsv = self.colour.hsv()
                strip.set_hsv(n, hsv[0], hsv[1], self.pulsar.intensity)
                ended = self.pulsar.tick()
                if ended:
                    self.position = random.randint(0, 65)
                    self.pulsar = Pulsar(self.lifespan, self.stepper)
            else:
                strip.set_hsv(n, 0 , 0, 0)


class MarchingScene(Scene):
    def __init__(self, colour=rgb_colours.RGB_SILVER, gap=3):
        self.colour = Colour(*colour)
        self.gap = gap
        self.cycle = 0

    def next_frame(self, strip):
        for n in range(66):
            if n % self.gap == self.cycle:
                strip.set_hsv(n, *self.colour.hsv())
            else:
                strip.set_hsv(n, 0 , 0, 0)

        self.cycle = (self.cycle + 1) % self.gap


class PulsarsScene(Scene):
    def __init__(self, colour=rgb_colours.RGB_SILVER):
        self.colour = Colour(*colour)
        self.tracker = [None] * 66

    def next_frame(self, strip):
        empties = [n for n, x in enumerate(self.tracker) if not x]
        self.tracker[empties[random.randint(0, len(empties) - 1)]] = Pulsar()
        for n in range(66):
            if self.tracker[n]:
                hsv = self.colour.hsv()
                strip.set_hsv(n, hsv[0], hsv[1], self.tracker[n].intensity)
                ended = self.tracker[n].tick()
                if ended:
                    self.tracker[n] = None
            else:
                strip.set_hsv(n, 0 , 0, 0)


class RainbowScene(Scene):
    def __init__(self, intensity=1.0):
        self.offset = 0.0
        self.intensity = intensity

    def next_frame(self, strip):
        self.offset += float(10) / 1000.0

        for i in range(66):
            hue = float(i) / 66
            strip.set_hsv(i, hue+self.offset, 1.0, self.intensity)


class SparkleScene(Scene):
    def __init__(self, colour=rgb_colours.RGB_SILVER):
        self.colour = Colour(*colour)

    def next_frame(self, strip):
        for n in range(66):
            strip.set_hsv(n, 0 , 0, 0)
        for n in range(10):
            strip.set_hsv(random.randint(0, 65), *self.colour.hsv())


class ThereAndBackScene(Scene):
    def __init__(self):
        self.head = 3
        self.len = 4
        self.dir = 1

    def next_frame(self, strip):
        strip.set_rgb(self.head, 235, 255, 0)
        for n in range(1, self.len + 1):
            i = self.head + (self.dir * -1 * n)
            strip.set_rgb(i, int(235/4*(4-n)), int(255/4*(4-n)), 0)
        self.head += self.dir
        if self.head > 65:
            self.head = 66 - self.len
            self.dir = -1
        elif self.head < 0:
            self.head = self.len - 1
            self.dir = 1


PROGRAM_BANK = [
    Program([{'scene': ThereAndBackScene,
              'duration': 5,
              'frameduration': 0.05},
              {'scene': BlankScene,
               'duration': 0.01,
               'frameduration': 0},
              {'scene': BlankScene,
               'duration': 1,
               'frameduration': 2},
              {'scene': PulsarsScene,
              'duration': 20,
              'frameduration': 0.1,
              'params': {'colour': rgb_colours.RGB_DARKORANGE}},
              {'scene': RainbowScene,
              'duration': 15,
              'frameduration': 0,
              'params': {'intensity': 1.0}}, ]),
    Program([{'scene': MarchingScene,
              'duration': 0,
              'frameduration': 1,
              'params': {'colour': rgb_colours.RGB_DARKORANGE, 'gap': 5}}]),
    Program([{'scene': LonelyPulsarScene,
              'duration': 0,
              'frameduration': 0.1,
              'params': {'colour': rgb_colours.RGB_DARKORANGE}}]),
    Program([{'scene': PulsarsScene,
              'duration': 0,
              'frameduration': 0.2,
              'params': {'colour': rgb_colours.RGB_DARKORANGE}}]),
    Program([{'scene': RainbowScene,
              'duration': 0,
              'frameduration': 0,
              'params': {'intensity': 1.0}}]),
    Program([{'scene': ThereAndBackScene,
              'duration': 0,
              'frameduration': 0.05}]),
]

'''not_in_use = [
    Program([
        {'scene': green_pine_image, 'duration': 2},
        {'scene': blank_image, 'duration': 2},
    ]),
    #Program([{'scene': MarchingScene, 'duration': 0.5, 'params': {'colour': rgb_colours.RGB_PINK, 'gap': 4}}]),
    #Program([{'scene': MarchingScene, 'duration': 0.5, 'params': {'colour': rgb_colours.RGB_DARKORANGE}}]),
    #Program([{'scene': LonelyPulsarScene, 'duration': 0.1}]),
    #Program([{'scene': PulsarsScene, 'duration': 0.2}]),
    #Program([{'scene': SparkleScene, 'duration': 0}]),
    #Program([{'scene': SparkleScene, 'duration': 0, 'params': {'colour': rgb_colours.RGB_YELLOW}}]),
    #Program([{'scene': SparkleScene, 'duration': 0, 'params': {'colour': rgb_colours.RGB_DARKORANGE}}]),
    #Program([{'scene': SparkleScene, 'duration': 0, 'params': {'colour': rgb_colours.RGB_DARKGREEN}}]),
    #Program([{'scene': ThereAndBackScene, 'duration': 0.2}]),
    #Program([{'scene': ThereAndBackScene, 'duration': 0.15}]),
    #Program([{'scene': ThereAndBackScene, 'duration': 0.1}]),
    Program([{'scene': RainbowScene, 'duration': 0, 'params': {'intensity': 0.66}}]),
    Program([{'scene': RainbowScene, 'duration': 0, 'params': {'intensity': 0.33}}]),
]'''
