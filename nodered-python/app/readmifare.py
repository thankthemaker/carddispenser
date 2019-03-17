import binascii
import sys
import signal
import time

import Adafruit_PN532 as PN532

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Setup how the PN532 is connected to the Raspbery Pi/BeagleBone Black.
# It is recommended to use a software SPI connection with 4 digital GPIO pins.

# Configuration for a Raspberry Pi:
CS   = 8
MOSI = 10
MISO = 9
SCLK = 11

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

# Call begin to initialize communication with the PN532.  Must be done before
# any other calls to the PN532!
pn532.begin()

# Get the firmware version from the chip and print(it out.)
ic, ver, rev, support = pn532.get_firmware_version()
##print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards.
pn532.SAM_configuration()

# Main loop to detect cards and read a block.
##print('Waiting for MiFare card...')
while True:
    # Check if a card is available to read.
    uid = pn532.read_passive_target()
    # Try again if no card is available.
    if uid is None:
        continue
##    print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
##    print('{0}'.format(binascii.hexlify(uid)))
    uid_hex = binascii.hexlify(uid)
    byte1 = int("0x" + uid_hex[0:2],0)
    byte2 = int("0x" + uid_hex[2:4],0)
    byte3 = int("0x" + uid_hex[4:6],0)
    byte4 = int("0x" + uid_hex[6:8],0)
    token =  (byte1 << 24) + (byte2 << 16) + (byte3 << 8) + byte4
    print('{:012d}'.format(token))
    time.sleep(5)
