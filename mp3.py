#!/usr/bin/env python3

import sys, threading, time, os, subprocess, st7789
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

# Home directory and file extension
# change to full path of your music folder
directory = '/home/user/music'
file_extension = '.mp3'

# GPIO pins for buttons
button1 = Button(5)
button2 = Button(6)
button3 = Button(16)
button4 = Button(24)

# Display type and initialization
display_type = "square"

# Selected file index
selectedindex = 0

# Initialize file paths and names
paths = []
files = []

# Scan for MP3 files in the specified directory
def scan_files():
    global paths, files
    paths.clear()
    files.clear()
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(file_extension):
                paths.append(os.path.join(dirpath, filename))
                files.append(filename)

# Play the selected MP3 file using mpg321 and make it properly resets alsa when playing is started and stopped
def reset_alsa():
    release_alsa()
    subprocess.run(["sudo", "alsactl", "init"])
    subprocess.run(["sudo", "alsa", "force-reload"])

current_process = None

def release_alsa():
    subprocess.run(["sudo", "fuser", "-k", "/dev/snd/pcmC0D0p"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

current_process = None

def play_file(index):
    global current_process
    global current_process
    reset_alsa()
    release_alsa()
    if current_process:
        current_process.terminate()
    if 0 <= index < len(paths):
        filepath = paths[index]
        current_process = subprocess.Popen(["mpg321", "-g", "50", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if current_process:
        current_process.terminate()
    if 0 <= index < len(paths):
        filepath = paths[index]
        current_process = subprocess.Popen(["mpg321", "-g", "50", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if 0 <= index < len(paths):
        filepath = paths[index]
        subprocess.Popen(["mpg321", "-g", "50", filepath])

# Handle button presses
def handle_button(bt):
    global selectedindex
    if bt.pin.number == 16:
        selectedindex = max(0, selectedindex - 1)
    elif bt.pin.number == 24:
        selectedindex = min(len(files) - 1, selectedindex + 1)
    elif bt.pin.number == 6:
        scan_files()
    elif bt.pin.number == 5:
        play_file(selectedindex)

# Attach button handlers
button1.when_pressed = handle_button
button2.when_pressed = handle_button
button3.when_pressed = handle_button
button4.when_pressed = handle_button

# Display Initialization
if display_type == "square":
    disp = st7789.ST7789(
        height=240,
        rotation=90,
        port=0,
        cs=st7789.BG_SPI_CS_FRONT,
        dc=9,
        backlight=13,
        spi_speed_hz=80 * 1000 * 1000
    )
else:
    print("Invalid display type!")

# Initialize display
disp.begin()
WIDTH, HEIGHT = disp.width, disp.height
img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

# Main loop
scan_files()
visible_lines = HEIGHT // 30
scroll_offset = 0

while True:
    time.sleep(0.1)
    draw.rectangle((0, 0, WIDTH, HEIGHT), (0, 0, 0))
    if selectedindex >= scroll_offset + visible_lines:
        scroll_offset += 1
    elif selectedindex < scroll_offset:
        scroll_offset = max(0, scroll_offset - 1)

    visible_files = files[scroll_offset:scroll_offset + visible_lines]

    for i, line in enumerate(visible_files):
        y_pos = 10 + ((i % visible_lines) * 30)
        if scroll_offset + i == selectedindex:
            draw.rectangle([10, y_pos, WIDTH - 10, y_pos + 30], fill=(255, 255, 255))
            draw.text((10, y_pos), line, font=font, fill=(0, 0, 0))
        else:
            draw.text((10, y_pos), line, font=font, fill=(255, 255, 255))
    disp.display(img)
