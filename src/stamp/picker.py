import threading
import cv2

from src.stamp.detector import StampDetector
from src.arduino.communicator import ArduinoCom


class StampPicker:
    def __init__(self):
        self.stamp_detector = StampDetector()
        self.ard_com = ArduinoCom()

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            _, frame = cap.read()
            if self.ard_com.ard_res == "detect":
                detected_stamp = self.stamp_detector.detect_from_images(frame=frame)
                stamp_x = int((detected_stamp[0] + detected_stamp[2]) / 2)
                stamp_y = int((detected_stamp[1] + detected_stamp[3]) / 2)
                cv2.circle(frame, (stamp_x, stamp_y), 5, (0, 0, 255), 3)
                print(f"[INFO] Pick Stamp at {stamp_x}, {stamp_y}")
                ard_threading = threading.Thread(target=self.ard_com.communicate_arduino,
                                                 args=[f"{stamp_x},{stamp_y}", ])
                ard_threading.start()
                self.ard_com.ard_res = None

            cv2.imshow("Stamp Detector", frame)
            if cv2.waitKey(1) or 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    StampPicker().run()
