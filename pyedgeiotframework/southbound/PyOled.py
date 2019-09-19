"""
ToDo: replace Adafrui_ssd1306 par luma -> https://github.com/rm-hull/luma.oled
"""
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
# import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class PyOled(EdgeService):

    def __init__(self):
        # ----
        EdgeService.__init__(self)
        # ----
        self.RST = None  # on the PiOLED this pin isnt used
        self.display_connected = False
        self.interligne = 8
        self.line_one = "Starting ..."
        self.line_two = ""
        self.line_three = ""
        self.line_four = ""
        self.line_five = ""
        self.line_six = ""
        self.line_seven = ""
        self.line_eight = ""

        self.power_on = True
        # 128x64 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)

        try:
            # Initialize library.
            self.disp.begin()

            # Clear display.
            self.disp.clear()
            self.disp.display()

            # Create blank image for drawing.
            # Make sure to create image with mode '1' for 1-bit color.
            self.width = self.disp.width
            self.height = self.disp.height

            self.image = Image.new('1', (self.width, self.height))

            # Get drawing object to draw on image.
            self.draw = ImageDraw.Draw(self.image)

            # Draw a black filled box to clear the image.
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

            # Draw some shapes.
            # First define some constants to allow easy resizing of shapes.
            padding = -2
            self.top = padding
            self.bottom = self.height - padding
            # Move left to right keeping track of the current x position for drawing shapes.
            self.x = 0

            # Load default font.
            self.font = ImageFont.load_default()

            # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
            # Some other nice fonts to try: http://www.dafont.com/bitmap.php
            # font = ImageFont.truetype('Minecraftia.ttf', 8)

            self.display_connected = True

        except OSError:
            self.display_connected = False
            print("no display")

    def run(self):
        # ----
        EdgeService.run(self)
        # ----
        while self.display_connected:
            # Draw a black filled box to clear the image.
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            # Write two lines of text.
            self.draw.text((self.x, self.top + (self.interligne * 0)), self.line_one, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 1)), self.line_two, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 2)), self.line_three, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 3)), self.line_four, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 4)), self.line_five, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 5)), self.line_six, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 6)), self.line_seven, font=self.font, fill=255)
            self.draw.text((self.x, self.top + (self.interligne * 7)), self.line_eight, font=self.font, fill=255)
            # Display image.
            self.disp.image(self.image)
            self.disp.display()

    def display_lines(self):
        if self.display_connected:
            if self.power_on:
                # Draw a black filled box to clear the image.
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

                # Write two lines of text.

                self.draw.text((self.x, self.top + (self.interligne * 0)), self.line_one, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 1)), self.line_two, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 2)), self.line_three, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 3)), self.line_four, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 4)), self.line_five, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 5)), self.line_six, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 6)), self.line_seven, font=self.font, fill=255)
                self.draw.text((self.x, self.top + (self.interligne * 7)), self.line_eight, font=self.font, fill=255)

                # Display image.
                self.disp.image(self.image)
                self.disp.display()
                # time.sleep(.1)
            else:
                # Clear display.
                self.disp.clear()
                self.disp.display()
