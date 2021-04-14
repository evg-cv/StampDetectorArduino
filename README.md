# StampDetectorArduino

## Overview

This project is to detect the stamp in the frame captured by web camera and send its coordinate to Arduino so that 
a robot can pick the detected stamp. Faster_RCNN_Resnet_101 model is trained to detect the stamp.

Then when the robot moves the picked stamp in front of 2 cameras which are used to take the top and bottom side of the 
stamp, it is estimated whether the stamps picked by the robot are multi or single and if there is only one stamp, 
a front side of the stamp is estimated among 2 photos taken by the 2 cameras.

In the next step, the correct orientation of the stamp is determined to rotate into the correct direction, and finally 
the stamp is aligned into the white paper with the specific image processing.

This process is iterated by communicating between Arduino and PC.

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

- user_config

    Some configurations of user input for image processing like contrast, brightness, sharpness, gamma, white balance. 
## Installation

- Environment

    Ubuntu 18.04(Recommended), Windows 10, Python 3.6

- Dependency Installation

    Please navigate to this project directory and run the following command in the terminal.
    ```
        pip3 install -r requirements.txt
    ```

- Please create "model" folder in the "utils" folder and copy the 2 deep learning models into the "model" folder.

- Please create "credential" folder in the "utils" folder and copy the vision_key.txt file into the "credential" folder.

## Execution

- Configuration (in user_config file)

    * arduino_port: the port connected with Arduino.
    * gamma: float value for gamma of image processing 
    * brightness: int value between -255 and 255 for brightness
    * contrast: int value between -127 and 127 for contrast
    * sharpness: bool value with true and false for sharpness
    * white_balance: bool value with true and false for white balance
    * collection_number: int value of collection number
    * top_cam: int value of top camera number
    * bottom_cam: int value of bottom camera number
    * stamp_detector_cam: int value of stamp detector camera number

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

- Communication between PC and Arduino

    1. Arduino -> PC: "detect": PC detects the stamp
    2. Once PC detects the stamp: PC -> Arduino: coordinate with x, y like "x,y"
    3. Robot moves the stamp, Arduino -> PC: "moved", PC takes the photos of top and bottom
    4. If multi stamps or not any stamp, PC -> Arduino: "retry"
    5. If single, after estimation of the front side and rotation, PC aligns the stamp.
    6. If alignment is not complete, PC -> Arduino: "retry"
    7. If alignment is complete, PC -> Arduino: "complete"
