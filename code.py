# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import pulseio
import board
import adafruit_irremote
import time
import neopixel

from adafruit_circuitplayground import cp
import gc

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

# NeoPixels Setup
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


num_pixels = 10
cp.pixels.brightness = 0.4


def color_chase(wait):
    COLORS = (
        RED, YELLOW, GREEN, CYAN, BLUE, PURPLE
    )
    num_colors = len(COLORS)
    pos = 0
    for i in range(num_pixels):
        r,g,b = COLORS[pos]
        cp.pixels[i] = (r, g, b)
        time.sleep(wait)
        color_off(i)
        pos += 1
        pos %= num_colors
    time.sleep(0.5)


def color_off(pos: int):
    cp.pixels[pos] = (0, 0, 0)


def color_wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j
            cp.pixels[i] = color_wheel(rc_index & 255)
        cp.pixels.show()
        time.sleep(wait)


while True:
    pulses = decoder.read_pulses(pulsein)
    try:
        # Attempt to convert received pulses into numbers
        received_code = decoder.decode_bits(pulses)
    except adafruit_irremote.IRNECRepeatException:
        # We got an unusual short code, probably a 'repeat' signal
        # print("NEC repeat!")
        continue
    except adafruit_irremote.IRDecodeException as e:
        # Something got distorted or maybe its not an NEC-type remote?
        # print("Failed to decode: ", e.args)
        continue

    print("NEC Infrared code received: ", received_code)
    if received_code == (64, 191, 101, 154):
        color_chase(0.1)
        gc.collect()

