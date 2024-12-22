from abstract import Scene

SHAPE_EMPTY = [
    ' . . . . . .',
    '. . . . . . ',
    ' . . . . . .',
    '. . . . . . ',
    ' . . . . . .',
    '. . . . . . ',
    ' . . . . . .',
    '. . . . . . ',
    ' . . . . . .',
    '. . . . . . ',
    ' . . . . . .',
]

class Grid66Image(Scene):
    def __init__(self, colours, shape):
        self.colours = colours
        self.shape = shape

    def __str__(self):
        s = []
        for n, r in enumerate(self.shape):
            s.append(''.join([x if m % 2 == n % 2 else ' ' for m, x in enumerate(r)]))
        return '\n'.join(s)

    def _to_strip_rgb(self):
        r = []
        for i in range(12):
            if i % 2 == 0:
                jj = range(10, -1, -2)
            else:
                jj = range(1, 11, 2)
            for j in jj:
                p = self.shape[j][i]
                if p == ' ':
                    r.append((0, 0, 0))
                else:
                    r.append(self.colours.get(p, (255, 255, 255)))
        return r

    def next_frame(self, led_strip):
        for n, p in enumerate(self._to_strip_rgb()):
            led_strip.set_rgb(n, p[1], p[0], p[2])


aa = [
    '#.#.#.#.#.#.',
    '.#.#.#.#.#.#',
    '#.#.#.#.#.#.',
    '.#.#.#.#.#.#',
    '#.#.#.#.#.#.',
    '.#.#.#.#.#.#',
    '#.#.#.#.#.#.',
    '.#.#.#.#.#.#',
    '#.#.#.#.#.#.',
    '.#.#.#.#.#.#',
    '#.#.#.#.#.#.',
]

aa = [
    ' . . .#. . .',
    '. . .#.#. . ',
    ' . .#. .#. .',
    '. .#. . .#. ',
    ' . .#. .#. .',
    '. .#. . .#. ',
    ' .#. . . .#.',
    '.#. . . . .#',
    ' .#.#.#.#.#.',
    '. . .#.#. . ',
    ' . . .#. . .',
]

'''aa = [
    ' . .#.#. . .',
    '. .#.#.#. . ',
    ' . .#.#. . .',
    '. .#. .#. . ',
    ' .#. . .#. .',
    '. .#. .#. . ',
    ' .#. . .#. .',
    '.#. . . .#. ',
    '#. . . . .#.',
    '.#.#.#.#.#. ',
    ' . .#.#. . .',
]'''

green_pine_image = Grid66Image(
    colours={'#': (34, 139, 34)},
    shape=[
        ' . . .#. . .',
        '. . .#.#. . ',
        ' . .#. .#. .',
        '. .#. . .#. ',
        ' . .#. .#. .',
        '. .#. . .#. ',
        ' .#. . . .#.',
        '.#. . . . .#',
        ' .#.#.#.#.#.',
        '. . .#.#. . ',
        ' . . .#. . .',
    ],
)

blank_image = Grid66Image(
    colours={},
    shape=[
        ' . . . . . .',
        '. . . . . . ',
        ' . . . . . .',
        '. . . . . . ',
        ' . . . . . .',
        '. . . . . . ',
        ' . . . . . .',
        '. . . . . . ',
        ' . . . . . .',
        '. . . . . . ',
        ' . . . . . .',
    ],
)

test_animation = [
    {'image': green_pine_image, 'duration': 2},
    {'image': blank_image, 'duration': 2},
]
