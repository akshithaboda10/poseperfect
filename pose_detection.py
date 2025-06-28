import cv2
import mediapipe as mp
from feedback_logic import get_feedback

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_pose():
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            # Convert to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            # Convert back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Feedback overlay
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                feedback = get_feedback(landmarks)

                # Display feedback
                y0 = 30
                for i, line in enumerate(feedback):
                    y = y0 + i * 30
                    cv2.putText(image, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('PosePerfect - Posture Feedback', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
