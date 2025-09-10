# This was originally created by Dygear
#rename to code.py on the RX feather board

import board
import digitalio
import neopixel
import adafruit_rfm9x

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.01
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

print("Waiting for packets...")
while True:
    packet = LoRA.receive(timeout=5.0)
    if packet is not None:
        if packet.startswith(b"GPS"):
            print(f"{packet.decode('utf-8')};{LoRA.snr:.2f};{LoRA.rssi:04d}")

        pixel.fill(color_values[color_index])
        color_index = (color_index + 1) % len(color_values)
