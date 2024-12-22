import machine
import plasma
import utime

from plasma import plasma2040

from program_bank import PROGRAM_BANK


BUTTON_A = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
ONBOARD_LED = machine.Pin("LED", machine.Pin.OUT)
ONBOARD_LED.on()


class StripController(object):
    def __init__(self):
        self.led_strip = plasma.WS2812(66, 0, 0, plasma2040.DAT)
        self.led_strip.start()
        self.program = None

    def _clear_strip(self):
        for i in range(66):
            self.led_strip.set_rgb(i, 0, 0, 0)

    def start_program(self, program):
        self._clear_strip()
        self.program = program
        self.program.start()

    def tick_program(self):
        self.program.tick(self.led_strip)


for n in range(6):
    ONBOARD_LED.toggle()
    utime.sleep(0.1)

program_no = 0
sc = StripController()
sc.start_program(PROGRAM_BANK[program_no])

while True:
    if BUTTON_A.value() == 0:
        ONBOARD_LED.off()
        while BUTTON_A.value() == 0:
            pass
        program_no = (program_no + 1) % len(PROGRAM_BANK)
        print('PROGRAM', program_no)
        sc.start_program(PROGRAM_BANK[program_no])
        ONBOARD_LED.on()

    sc.tick_program()
    utime.sleep(0.04)
