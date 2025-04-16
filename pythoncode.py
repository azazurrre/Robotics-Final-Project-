import cv2
import torch
import serial
import time
from collections import deque

# Connect to Arduino (adjust COM port if needed)
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

def ard():
    laser_on = False
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()

    # Open webcam (change to 0 if needed)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open webcam.")
        return

    print("Running person tracking. Press 'q' to quit.")

    # Get frame dimensions
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    center_x = frame_width // 2
    center_y = frame_height // 2

    # Buffer to hold previous detections for smoothing
    detection_buffer = deque(maxlen=5)
    prev_step_x = 0
    prev_step_y = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame.")
            break
            #continue

        results = model(frame)
        detections = results.xyxy[0]

        person_found = False
        for det in detections:
            x1, y1, x2, y2, conf, cls = det.tolist()
            if int(cls) == 0 and conf > 0.2:
                person_found = True
                person_center_x = int((x1 + x2) / 2)
                person_center_y = int((y1 + y2) / 2)
                detection_buffer.append((person_center_x, person_center_y))
                break

        # Only act if buffer has valid data
        if len(detection_buffer) > 0:
            avg_x = int(sum(p[0] for p in detection_buffer) / len(detection_buffer))
            avg_y = int(sum(p[1] for p in detection_buffer) / len(detection_buffer))

            temp_x = avg_x - center_x
            temp_y = avg_y - center_y

            step_x = 0
            step_y = 0

            # Move if offset is large enough
            if abs(temp_x) > 5:
                step_x = int(temp_x * 0.05)
                step_x = max(min(step_x, 5), -5)
            
            else:
                arduino.write(b"H\n")

            if abs(temp_y) > 5:
                step_y = int(temp_y * 0.05)
                step_y = max(min(step_y, 5), -5)
                #arduino.write(b"L\n")
            

            # Only send if step changed
            if step_x != prev_step_x or step_y != prev_step_y:
                arduino.write(f"{step_x},{step_y}\n".encode())
                prev_step_x = step_x
                prev_step_y = step_y
                arduino.write(b"L\n")
            # else:
            #     arduino.write(b"H\n")

            # else:
            #     print("LEWQLELQLEWQLELWQLELWQELWQLEWQLEWLQELQWELQWLEWQL")

            # Draw tracking dot
            cv2.circle(frame, (avg_x, avg_y), 5, (0, 0, 255), -1)

        # Draw frame center
        cv2.line(frame, (center_x, 0), (center_x, frame_height), (255, 0, 0), 1)
        cv2.line(frame, (0, center_y), (frame_width, center_y), (255, 0, 0), 1)

        cv2.imshow("Tracking", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ard()
