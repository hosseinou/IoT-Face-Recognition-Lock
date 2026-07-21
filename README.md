# IoT Facial Recognition Smart Lock

This repository contains the software and hardware code for my Bachelor's Project in Electrical Engineering at Shiraz University (Fall 2021). The project was supervised by Dr. Mohammad Hassan Asemani.

This project implements an IoT-based smart lock system that uses computer vision to identify users and wirelessly commands an ESP8266 microcontroller to trigger a physical door lock.

## Project Components
The system is divided into two main parts: the Python-based server (Computer Vision) and the ESP8266-based client (Hardware).

### 1. Computer Vision (Python)
The facial recognition is handled using OpenCV. The pipeline consists of three scripts:
*   `label.py`: Captures ~30 grayscale images of a person's face via webcam to build a dataset.
*   `Train.py`: Processes the captured images, assigns IDs, and trains a Local Binary Patterns Histograms (LBPH) recognizer, saving the model as `trainer.yml`.
*   `Use.py`: Runs a live video feed and a background socket server on port 1250. It predicts the face in the frame. If the confidence score is <= 48, it sends the string `"OPENM"` over Wi-Fi to the ESP8266 client.

### 2. Hardware (ESP8266 & Arduino)
The hardware side is controlled by an ESP8266 Wi-Fi module. 
*   The ESP8266 connects to a local Wi-Fi hotspot and acts as a client to the Python server.
*   It continuously listens for incoming packets. 
*   When it receives the `"OPENM"` command, it sets Pin 14 to `LOW`.
*   This triggers a 5V relay (powered via a 12V source and a regulator), which actuates the electronic lock.
*   Using a non-blocking `millis()` timer, the pin returns to `HIGH` after exactly 2 seconds, safely re-locking the door.

## How to Run
1. Upload `client-server.ino` to the ESP8266 via the Arduino IDE. Ensure you update the Wi-Fi SSID, password, and the host IP to match your server.
2. Run `label.py` to register a new face dataset.
3. Run `Train.py` to generate the LBPH model.
4. Run `Use.py` and press `Enter` to start the live detection socket server.
