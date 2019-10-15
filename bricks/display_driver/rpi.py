from .driver import Driver as DriverBase
from time import sleep

try:
    from RPi import GPIO
except ModuleNotFoundError:
    from fake_rpi.RPi import GPIO


class Driver(DriverBase):
    def __init__(self, resolution, pins):
        self.w, self.h = resolution
        self.clk_pin, self.latch_pin, self.ds_pin = 17, 27, 22 if pins is None else pins

    def start(self):
        GPIO.setmode(GPIO.BCM)
        for pin, ini in [
            (self.clk_pin, GPIO.HIGH),
            (self.latch_pin, GPIO.HIGH),
            (self.ds_pin, GPIO.HIGH)
        ]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, ini)

    def stop(self):
        GPIO.cleanup()

    def push_frame(self, frame):
        load(frame)


GPIO.setmode(GPIO.BCM)

row_pins = c1, l1, d1 = 17, 27, 22
col_pins = c2, l2, d2 = 18, 23, 24

for p in (row_pins + col_pins):
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, GPIO.HIGH)

ds_delay = .000
clk_delay = .000
latch_delay = 0.000

n_cols = 6
n_rows = 14
col_track = 0


def push(bit, pins):
    clk, _, ds = pins
    GPIO.output(ds, bit)
    sleep(ds_delay)
    GPIO.output(clk, GPIO.LOW)
    sleep(clk_delay)
    GPIO.output(clk, GPIO.HIGH)
    sleep(clk_delay)


def sync(pins):
    _, latch, _ = pins
    GPIO.output(latch, GPIO.LOW)
    sleep(latch_delay)
    GPIO.output(latch, GPIO.HIGH)


s1, s2 = 0.001, 0


def load(frame):
    push(1, col_pins)
    for c in range(n_cols):
        for r in range(n_rows):
            push(int(frame[r][c]) == 0, row_pins)
        sync(row_pins)
        sync(col_pins)
        sleep(s1)
        push(0, col_pins)
    sleep(s2)
