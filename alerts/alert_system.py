import cv2
import time

def trigger_alert(frame, score):

    print("⚠ THREAT ALERT! Score:", score)

    filename = f"clips/alert_{int(time.time())}.jpg"

    cv2.imwrite(filename, frame)