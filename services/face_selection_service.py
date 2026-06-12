def get_face_area(face_landmarks, width, height):

    xs = []
    ys = []

    for landmark in face_landmarks.landmark:
        xs.append(int(landmark.x * width))
        ys.append(int(landmark.y * height))

    face_width = max(xs) - min(xs)
    face_height = max(ys) - min(ys)

    return face_width * face_height

def get_primary_face(faces, width, height):

    largest_face = None
    largest_area = 0

    for face in faces:

        area = get_face_area(
            face,
            width,
            height
        )

        if area > largest_area:
            largest_area = area
            largest_face = face

    return largest_face