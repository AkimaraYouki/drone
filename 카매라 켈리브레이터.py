import cv2
import numpy as np
import glob

# internal coner count
CHECKERBOARD = (9, 6)

objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

objpoints = []
imgpoints = []

images = glob.glob('checkerboard_images/*.jpg')

last_gray = None
for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print(f"can't load image: {fname}")
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    last_gray = gray

    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        imgpoints.append(corners2)

        # Visualize the checking process
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

# noinspection PyTypeChecker
ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, last_gray.shape[::-1], None, None)

np.save('camera_matrix.npy', cameraMatrix)
np.save('dist_coeffs.npy', distCoeffs)
print(np.load('camera_matrix.npy'))
print(np.load('dist_coeffs.npy'))
print("Calibration complete.")
