import math

class AccidentDetector:

    def detect_collision(self, vehicles):

        collisions = []

        for i in range(len(vehicles)):
            for j in range(i+1, len(vehicles)):

                x1,y1,x2,y2,id1 = vehicles[i]
                a1,b1,a2,b2,id2 = vehicles[j]

                # check bbox overlap
                if x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1:
                    collisions.append((id1,id2))

        return collisions