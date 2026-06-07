from utils.geometry import calculate_mar

MOUTH = [13, 14, 78, 308]

def get_mouth_data(face_landmarks, w, h):

    mouth_coords = []

    for idx in MOUTH:
        landmark = face_landmarks.landmark[idx]

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        mouth_coords.append((x, y))

    mar = calculate_mar(mouth_coords)

    return mouth_coords, mar