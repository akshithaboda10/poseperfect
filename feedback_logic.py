def get_feedback(landmarks):
    feedback = []

    if not landmarks:
        return ["No landmarks detected."]

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_elbow = landmarks[13]
    left_wrist = landmarks[15]
    left_knee = landmarks[25]

    # Shoulders level
    shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
    if shoulder_diff > 0.05:
        feedback.append("Keep your shoulders level.")

    # Upright posture
    hip_diff = abs(left_hip.y - right_hip.y)
    if hip_diff > 0.05:
        feedback.append("Stand upright.")

    # Back alignment
    back_alignment = abs(left_shoulder.x - left_hip.x)
    if back_alignment > 0.05:
        feedback.append("Align your back straight.")

    # Elbow and wrist alignment
    elbow_wrist_dist = abs(left_elbow.y - left_wrist.y)
    if elbow_wrist_dist > 0.2:
        feedback.append("Keep your arm straight.")

    # Knee check (optional for sitting/leg pose)
    if left_knee.y < left_hip.y:
        feedback.append("Keep your knee below hip level.")

    if not feedback:
        feedback.append("Great posture! 🎉")

    return feedback
