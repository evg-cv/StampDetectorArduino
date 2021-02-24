import os


CUR_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(CUR_DIR, 'utils', 'model', 'stamp_detector.pb')

CONFIDENCE = 0.8
BAUD_RATE = 115200

ARDUINO_PORT = "/dev/ttyUSB0"
