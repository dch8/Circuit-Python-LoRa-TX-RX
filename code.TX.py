# This was originally created by Dygear


#Remae to code.py on the TX side feather board

import os
import time
import board
import busio
import digitalio
import adafruit_rfm9x
import adafruit_gps
import neopixel

UNIT_ID = os.getenv("UNIT_ID", "UNKNOWN")
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
color_values = [
    (255,  0,  0), # 31 - Red
    (  0,255,  0), # 32 - Green
    (255,255,  0), # 33 - Yellow
    (  0,  0,255), # 34 - Blue
    (255,  0,255), # 35 - Magenta
    (  0,255,255), # 36 - Cyan
    (255,255,255), # 37 - White
    (  0,  0,  0), # 30 - Black
]
color_index = 0

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

LoRA = adafruit_rfm9x.RFM9x(
    board.SPI(),
    digitalio.DigitalInOut(board.RFM_CS),
    digitalio.DigitalInOut(board.RFM_RST),
    frequency = 915.0
)
LoRA.signal_bandwidth = 125000
print(f"signal_bandwidth: {LoRA.signal_bandwidth}")
LoRA.spreading_factor = 10
print(f"spreading_factor: {LoRA.spreading_factor}")
LoRA.coding_rate = 8
print(f"coding_rate: {LoRA.coding_rate}")
LoRA.enable_crc = True
print(f"enable_crc: {LoRA.enable_crc}")
LoRA.tx_power = 19;
print(f"tx_power: {LoRA.tx_power}")

last_print = time.monotonic()
while True:
    gps.update()
    current = time.monotonic()
    if current - last_print >= 1.0:
        pixel.fill(color_values[color_index])
        color_index = (color_index + 1) % len(color_values)
        last_print = current
        if not gps.has_fix:
            print("Waiting for fix...")
            continue

        print(f"GPS;{UNIT_ID};{gps.latitude:4.8f},{gps.longitude:4.8f},{gps.altitude_m};{gps.satellites:02d};{gps.has_fix};{gps.timestamp_utc.tm_year:4d}-{gps.timestamp_utc.tm_mon:02d}-{gps.timestamp_utc.tm_mday:02d} {gps.timestamp_utc.tm_hour:02d}:{gps.timestamp_utc.tm_min:02d}:{gps.timestamp_utc.tm_sec:02d}")
        LoRA.send(bytes(f"GPS;{UNIT_ID};{gps.latitude:4.8f},{gps.longitude:4.8f},{gps.altitude_m};{gps.satellites:02d};{gps.has_fix};{gps.timestamp_utc.tm_year:4d}-{gps.timestamp_utc.tm_mon:02d}-{gps.timestamp_utc.tm_mday:02d} {gps.timestamp_utc.tm_hour:02d}:{gps.timestamp_utc.tm_min:02d}:{gps.timestamp_utc.tm_sec:02d}", "UTF-8"))
