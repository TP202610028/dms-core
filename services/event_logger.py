from datetime import datetime

def log_event(event):
    with open("events.log", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {event}\n")