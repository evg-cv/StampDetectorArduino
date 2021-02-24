# StampDetectorArduino

## Overview

This project is to detect the stamp in the frame captured by web camera and send its coordinate to Arduino so that 
a robot can pick the detected stamp. Faster_RCNN_Resnet_101 model is trained to detect the stamp.

## Structure

- arduino

    The Arduino code for communication between PC and Arduino

- src

    The main source code for detecting stamps and communication with Arduino
    
- utils

    * The deep learning model for stamp detection
    * The source code for management of files and folders

- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings

    Several settings including serial port
    
## Installation

- Environment

    Ubuntu 18.04(Recommended), Windows 10, Python 3.6

- Dependency Installation

    Please navigate to this project directory and run the following command in the terminal.
    ```
        pip3 install -r requirements.txt
    ```

- Please create "model" folder in the "utils" folder and copy the deep learning model into the "model" folder.

## Execution

- Please set ARDUINO_PORT variable in settings file with the port connected with Arduino.

- In the case of Ubuntu OS, please run the following command in the terminal.

    ```
        sudo chmod 666 {ARDUINO_PORT} # like /dev/ttyUSB0
    ```

- Please run the following command in the terminal.

    ```
        python3 app.py
    ```

## Note

- Please refer arduino/coordinate_sender.ino file for communication between Arduino and PC.
