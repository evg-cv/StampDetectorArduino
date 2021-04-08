import cv2

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap3 = cv2.VideoCapture(2)
while True:
    _, frame1 = cap1.read()
    _, frame2 = cap2.read()
    _, frame3 = cap3.read()
    cv2.imshow("Frame1", frame1)
    cv2.imshow("Frame2", frame2)
    cv2.imshow("Frame3", frame3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap1.release()
cap2.release()
cv2.destroyAllWindows()
