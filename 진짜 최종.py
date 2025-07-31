import cv2
import numpy as np

# --- Per-marker rotation corrections (local frame) ---
rotation_corrections = {
    0: np.array([[ 0, 0, -1], [0, 1, 0], [1, 0, 0]], dtype=np.float32),  # Y-axis +90°
    1: np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=np.float32) @
       np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=np.float32),# Z flip + X flip
    2: np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype=np.float32),  # custom
    3: np.eye(3, dtype=np.float32),                                       # no rotation
    4: np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=np.float32),   # X-axis +90°
    5: np.array([[1,0,0], [0,0,1], [0,-1,0]], dtype=np.float32) @
       np.array([[0,-1,0], [1,0,0], [0,0,1]], dtype=np.float32) @
       np.array([[0,-1,0], [1,0,0], [0,0,1]], dtype=np.float32)          # X then Z twice
}

# --- Per-marker translation offsets along local axes (in meters) ---
translation_offsets = {
    0: (-0.05, 0.0, 0.0),  # move -5cm along local X
    1: (0.0, 0.0,  0.05),  # +Z
    2: ( 0.05,0.0, 0.0),   # +X
    3: (0.0, 0.0, -0.05),  # -Z
    4: (0.0, 0.05,0.0),    # +Y
    5: (0.0,-0.05,0.0)     # -Y
}

cap = cv2.VideoCapture(0)

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
parameters = cv2.aruco.DetectorParameters()

def draw_custom_axes(img, camera_matrix, dist_coeffs, rvec, tvec, length=0.05, thickness=3):
    axis_points = np.float32([
        [0, 0, 0],          # origin
        [length, 0, 0],     # x axis
        [0, length, 0],     # y axis
        [0, 0, length]      # z axis
    ]).reshape(-1, 3)

    imgpts, _ = cv2.projectPoints(axis_points, rvec, tvec, camera_matrix, dist_coeffs)
    imgpts = np.int32(imgpts).reshape(-1, 2)

    # Draw the three axes with custom colors
    cv2.line(img, imgpts[0], imgpts[1], (255, 255, 255), thickness)  # X axis (red)
    cv2.line(img, imgpts[0], imgpts[2], (255, 255, 255), thickness)  # Y axis (green)
    cv2.line(img, imgpts[0], imgpts[3], (255, 255, 255), thickness)  # Z axis (blue)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    correct_color = cv2.undistort(frame, np.load('camera_matrix.npy'), np.load('dist_coeffs.npy'))
    correct_gray = cv2.cvtColor(correct_color, cv2.COLOR_BGR2GRAY)

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(correct_gray)
    camera_matrix = np.load('camera_matrix.npy')
    dist_coeffs = np.load('dist_coeffs.npy')
    marker_length = 0.1  # 3 cm

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(correct_color, corners, ids, (255, 255, 0))

        # --- Estimate, correct, and draw each marker ###
        rvec_list, tvec_list = [], []
        for i, marker_id in enumerate(ids.flatten()):
            # 1) base pose estimation
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                [corners[i]], marker_length, camera_matrix, dist_coeffs
            )
            R, _ = cv2.Rodrigues(rvec[0])

            # 2) apply per-marker rotation correction
            R_corr = rotation_corrections.get(marker_id, np.eye(3, dtype=np.float32))
            R_new = R @ R_corr

            # 3) apply per-marker translation offset along its local axes
            dx, dy, dz = translation_offsets.get(marker_id, (0.0,0.0,0.0))
            t_offset_vec = dx * R_new[:,0] + dy * R_new[:,1] + dz * R_new[:,2]
            tvec_adj = (tvec[0].reshape(3) + t_offset_vec).reshape(1,3)

            # 4) convert corrected rotation back to rvec
            rvec_adj, _ = cv2.Rodrigues(R_new)

            # 5) draw built-in axes for this marker with thickness=5
            cv2.drawFrameAxes(correct_color, camera_matrix, dist_coeffs, rvec_adj, tvec_adj.reshape(3,1), 0.05, 8)

            # 6) collect for cube-center averaging
            rvec_list.append(rvec_adj)
            tvec_list.append(tvec_adj.reshape(3,1))

        # --- Compute and draw cube-center pose via simple averaging ---
        if rvec_list:
            tmat = np.hstack(tvec_list)  # 3×N
            t_center = np.mean(tmat, axis=1).reshape(3,1)
            # approximate rotation average by mean of rvecs
            rmat = np.vstack([r.flatten() for r in rvec_list])
            r_center = np.mean(rmat, axis=0).reshape(3,1)
            draw_custom_axes(correct_color, camera_matrix, dist_coeffs, r_center, t_center, length=0.1, thickness=5)

    cv2.imshow('ArUco Detection', correct_color)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()