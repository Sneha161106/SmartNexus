def calculate_threat(objects):

    score = 0

    for obj in objects:

        label = obj[0]

        if label == "person":
            score += 5

        elif label == "knife":
            score += 70

        elif label == "scissors":
            score += 60

        elif label == "baseball bat":
            score += 50

    return score