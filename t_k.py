import threading
import time
import cv2


class CamThread:
    def __init__(self):
        self.top_frame = None
        self.bottom_frame = None
        self.stamp_detector_frame = None
        self.break_ret = False

    def get_frame(self, num_port, cam_cat):
        cap = cv2.VideoCapture(num_port)
        while True:
            if self.break_ret:
                cap.release()
                break
            _, frame = cap.read()
            if cam_cat == "top":
                self.top_frame = frame
            elif cam_cat == "bottom":
                self.bottom_frame = frame
            elif cam_cat == "stamp":
                self.stamp_detector_frame = frame
            time.sleep(0.02)

        return

    def run(self):
        top_frame_thread = threading.Thread(target=self.get_frame, args=[0, "top"])
        bottom_frame_thread = threading.Thread(target=self.get_frame, args=[1, "bottom"])
        stamp_frame_thread = threading.Thread(target=self.get_frame, args=[2, "stamp"])
        top_frame_thread.start()
        bottom_frame_thread.start()
        stamp_frame_thread.start()
        time.sleep(2)
        while True:
            cv2.imshow("Top Frame", self.top_frame)
            cv2.imshow("Bottom Frame", self.bottom_frame)
            cv2.imshow("Stamp Detector Frame", self.stamp_detector_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.break_ret = True
                top_frame_thread.join()
                bottom_frame_thread.join()
                stamp_frame_thread.join()
                break
        cv2.destroyAllWindows()

        return


if __name__ == '__main__':
    CamThread().run()
