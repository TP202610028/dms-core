import numpy as np

def calibrate_ear(ear_samples):
    mean_ear = np.mean(ear_samples)

    threshold = mean_ear * 0.7

    return threshold

def calibrate_mar(mar_samples):
    mean_mar = np.mean(mar_samples)
    std_mar = np.std(mar_samples)

    threshold = max(
        mean_mar + (3 * std_mar),
        0.15
    )

    return threshold