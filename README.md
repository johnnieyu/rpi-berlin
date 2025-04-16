# RPI Berlin

Berlin is an AI-powered camera that prints poetry on thermal paper from photos - like a polaroid camera, but with a twist. Named after the city of Berlin, I remember rediscovering my love for photography over the pandemic after finding a Berlin-based photo community - Safelight - and its Youtube channel. When I finally visited the city in October of 2022, I immediately fell in love with its culture around art and technology. As a city that I dream to live in, but will most likely never have a chance to live in, I'm naming a device that produces machine hallucinations after a city of my human delusions. 

The idea has been conceived long ago, but after research, the conviction to actually go build the camera was inspired by a project called [Poetry Camera](https://www.raspberrypi.com/news/this-camera-writes-poems/) by Kelin Carolyn Zhang and Ryan Mather, who I would encourage anyone interested to read more about. The creators have kindly open-sourced their code, and I've studied it as inspiration for the project. I will, however, be coding this project from scratch using a different software approach and hardware components for reasons that will be explained later. 

## Hardware

- **Raspberry Pi Zero 2 WH w/ soldered GPIO header:** Selected for its small form factor, low power consumption, price, and fast boot time.
- **PiSugar 3 Portable 1200 mAh Battery Pack:** Not sure if it's enough to power the camera and printer, but it'll have to do for now.
- **Arducam Camera Module 3:** Because RPI's Camera Module 3 is out of stock everywhere...

## Software

The plan is: 
- **/data:** directory for storing test files. 
- **/images:** directory for storing images. 
- **/poems:** directory for storing poems. 
- **capture.py:** detects button press and capture an image from the camera and save it to the SD card. 
- **ai.py:** run the image through an LLM and generate a poem. 
- **print.py:** print the poem on the thermal printer. 
- **main.py:** main script that orchestrates the capture, ai, and print. 

## Journal

### April 16, 2025

- There are a few missing components - I need bread boards and wire nuts. Ordered & arriving tomorrow. 
- Ordered a 3D printer that arrived today. Won't know how to design the enclosure until I get the software and hardware working, but this is my first 3D printing project so I'll be doing some test prints and learning everything I need to design the camera shell. 
- Started planning out the software architecuture - Github initiated today. 
- Added cdmx.jpg to the /data directory, the first photo I hand-printed in NYC. 

### April 15, 2025

- I ordered the components online over the weekend and they finally arrived today.
- I spent 3 hours trying to get the camera component working (since it's not a native RPI camera module) and finally found the solution online. After that, I realized that I threw out the instructions that told me exactly what I needed to do... so that's a lesson learned in reading instructions. 
- I was able to run `rpicam-hello` with success and got a picture from the camera. 
- Signing off at 1:30am to get some rest!