def detect_microsleep(
    closed_eye_frames,
    microsleep_limit
):
    return closed_eye_frames >= microsleep_limit