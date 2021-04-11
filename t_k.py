import time
import cv2

cap1 = cv2.VideoCapture(0)
time.sleep(0.1)
# cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
# cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
cap2 = cv2.VideoCapture(1)
time.sleep(0.1)
cap3 = cv2.VideoCapture(2)
while True:
    _, frame1 = cap1.read()
    # print(frame1.shape[:2])
    _, frame2 = cap2.read()
    _, frame3 = cap3.read()
    # print(frame3.shape[:2])
    cv2.imshow("Frame1", frame1)
    cv2.imshow("Frame2", frame2)
    cv2.imshow("Frame3", frame3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()
