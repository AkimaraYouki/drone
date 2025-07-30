import cv2
import numpy as np

cap = cv2.VideoCapture(0)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
parameters = cv2.aruco.DetectorParameters()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    correct = cv2.undistort(frame, np.load('camera_matrix.npy'), np.load('dist_coeffs.npy'))
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(correct)

    if ids is not None:
        for i in range(len(ids)):
            cv2.aruco.drawDetectedMarkers(correct, corners, ids, (255, 255, 0))

        for i, id in enumerate(ids):
            print(f"Detected ID: {id[0]}")

    cv2.imshow('ArUco Detection', correct)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()