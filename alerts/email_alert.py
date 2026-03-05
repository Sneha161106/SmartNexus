import smtplib
from email.message import EmailMessage
import cv2

def send_email(frame, score):

    sender_email = "pranavkhaire777@gmail.com"
    receiver_email = "sanskarshitole2005@gmail.com"
    app_password = "acfy bbsp skge lvji"

    # save frame image
    image_path = "incident.jpg"
    cv2.imwrite(image_path, frame)

    msg = EmailMessage()
    msg["Subject"] = f"⚠ Threat Alert Score: {score}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(f"Threat detected with score {score}")

    with open(image_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="image",
            subtype="jpeg",
            filename="incident.jpg"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    print("Email alert sent!")