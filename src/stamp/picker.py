import cv2

from src.stamp.detector import StampDetector
from src.arduino.communicator import ArduinoCom


class StampPicker:
    def __init__(self):
        self.stamp_detector = StampDetector()
        self.ard_com = ArduinoCom()
        self.detect_ret = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            _, frame = cap.read()
            detected_stamp = self.stamp_detector.detect_from_images(frame=frame)
            self.detect_ret = False
            stamp_x = int((detected_stamp[0] + detected_stamp[2]) / 2)
            stamp_y = int((detected_stamp[1] + detected_stamp[3]) / 2)
            print(f"[INFO] Pick Stamp at {stamp_x}, {stamp_y}")
            ard_res = self.ard_com.communicate_arduino(coordinates=f"{stamp_x},{stamp_y}")
            print(f"[INFO] Arduino Command: {ard_res}")
            if cv2.waitKey(0) or 0xff == ord('q'):
                break
        cap.release()


if __name__ == '__main__':
    StampPicker().run()
