import cv2
import numpy as np

cap = cv2. VideoCapture(0)
save = 0
while True:
    ret, frame = cap.read()
    correct = cv2.undistort(frame, np.load('camera_matrix.npy'), np.load('dist_coeffs.npy'))
    cv2.imshow('frame', correct)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        save = save + 1
        cv2.imwrite(f'cube_{save}.jpg', correct)




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()