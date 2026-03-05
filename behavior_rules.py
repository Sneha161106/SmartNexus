import math

class BehaviorRules:

    def __init__(self):
        self.prev_positions = {}

    def check_behaviors(self, tracked_people):

        fights = []
        aggression = []
        falls = []

        # check fall + aggression
        for x1,y1,x2,y2,person_id in tracked_people:

            width = x2 - x1
            height = y2 - y1

            # FALL DETECTION
            if width > height:
                falls.append(person_id)

            # AGGRESSION (speed check)
            cx = (x1+x2)//2
            cy = (y1+y2)//2

            if person_id in self.prev_positions:

                px,py = self.prev_positions[person_id]

                dist = math.hypot(cx-px, cy-py)

                if dist > 40:
                    aggression.append(person_id)

            self.prev_positions[person_id] = (cx,cy)

        # FIGHT DETECTION (bbox overlap)
        for i in range(len(tracked_people)):
            for j in range(i+1,len(tracked_people)):

                x1,y1,x2,y2,id1 = tracked_people[i]
                a1,b1,a2,b2,id2 = tracked_people[j]

                if x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1:
                    fights.append((id1,id2))

        return fights, aggression, falls