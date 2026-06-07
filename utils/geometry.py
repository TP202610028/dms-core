import numpy as np

def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_ear(eye):
    p1, p2, p3, p4, p5, p6 = eye

    vertical1 = euclidean_distance(p2, p6)
    vertical2 = euclidean_distance(p3, p5)
    horizontal = euclidean_distance(p1, p4)
    
    if horizontal == 0:
        return 0

    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

def calculate_mar(mouth):
    upper_lip, lower_lip, left_corner, right_corner = mouth

    vertical = euclidean_distance(upper_lip, lower_lip)
    horizontal = euclidean_distance(left_corner, right_corner)
    
    if horizontal == 0:
        return 0

    mar = vertical / horizontal
    return mar