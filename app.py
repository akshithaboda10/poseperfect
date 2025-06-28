import csv
from datetime import datetime
import cv2
import mediapipe as mp
from feedback_logic import get_feedback
from PIL import ImageFont, ImageDraw, Image
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Load a TTF font (can be customized)
try:
    font_path = "arial.ttf"  # Adjust if using a different font or OS
    font = ImageFont.truetype(font_path, 22)
except:
    font = ImageFont.load_default()

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue

        # Convert color and make detection
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        # Convert back and draw landmarks
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmarks = results.pose_landmarks.landmark
            feedback = get_feedback(landmarks)

            # Save feedback to CSV
            with open("feedback_log.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for line in feedback:
                    writer.writerow([timestamp, line])

            # Draw background + text using Pillow for better font rendering
            img_pil = Image.fromarray(image)
            draw = ImageDraw.Draw(img_pil)

            box_x, box_y = 10, 10
            line_spacing = 28
            box_width = 460
            box_height = 20 + (len(feedback) + 1) * line_spacing  # dynamic height

            # Black rectangle
            draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=(0, 0, 0, 180))

            # Title
            draw.text((box_x + 10, box_y + 5), "Posture Feedback", font=font, fill=(255, 255, 0))

            # Feedback lines
            for i, msg in enumerate(feedback):
                draw.text((box_x + 10, box_y + 35 + i * line_spacing), msg, font=font, fill=(255, 255, 255))

            image = np.array(img_pil)

        # Show the frame
        cv2.imshow('Pose Feedback', image)

        # Quit with 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
