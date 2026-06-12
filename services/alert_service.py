import winsound
import time

LAST_ALERT_TIME = 0
ALERT_COOLDOWN = 5

def play_alert():

    global LAST_ALERT_TIME

    current_time = time.time()

    if (
        current_time - LAST_ALERT_TIME
        < ALERT_COOLDOWN
    ):
        return

    winsound.Beep(
        2000,
        500
    )

    LAST_ALERT_TIME = current_time