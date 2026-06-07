import cv2
import numpy as np

HEAD_POSE_POINTS = [1, 33, 263, 61, 291, 199]

FACE_3D = np.array([
    (0.0, 0.0, 0.0),         # nariz
    (-30.0, -30.0, -30.0),   # ojo izquierdo
    (30.0, -30.0, -30.0),    # ojo derecho
    (-25.0, 30.0, -30.0),    # boca izquierda
    (25.0, 30.0, -30.0),     # boca derecha
    (0.0, 65.0, -5.0)        # mentón
], dtype=np.float64)


def calculate_head_pose(face_landmarks, w, h):

    head_points = []

    for idx in HEAD_POSE_POINTS:
        landmark = face_landmarks.landmark[idx]

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        head_points.append((x, y))

    face_2d = np.array(head_points, dtype=np.float64)

    focal_length = w

    cam_matrix = np.array([
        [focal_length, 0, w / 2],
        [0, focal_length, h / 2],
        [0, 0, 1]
    ], dtype=np.float64)

    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    success, rot_vec, trans_vec = cv2.solvePnP(
        FACE_3D,
        face_2d,
        cam_matrix,
        dist_matrix
    )

    if not success:
        return 0, 0, 0, head_points

    rmat, _ = cv2.Rodrigues(rot_vec)

    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

    pitch = angles[0]
    yaw = angles[1]
    roll = angles[2]

    return pitch, yaw, roll, head_points