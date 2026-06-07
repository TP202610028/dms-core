import numpy as np

def calibrate_ear(ear_samples):
    mean_ear = np.mean(ear_samples)

    threshold = mean_ear * 0.7

    return threshold

def calibrate_mar(mar_samples):
    mean_mar = np.mean(mar_samples)

    threshold = mean_mar * 2.5

    return threshold