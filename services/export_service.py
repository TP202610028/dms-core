import json
import os
from datetime import datetime

def save_session(session_metrics):

    os.makedirs(
        "data/sessions",
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "%Y%m%d_%H%M%S.json"
    )

    filepath = f"data/sessions/{filename}"

    data = {
        "duration_seconds":
            session_metrics.duration_seconds(),

        "yawns":
            session_metrics.yawns,

        "fatigue_events":
            session_metrics.fatigue_events,

        "microsleeps":
            session_metrics.microsleeps,

        "distractions":
            session_metrics.distractions,

        "vertical_distractions":
            session_metrics.vertical_distractions,

        "face_missing_events":
            session_metrics.face_missing_events,

        "average_perclos":
            session_metrics.average_perclos(),

        "average_risk":
            session_metrics.average_risk(),

        "max_risk":
            session_metrics.max_risk()
    }

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print(f"\nSesion guardada: {filepath}")