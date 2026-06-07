from utils.geometry import calculate_ear

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def get_eye_data(face_landmarks, w, h):

    left_eye_coords = []

    for idx in LEFT_EYE:
        landmark = face_landmarks.landmark[idx]
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        left_eye_coords.append((x, y))

    right_eye_coords = []

    for idx in RIGHT_EYE:
        landmark = face_landmarks.landmark[idx]
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        right_eye_coords.append((x, y))

    left_ear = calculate_ear(left_eye_coords)
    right_ear = calculate_ear(right_eye_coords)

    return (
        left_eye_coords,
        right_eye_coords,
        left_ear,
        right_ear
    )