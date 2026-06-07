import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from detectors.eye_detector import get_eye_data
from detectors.mouth_detector import get_mouth_data
from detectors.head_pose_detector import calculate_head_pose
from services.driver_state_service import get_driver_state
from config.settings import (
    EAR_THRESHOLD,
    MIN_EAR,
    FATIGUE_FRAMES,
    MAR_THRESHOLD,
    YAWN_FRAMES,
    DISTRACTION_THRESHOLD,
    DISTRACTION_LIMIT,
    PITCH_DOWN_THRESHOLD,
    PITCH_UP_THRESHOLD,
    VERTICAL_DISTRACTION_LIMIT,
    PERCLOS_WINDOW
)

CLOSED_EYES_FRAMES = 0
MOUTH_OPEN_FRAMES = 0
DISTRACTION_FRAMES = 0
VERTICAL_DISTRACTION_FRAMES = 0

eye_history = deque(PERCLOS_WINDOW)

# Access the module that detects faces with points
mp_face_mesh = mp.solutions.face_mesh

# Create the detector
face_mesh = mp_face_mesh.FaceMesh()

# Draw lines, points and visualize results
mp_drawing = mp.solutions.drawing_utils

# Open the camera
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("Deteccion Facial", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Deteccion Facial", 1200, 800)

while True:
    # Read a frame -> "ret": successful reading | "frame": captured image
    ret, frame = cap.read()
    if not ret:
        break
    
    fatigue_detected = False
    yawn_detected = False
    distraction_detected = False
    vertical_distraction_detected = False

    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        # face_landmarks => +-468 points
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            
            # =====================================
            # EYE DETECTION (EAR)
            # =====================================
            (
                left_eye_coords,
                right_eye_coords,
                left_ear,
                right_ear
            ) = get_eye_data(face_landmarks, w, h)
            
            for point in left_eye_coords:
                cv2.circle(frame, point, 2, (0, 255, 0), -1)

            for point in right_eye_coords:
                cv2.circle(frame, point, 2, (0, 0, 255), -1)
            
            left_valid = left_ear > MIN_EAR
            right_valid = right_ear > MIN_EAR

            if left_valid and right_valid:
                ear = (left_ear + right_ear) / 2.0
            elif left_valid:
                ear = left_ear
            elif right_valid:
                ear = right_ear
            else:
                ear = 1  # avoid false positive
                
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            if ear < EAR_THRESHOLD:
                CLOSED_EYES_FRAMES += 1
                eye_history.append(1)
                cv2.putText(frame, "OJOS CERRADOS", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            else:
                CLOSED_EYES_FRAMES = 0
                eye_history.append(0)
                cv2.putText(frame, "OJOS ABIERTOS", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if CLOSED_EYES_FRAMES >= FATIGUE_FRAMES:
                fatigue_detected = True
                cv2.putText(frame, "FATIGA DETECTADA", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
            perclos = (
                sum(eye_history) / len(eye_history)
                if eye_history
                else 0
            )
            
            cv2.putText(
                frame,
                f"PERCLOS: {perclos:.2f}",
                (30, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2
            )

            # =====================================
            # MOUTH DETECTION (MAR)
            # =====================================
            mouth_coords, mar = get_mouth_data(
                face_landmarks,
                w,
                h
            )
            
            for point in mouth_coords:
                cv2.circle(frame, point, 2, (255, 0, 0), -1)
            
            cv2.putText(frame, f"MAR: {mar:.2f}", (30, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            
            cv2.putText(frame, f"MOUTH FRAMES: {MOUTH_OPEN_FRAMES}", (30, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            if mar > MAR_THRESHOLD:
                MOUTH_OPEN_FRAMES += 1
            else:
                MOUTH_OPEN_FRAMES = 0
            
            if MOUTH_OPEN_FRAMES >= YAWN_FRAMES:
                yawn_detected = True
                cv2.putText(frame, "BOSTEZO DETECTADO", (30, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # =====================================
            # HEAD POSE LANDMARKS
            # =====================================
            pitch, yaw, roll, head_points = calculate_head_pose(
                face_landmarks,
                w,
                h
            )
            
            for point in head_points:
                cv2.circle(frame, point, 4, (0, 255, 255), -1)
            
            if abs(yaw) > DISTRACTION_THRESHOLD:
                DISTRACTION_FRAMES += 1
            else:
                DISTRACTION_FRAMES = 0
                
            if (
                pitch < PITCH_DOWN_THRESHOLD
                or
                pitch > PITCH_UP_THRESHOLD
            ):
                VERTICAL_DISTRACTION_FRAMES += 1
            else:
                VERTICAL_DISTRACTION_FRAMES = 0
                
            cv2.putText(
                frame,
                f"VERT DISTRACTION: {VERTICAL_DISTRACTION_FRAMES}",
                (600, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,0),
                2
            )
                
            cv2.putText(frame,
                f"DISTRACTION FRAMES: {DISTRACTION_FRAMES}",
                (30, 550),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,255),
                2)
            
            if DISTRACTION_FRAMES >= DISTRACTION_LIMIT:
                distraction_detected = True
                cv2.putText(
                    frame,
                    "DISTRACCION DETECTADA",
                    (30, 600),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3
                )
                
            if VERTICAL_DISTRACTION_FRAMES >= VERTICAL_DISTRACTION_LIMIT:
                vertical_distraction_detected = True
                cv2.putText(
                    frame,
                    "DISTRACCION VERTICAL",
                    (600, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3
                )
                
            driver_state = get_driver_state(
                perclos,
                fatigue_detected,
                yawn_detected,
                distraction_detected,
                vertical_distraction_detected
            )
            
            cv2.putText(
                frame,
                f"ESTADO: {driver_state}",
                (700, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )
            
            cv2.putText(frame, f"YAW: {yaw:.2f}", (30, 400),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

            cv2.putText(frame, f"PITCH: {pitch:.2f}", (30, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

            cv2.putText(frame, f"ROLL: {roll:.2f}", (30, 500),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    # Open a window
    cv2.imshow("Deteccion Facial", frame)

    # Escape with "ESC"
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Free up resources
cap.release()
cv2.destroyAllWindows()