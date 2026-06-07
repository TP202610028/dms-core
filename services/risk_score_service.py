def calculate_risk_score(
    perclos,
    fatigue_detected,
    yawn_detected,
    distraction_detected,
    vertical_distraction_detected
):
    score = 0

    if fatigue_detected:
        score += 40

    if yawn_detected:
        score += 15

    if distraction_detected:
        score += 20

    if vertical_distraction_detected:
        score += 15

    if perclos > 0.30:
        score += 10
        
    

    return min(score, 100)

def get_risk_level(score):

    if score < 20:
        return "BAJO"

    if score < 50:
        return "MEDIO"

    if score < 80:
        return "ALTO"

    return "CRITICO"