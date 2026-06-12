import cv2
import os
from datetime import datetime

def save_event_frame(frame, event_name):

    os.makedirs(
        "data/events",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"data/events/"
        f"{event_name}_{timestamp}.jpg"
    )

    cv2.imwrite(
        filename,
        frame
    )

    print(
        f"Evento guardado: {filename}"
    )