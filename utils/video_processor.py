import cv2
from detection.detector import Detector
from threat.threat_score import calculate_threat
from alerts.alert_system import trigger_alert
from alerts.email_alert import send_email
from alerts.incident_logger import log_incident
from behavior.loitering import LoiteringDetector
from tracking.simple_tracker import SimpleTracker
from behavior.behavior_rules import BehaviorRules
from behavior.accident_detector import AccidentDetector

detector = Detector()
loitering_detector = LoiteringDetector()

person_tracker = SimpleTracker()
vehicle_tracker = SimpleTracker()

behavior_rules = BehaviorRules()
accident_detector = AccidentDetector()

def run_system(source):

    cap = cv2.VideoCapture(source)

    email_sent = False

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        objects = detector.detect(frame)

        loitering_people = loitering_detector.check_loitering(objects)

        person_rects = []
        vehicle_rects = []

        for label,x1,y1,x2,y2 in objects:

            if label == "person":
                person_rects.append([x1,y1,x2,y2])

            if label in ["car","truck","bus","motorbike"]:
                vehicle_rects.append([x1,y1,x2,y2])

        tracked_people = person_tracker.update(person_rects)
        tracked_vehicles = vehicle_tracker.update(vehicle_rects)

        fights, aggression, falls = behavior_rules.check_behaviors(tracked_people)

        collisions = accident_detector.detect_collision(tracked_vehicles)

        # draw detections
        for label,x1,y1,x2,y2 in objects:

            color = (0,255,0)

            if label in ["knife","scissors","baseball bat"]:
                color = (0,0,255)

            for lp in loitering_people:
                if (label,x1,y1,x2,y2) == lp:
                    color = (0,165,255)
                    cv2.putText(frame,"LOITERING",
                                (x1,y1-30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,(0,165,255),2)

            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)

            cv2.putText(frame,label,
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2)

        # draw tracked people
        for x1,y1,x2,y2,person_id in tracked_people:

            text = f"ID {person_id}"
            color = (0,255,0)

            if person_id in falls:
                text += " FALL"
                color = (255,0,0)

            elif person_id in aggression:
                text += " AGGRESSION"
                color = (0,0,255)

            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)

            cv2.putText(frame,text,
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

        # draw tracked vehicles
        for x1,y1,x2,y2,vid in tracked_vehicles:

            color = (255,255,0)

            for c in collisions:
                if vid in c:
                    color = (0,0,255)

                    cv2.putText(frame,"ACCIDENT",
                                (x1,y1-40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,(0,0,255),2)

            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)

            cv2.putText(frame,f"V-ID {vid}",
                        (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

        # threat score
        score = calculate_threat(objects)

        if len(loitering_people) > 0:
            score += 40
            log_incident("LOITERING", score)

        if len(fights) > 0:
            score += 40
            log_incident("FIGHT", score)

        if len(aggression) > 0:
            score += 30
            log_incident("AGGRESSION", score)

        if len(falls) > 0:
            score += 25
            log_incident("FALL", score)

        if len(collisions) > 0:
            score += 60
            log_incident("ACCIDENT", score)

        cv2.putText(frame,
                    f"Threat Score: {score}",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3)

        # local alert
        if score > 20:
            trigger_alert(frame,score)

        # gmail alert
        if score > 80 and not email_sent:
            send_email(frame,score)
            log_incident("EMAIL ALERT SENT", score)
            email_sent = True

        cv2.imshow("ThreatSense AI",frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()