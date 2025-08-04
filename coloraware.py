import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cv2.namedWindow("ColorAware")
cv2.moveWindow("ColorAware", 100, 100)



while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Webcam feed not captured!")

        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red HSV range
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask_red1 = cv2.inRange(hsv, lower_red, upper_red)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask_red1, mask_red2)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    if cv2.contourArea(cnt) > 1000:
        x, y, w, h = cv2.boundingRect(cnt)
        center_x, center_y = x + w // 2, y + h // 2
        cv2.arrowedLine(frame, (10, 30), (center_x, center_y), (255, 255, 255), 2)
        cv2.putText(frame, "Red", (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        break  # Only one label for now

    # Define green HSV range
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    frame[green_mask > 0] = [0, 255, 0]

    # Define HSV range for blue
    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Define HSV range for yellow
    lower_yellow = np.array([22, 93, 100])
    upper_yellow = np.array([32, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Create masks for red
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Apply masks and overlays
    frame[red_mask > 0] = [0, 0, 255]        # Red overlay
    frame[green_mask > 0] = [0, 255, 0]      # Green overlay
    frame[blue_mask > 0] = [255, 0, 0]       # Blue overlay
    frame[yellow_mask > 0] = [0, 255, 255]   # Yellow overlay

    # # Add labels 
    if np.any(red_mask > 0):
        cv2.putText(frame, "Red Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if np.any(green_mask > 0):
        cv2.putText(frame, "Green Detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    if np.any(blue_mask > 0):
        cv2.putText(frame, "Blue Detected", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    if np.any(yellow_mask > 0):
        cv2.putText(frame, "Yellow Detected", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    
    # Create red pattern (diagonal stripes)
    pattern = np.zeros_like(frame)
    for i in range(0, pattern.shape[0], 10):
        cv2.line(pattern, (0, i), (pattern.shape[1], i), (0, 0, 255), 1)

# Apply pattern only to red_mask area
pattern_mask = cv2.bitwise_and(pattern, pattern, mask=red_mask)
frame = cv2.addWeighted(frame, 1, pattern_mask, 0.5, 0)

# Count how many pixels are detected
red_count = cv2.countNonZero(red_mask)
green_count = cv2.countNonZero(green_mask)
blue_count = cv2.countNonZero(blue_mask)
yellow_count = cv2.countNonZero(yellow_mask)

# Set a threshold (number of pixels) to filter out noise
threshold = 500

y_position = 30  # Starting Y position for text

if red_count > threshold:
        cv2.putText(frame, "Red Detected", (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
y_position += 40

if green_count > threshold:
        cv2.putText(frame, "Green Detected", (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
y_position += 40

if blue_count > threshold:
        cv2.putText(frame, "Blue Detected", (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
y_position += 40

if yellow_count > threshold:
        cv2.putText(frame, "Yellow Detected", (10, y_position), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    

# Analysis Panel Box
cv2.rectangle(frame, (frame.shape[1] - 220, 10), (frame.shape[1] - 10, 180), (50, 50, 50), -1)
cv2.putText(frame, "Analysis", (frame.shape[1] - 200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

y = 70
if red_count > threshold:
    cv2.putText(frame, "Red: Detected", (frame.shape[1] - 200, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    y += 30
if green_count > threshold:
    cv2.putText(frame, "Green: Detected", (frame.shape[1] - 200, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    y += 30
if blue_count > threshold:
    cv2.putText(frame, "Blue: Detected", (frame.shape[1] - 200, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    y += 30
if yellow_count > threshold:
    cv2.putText(frame, "Yellow: Detected", (frame.shape[1] - 200, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)


cv2.imshow("ColorAware", frame)
    

if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
                

    cap.release()
cv2.destroyAllWindows()
