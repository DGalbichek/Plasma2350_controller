import utime


class Colour(object):
    def __init__(self, g, r, b):
        self.g = g
        self.r = r
        self.b = b

    def grb(self):
        return self.g, self.r, self.b

    def hsv(self):
        r = self.r / 255
        g = self.g / 255
        b = self.b / 255
        maxc = max(r, g, b)
        minc = min(r, g, b)
        rangec = maxc - minc
        v = maxc
        if minc == maxc:
            return 0.0, 0.0, v
        s = rangec / maxc
        rc = (maxc - r) / rangec
        gc = (maxc - g) / rangec
        bc = (maxc - b) / rangec
        if r == maxc:
            h = bc - gc
        elif g == maxc:
            h = 2.0 + rc-bc
        else:
            h = 4.0 + gc - rc
        h = (h / 6.0) % 1.0
        return h, s, v


class Scene(object):
    def next_frame(self, strip):
        pass


class ProgramStep(object):
    def __init__(self, scene, duration, params={}):
        if type(scene) == type:
            if params:
                self.scene = scene(**params)
            else:
                self.scene = scene()
        else:
            self.scene = scene
        self.duration = duration


class Program(object):
    def __init__(self, steps):
        self.steps = steps
        self.current_step = {}
        self.nstep = 999
        self.in_step_since = 999

    def start(self):
        self.current_step = ProgramStep(**self.steps[0])
        self.step = 0
        self.in_step_since = utime.time_ns()

    def tick(self, led_strip):
        t = utime.time_ns()
        elapsed = (t - self.in_step_since) / 10 ** 9
        #print(t, self.in_step_since, elapsed)
        if self.current_step.duration == 0 or elapsed >= self.current_step.duration:
            if len(self.steps) > 1:
                self.nstep = (self.nstep + 1) % len(self.steps)
                self.current_step = ProgramStep(**self.steps[self.nstep])
            self.in_step_since = utime.time_ns()

            self.current_step.scene.next_frame(led_strip)
