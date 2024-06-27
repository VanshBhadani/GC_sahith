import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
else:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
    else:
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    cap.release()
