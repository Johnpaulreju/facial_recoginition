# # face_tracker.py
# # Purpose: Detects head tilt, eye closure, and forward tilt for game control

# import cv2                  # OpenCV for webcam and image processing
# import dlib                 # Dlib for facial landmark detection
# import numpy as np          # Numpy for calculations

# # Initialize Dlib's face detector and landmark predictor
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# # Eye landmarks (left eye: 36-41, right eye: 42-47)
# LEFT_EYE_POINTS = list(range(36, 42))
# RIGHT_EYE_POINTS = list(range(42, 48))

# # Eye Aspect Ratio (EAR) threshold for detecting closed eyes
# EAR_THRESHOLD = 0.25  # Adjust this based on testing
# EAR_CONSECUTIVE_FRAMES = 3  # Number of frames eyes must be closed to trigger stop

# # Function to calculate Eye Aspect Ratio (EAR)
# def eye_aspect_ratio(eye_points, landmarks):
#     # Compute the distances between vertical eye landmarks
#     A = np.linalg.norm([landmarks.part(eye_points[1]).x - landmarks.part(eye_points[5]).x,
#                         landmarks.part(eye_points[1]).y - landmarks.part(eye_points[5]).y])
#     B = np.linalg.norm([landmarks.part(eye_points[2]).x - landmarks.part(eye_points[4]).x,
#                         landmarks.part(eye_points[2]).y - landmarks.part(eye_points[4]).y])
#     # Compute the distance between horizontal eye landmarks
#     C = np.linalg.norm([landmarks.part(eye_points[0]).x - landmarks.part(eye_points[3]).x,
#                         landmarks.part(eye_points[0]).y - landmarks.part(eye_points[3]).y])
#     # Compute EAR
#     ear = (A + B) / (2.0 * C)
#     return ear

# # Function to get head tilt, eye state, and forward tilt
# def get_face_controls():
#     # Open webcam (0 is default camera)
#     cap = cv2.VideoCapture(0)
#     closed_eyes_counter = 0  # Counter for consecutive frames with closed eyes
#     is_game_paused = False   # Track if game is paused due to eye closure
#     prev_pitch = 0           # Track previous pitch for smoothing

#     while True:
#         ret, frame = cap.read()  # Capture frame from webcam
#         if not ret:
#             print("Error: Could not open webcam.")
#             break
        
#         # Convert frame to grayscale for faster processing
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
#         # Detect faces in the frame
#         faces = detector(gray)
        
#         tilt = "center"  # Default tilt
#         eyes_closed = False
#         forward_tilt = False

#         if len(faces) > 0:  # If at least one face is detected
#             # Get landmarks for the first face
#             landmarks = predictor(gray, faces[0])
            
#             # Calculate head tilt using nose position (landmark 30)
#             nose_x = landmarks.part(30).x
#             frame_width = frame.shape[1]
#             tilt_position = nose_x / frame_width
#             if tilt_position < 0.4:
#                 tilt = "left"
#             elif tilt_position > 0.6:
#                 tilt = "right"
#             else:
#                 tilt = "center"
            
#             # Calculate Eye Aspect Ratio for both eyes
#             left_ear = eye_aspect_ratio(LEFT_EYE_POINTS, landmarks)
#             right_ear = eye_aspect_ratio(RIGHT_EYE_POINTS, landmarks)
#             avg_ear = (left_ear + right_ear) / 2.0
            
#             # Check if eyes are closed
#             if avg_ear < EAR_THRESHOLD:
#                 closed_eyes_counter += 1
#                 if closed_eyes_counter >= EAR_CONSECUTIVE_FRAMES:
#                     eyes_closed = True
#                     is_game_paused = True
#             else:
#                 closed_eyes_counter = 0
#                 eyes_closed = False
#                 is_game_paused = False
            
#             # Calculate forward tilt (pitch) using eye and nose positions
#             left_eye_center = np.mean([(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_POINTS], axis=0)
#             right_eye_center = np.mean([(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_POINTS], axis=0)
#             eye_center_y = (left_eye_center[1] + right_eye_center[1]) / 2.0
#             nose_y = landmarks.part(30).y
#             pitch = nose_y - eye_center_y  # Positive pitch = head tilted forward
            
#             # Smooth pitch to avoid jitter
#             pitch = 0.7 * prev_pitch + 0.3 * pitch
#             prev_pitch = pitch
            
#             # Detect forward tilt (threshold may need adjustment)
#             if pitch > 20:  # Adjust this threshold based on testing
#                 forward_tilt = True
        
#         # Yield the control states
#         yield {
#             "tilt": tilt,
#             "eyes_closed": eyes_closed,
#             "forward_tilt": forward_tilt
#         }

# # Cleanup function to release resources
# def cleanup(cap):
#     cap.release()
#     cv2.destroyAllWindows()

# # Run the tracker if this file is executed directly (for testing)
# if __name__ == "__main__":
#     cap = cv2.VideoCapture(0)
#     face_controls = get_face_controls()
#     for control in face_controls:
#         print(control)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cleanup(cap)





# face_tracker.py
# Purpose: Detects head tilt, eye closure, and forward tilt for game control, with webcam display

import cv2                  # OpenCV for webcam and image processing
import dlib                 # Dlib for facial landmark detection
import numpy as np          # Numpy for calculations

# Initialize Dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Eye landmarks (left eye: 36-41, right eye: 42-47)
LEFT_EYE_POINTS = list(range(36, 42))
RIGHT_EYE_POINTS = list(range(42, 48))

# Eye Aspect Ratio (EAR) threshold for detecting closed eyes
EAR_THRESHOLD = 0.25  # Adjust this based on testing
EAR_CONSECUTIVE_FRAMES = 3  # Number of frames eyes must be closed to trigger stop

# Forward tilt threshold
FORWARD_TILT_THRESHOLD = 20  # Lowered for easier detection

# Function to calculate Eye Aspect Ratio (EAR)
def eye_aspect_ratio(eye_points, landmarks):
    A = np.linalg.norm([landmarks.part(eye_points[1]).x - landmarks.part(eye_points[5]).x,
                        landmarks.part(eye_points[1]).y - landmarks.part(eye_points[5]).y])
    B = np.linalg.norm([landmarks.part(eye_points[2]).x - landmarks.part(eye_points[4]).x,
                        landmarks.part(eye_points[2]).y - landmarks.part(eye_points[4]).y])
    C = np.linalg.norm([landmarks.part(eye_points[0]).x - landmarks.part(eye_points[3]).x,
                        landmarks.part(eye_points[0]).y - landmarks.part(eye_points[3]).y])
    ear = (A + B) / (2.0 * C)
    return ear

# Function to get head tilt, eye state, and forward tilt
def get_face_controls():
    # Open webcam (0 is default camera)
    cap = cv2.VideoCapture(0)
    closed_eyes_counter = 0  # Counter for consecutive frames with closed eyes
    is_game_paused = False   # Track if game is paused due to eye closure
    prev_pitch = 0           # Track previous pitch for smoothing
    baseline_pitch = None    # Baseline pitch for forward tilt calibration
    calibration_frames = 60  # Number of frames to calibrate baseline pitch

    # Set webcam resolution to reduce lag
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()  # Capture frame from webcam
        if not ret:
            print("Error: Could not open webcam.")
            break
        
        # Convert frame to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = detector(gray)
        
        tilt = "center"  # Default tilt
        eyes_closed = False
        forward_tilt = False
        pitch = 0        # Initialize pitch for display

        if len(faces) > 0:  # If at least one face is detected
            # Get landmarks for the first face
            landmarks = predictor(gray, faces[0])
            
            # Draw all 68 landmarks as circles
            for i in range(68):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Green dots, radius 2
            
            # Calculate head tilt using nose position (landmark 30)
            nose_x = landmarks.part(30).x
            frame_width = frame.shape[1]
            tilt_position = nose_x / frame_width
            if tilt_position < 0.4:
                tilt = "left"
            elif tilt_position > 0.6:
                tilt = "right"
            else:
                tilt = "center"
            
            # Calculate Eye Aspect Ratio for both eyes
            left_ear = eye_aspect_ratio(LEFT_EYE_POINTS, landmarks)
            right_ear = eye_aspect_ratio(RIGHT_EYE_POINTS, landmarks)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Check if eyes are closed
            if avg_ear < EAR_THRESHOLD:
                closed_eyes_counter += 1
                if closed_eyes_counter >= EAR_CONSECUTIVE_FRAMES:
                    eyes_closed = True
                    is_game_paused = True
            else:
                closed_eyes_counter = 0
                eyes_closed = False
                is_game_paused = False
            
            # Calculate forward tilt (pitch) using eye and nose positions
            left_eye_center = np.mean([(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_POINTS], axis=0)
            right_eye_center = np.mean([(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_POINTS], axis=0)
            eye_center_y = (left_eye_center[1] + right_eye_center[1]) / 2.0
            nose_y = landmarks.part(30).y
            pitch = nose_y - eye_center_y  # Positive pitch = head tilted forward
            
            # Smooth pitch to avoid jitter (less smoothing for more responsiveness)
            pitch = 0.5 * prev_pitch + 0.5 * pitch
            prev_pitch = pitch
            
            # Calibrate baseline pitch for the first few frames
            if calibration_frames > 0:
                if baseline_pitch is None:
                    baseline_pitch = pitch
                else:
                    baseline_pitch = 0.9 * baseline_pitch + 0.1 * pitch
                calibration_frames -= 1
            else:
                # Detect forward tilt relative to baseline
                if pitch - baseline_pitch > FORWARD_TILT_THRESHOLD:
                    forward_tilt = True
        
        # Display debug information on the webcam feed
        cv2.putText(frame, f"Tilt: {tilt}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Eyes Closed: {eyes_closed}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Forward Tilt: {forward_tilt}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Pitch: {pitch:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # Fix: Properly handle None case for baseline_pitch
        baseline_text = f"Baseline: {baseline_pitch:.2f}" if baseline_pitch is not None else "Baseline: Calibrating"
        cv2.putText(frame, baseline_text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display the webcam feed
        cv2.imshow("Face Tracker", frame)
        
        # Yield the control states
        yield {
            "tilt": tilt,
            "eyes_closed": eyes_closed,
            "forward_tilt": forward_tilt
        }

# Cleanup function to release resources
def cleanup(cap):
    cap.release()
    cv2.destroyAllWindows()

# Run the tracker if this file is executed directly (for testing)
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    face_controls = get_face_controls()
    for control in face_controls:
        print(control)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cleanup(cap)