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
    def __init__(self, scene, duration, frameduration, params={}):
        if type(scene) == type:
            if params:
                self.scene = scene(**params)
            else:
                self.scene = scene()
        else:
            self.scene = scene
        self.duration = duration
        self.frameduration = frameduration


class Program(object):
    def __init__(self, steps):
        self.steps = steps
        self.current_step = {}
        self.nstep = 0
        self.in_frame_since = 999
        self.in_step_since = 999

    def start(self, n=0):
        self.current_step = ProgramStep(**self.steps[n])
        self.nstep = n
        self.in_frame_since = utime.time_ns()
        self.in_step_since = self.in_frame_since

    def tick(self, led_strip):
        t = utime.time_ns()
        if len(self.steps) > 1 and self.current_step.duration > 0:
            elapsed = (t - self.in_step_since) / 10 ** 9
            if elapsed >= self.current_step.duration:
                self.start((self.nstep + 1) % len(self.steps))

        elapsed = (t - self.in_frame_since) / 10 ** 9
        if self.current_step.frameduration == 0 or elapsed >= self.current_step.frameduration:
            self.current_step.scene.next_frame(led_strip)
            self.in_frame_since = utime.time_ns()
