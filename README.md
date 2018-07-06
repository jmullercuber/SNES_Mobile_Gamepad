# SNES_Mobile_Gamepad
Use your phone as a virtual SNES-style gamepad

## Requirements
- Linux
- Python 3
- [python-uinput](https://github.com/tuomasjjrasanen/python-uinput)
- desire to play SNES games without a legit gamepad

## Project Steps
1. Emulate virtual gamepad controller with uinput
2. Create local server that can receive data representing button actions (on phone)
    * Hook virtual controller to respond to incomming data
3. Create client for phone that sends button data to server

## Running
Execution should be fairly simple:

On server/computer being controlled, open a terminal and type

`sudo python3 webhook.py`
