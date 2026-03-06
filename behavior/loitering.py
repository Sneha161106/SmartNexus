import time

class LoiteringDetector:

    def __init__(self):
        self.person_times = {}

    def check_loitering(self, objects):

        loitering_ids = []
        current_time = time.time()

        for label, x1, y1, x2, y2 in objects:

            if label == "person":

                center = ((x1+x2)//2,(y1+y2)//2)

                key = str(center)

                if key not in self.person_times:
                    self.person_times[key] = current_time
                else:
                    duration = current_time - self.person_times[key]

                    if duration > 10:   # seconds
                        loitering_ids.append((label,x1,y1,x2,y2))

        return loitering_ids