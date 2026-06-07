def get_driver_state(
    perclos,
    fatigue_detected,
    yawn_detected,
    distraction_detected,
    vertical_distraction_detected
):
    
    if (
        fatigue_detected
        and
        distraction_detected
    ):
        return "ALTO RIESGO"

    if (
        fatigue_detected
        or
        perclos > 0.40
        or
        yawn_detected
    ):
        return "FATIGADO"

    if (
        distraction_detected
        or
        vertical_distraction_detected
    ):
        return "DISTRAIDO"

    return "NORMAL"