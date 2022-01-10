# MIT License

# Copyright (c) 2020 Jonathan Ludwig, Michal Kozma

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import, print_function

from devices import init_gpio
from neopixel import *
import logging
from devices.lightstrip import RgbColor
from tests.testneo.neopixel import Color, Adafruit_NeoPixel

# TODO: Not sure what should be exposed through class contructor/setters
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class ColorStrip2:
    def __init__(self, device_cfg, led_freq):
        self._current_color = RgbColor(0, 0, 0)
        init_gpio()
        # Create NeoPixel object with appropriate configuration.
        logging.info('Initializing Neopixel driver with %u LEDs' % device_cfg.getint('LightStrip2', 'led_count'))
        self._strip = Adafruit_NeoPixel(device_cfg.getint('LightStrip2', 'led_count'), device_cfg.getint('LightStrip2', 'pin'), led_freq, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self._strip.begin()

    # Define functions which animate LEDs in various ways.
    def set_color(self, color, wait_ms=0):
        """Wipe color across display a pixel at a time."""
        if self._current_color == color:
            # No change
            return
        logging.info('Changing LED strip color to (%u,%u,%u)' % (color.red, color.green, color.blue))
        for i in range(self._strip.numPixels()):
            self._strip.setPixelColor(i, Color(color.green, color.red, color.blue))
            self._strip.show()
            # time.sleep(wait_ms/1000.0)
        self._current_color = color