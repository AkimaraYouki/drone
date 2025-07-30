import cv2
import numpy as np

#Load UVC cam
cap = cv2.VideoCapture(0)

# Resize function
def frame_resize(reference , width , height):
    dim = (width, height)
    return cv2.resize(reference, dim, interpolation=cv2.INTER_AREA)

# Main camera function
def start_cam():
    # Resize the frame
    frame_resize(frame, 640, 320)
    # Correct distortion
    camera_matrix = np.load('camera_matrix.npy')
    dist_coeffs = np.load('dist_coeffs.npy')
    undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs)
    # Show cam
    cv2.imshow('Undistorted View', undistorted)
    img_canny = cv2.Canny(undistorted, 70, 160)
    cv2.imshow('canny', img_canny)



while True:
    ret, frame = cap.read()
    if not ret:
        print('Failed to capture image.')
        break
    start_cam()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Quitting...')
        break
cap.release()
cv2.destroyAllWindows()