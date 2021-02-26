import threading
import cv2

from src.stamp.detector import StampDetector
from src.arduino.communicator import ArduinoCom


class StampPicker:
    def __init__(self):
        self.stamp_detector = StampDetector()
        self.ard_com = ArduinoCom()
        self.frame = None

    @staticmethod
    def click_event(event, x, y, flags, params):

        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"[INFO] Point X: {x}, Point Y: {y}")

    def run(self):
        cap = cv2.VideoCapture(0)
        ard_threading = None
        stamp_x = 0
        stamp_y = 0
        while cap.isOpened():
            _, self.frame = cap.read()
            if self.ard_com.ard_res == "detect":
                detected_stamp = self.stamp_detector.detect_from_images(frame=self.frame)
                if detected_stamp:
                    stamp_x = int((detected_stamp[0] + detected_stamp[2]) / 2)
                    stamp_y = int((detected_stamp[1] + detected_stamp[3]) / 2)
                    cv2.circle(self.frame, (stamp_x, stamp_y), 5, (0, 0, 255), 3)
                    print(f"[INFO] Pick Stamp at {stamp_x}, {stamp_y}")
                    ard_threading = threading.Thread(target=self.ard_com.communicate_arduino,
                                                     args=[f"{stamp_x},{stamp_y}", ])
                    ard_threading.start()
                    self.ard_com.ard_res = None

            if stamp_x != 0 and stamp_y != 0:
                cv2.circle(self.frame, (stamp_x, stamp_y), 5, (0, 0, 255), 3)
            cv2.imshow("Stamp Detector", self.frame)
            cv2.setMouseCallback('Stamp Detector', self.click_event)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        ard_threading.join()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    StampPicker().run()
