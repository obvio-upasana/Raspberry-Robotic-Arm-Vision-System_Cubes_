"""
OUTPUT:
- White cube  -> 0
- Grey cube   -> 1

Displays:
- Bounding box
- Center coordinates
- Label (0 or 1)
- Motion tracking in camera feed

Controls:
    q = Quit
    d = Toggle debug contours

Install:
    pip install opencv-python numpy
===========================================================================
"""

import cv2
import numpy as np
import time

# ==========================================================================
# CAMERA SETTINGS
# ==========================================================================

CAMERA_INDEX = 1


FRAME_WIDTH = 640
FRAME_HEIGHT = 480

PROCESS_WIDTH = 320
PROCESS_HEIGHT = 240

FPS = 30

# ==========================================================================
# HSV COLOR RANGES
# ==========================================================================

# WHITE
WHITE_LOWER = np.array([0, 0, 180], dtype=np.uint8)
WHITE_UPPER = np.array([179, 60, 255], dtype=np.uint8)

# GREY
GREY_LOWER = np.array([0, 0, 70], dtype=np.uint8)
GREY_UPPER = np.array([179, 70, 170], dtype=np.uint8)

# ==========================================================================
# DETECTION SETTINGS
# ==========================================================================

MIN_AREA = 700
MAX_AREA = 30000

SQUARE_RATIO_MIN = 0.75
SQUARE_RATIO_MAX = 1.25

MORPH_SIZE = 5

SHOW_DEBUG = False

# ==========================================================================
# COLORS
# ==========================================================================

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
RED = (0, 0, 255)

FONT = cv2.FONT_HERSHEY_SIMPLEX

# ==========================================================================
# CAMERA INIT
# ==========================================================================

cap = cv2.VideoCapture(CAMERA_INDEX)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)

if not cap.isOpened():
    print("ERROR: Camera not found")
    exit()

# Warmup
for _ in range(10):
    cap.read()

print("Camera started")

# ==========================================================================
# HELPER FUNCTIONS
# ==========================================================================

kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (MORPH_SIZE, MORPH_SIZE)
)


def build_mask(hsv, lower, upper):
    """
    Create clean binary mask
    """

    mask = cv2.inRange(hsv, lower, upper)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    return mask


def detect_squares(mask, label, draw_color, frame, scale_x, scale_y):
    """
    Detect square-like contours
    """

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detections = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < MIN_AREA or area > MAX_AREA:
            continue

        # Polygon approximation
        peri = cv2.arcLength(cnt, True)

        approx = cv2.approxPolyDP(
            cnt,
            0.04 * peri,
            True
        )

        # Must be square-like
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)

        aspect_ratio = w / float(h)

        if not (SQUARE_RATIO_MIN <= aspect_ratio <= SQUARE_RATIO_MAX):
            continue

        # Scale back to original resolution
        x = int(x * scale_x)
        y = int(y * scale_y)
        w = int(w * scale_x)
        h = int(h * scale_y)

        cx = x + w // 2
        cy = y + h // 2

        detections.append((label, cx, cy))

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            draw_color,
            2
        )

        # Center point
        cv2.circle(
            frame,
            (cx, cy),
            5,
            RED,
            -1
        )

        # Display text
        text = f"{label} ({cx},{cy})"

        cv2.putText(
            frame,
            text,
            (x, y - 10),
            FONT,
            0.6,
            draw_color,
            2
        )

        # Debug contour
        if SHOW_DEBUG:
            scaled = approx.copy().astype(np.float32)

            scaled[:, :, 0] *= scale_x
            scaled[:, :, 1] *= scale_y

            scaled = scaled.astype(np.int32)

            cv2.drawContours(
                frame,
                [scaled],
                -1,
                GREEN,
                1
            )

    return detections


# ==========================================================================
# MAIN LOOP
# ==========================================================================

frame_count = 0
fps_timer = time.time()
fps_value = 0

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera frame error")
        break

    frame_count += 1

    # Resize for faster processing
    small = cv2.resize(
        frame,
        (PROCESS_WIDTH, PROCESS_HEIGHT)
    )

    hsv = cv2.cvtColor(
        small,
        cv2.COLOR_BGR2HSV
    )

    hsv = cv2.GaussianBlur(
        hsv,
        (5, 5),
        0
    )

    scale_x = FRAME_WIDTH / PROCESS_WIDTH
    scale_y = FRAME_HEIGHT / PROCESS_HEIGHT

    # ----------------------------------------------------------------------
    # Build masks
    # ----------------------------------------------------------------------

    white_mask = build_mask(
        hsv,
        WHITE_LOWER,
        WHITE_UPPER
    )

    grey_mask = build_mask(
        hsv,
        GREY_LOWER,
        GREY_UPPER
    )

    # ----------------------------------------------------------------------
    # Detect objects
    # ----------------------------------------------------------------------

    detections = []

    # WHITE -> 0
    detections += detect_squares(
        white_mask,
        0,
        WHITE,
        frame,
        scale_x,
        scale_y
    )

    # GREY -> 1
    detections += detect_squares(
        grey_mask,
        1,
        GREY,
        frame,
        scale_x,
        scale_y
    )

    # ----------------------------------------------------------------------
    # Print detections
    # ----------------------------------------------------------------------

    for label, cx, cy in detections:
        print(f"Detected: {label} at X={cx}, Y={cy}")

    # ----------------------------------------------------------------------
    # FPS
    # ----------------------------------------------------------------------

    if frame_count >= 30:
        now = time.time()

        fps_value = frame_count / (now - fps_timer)

        fps_timer = now
        frame_count = 0

    cv2.putText(
        frame,
        f"FPS: {fps_value:.1f}",
        (10, 30),
        FONT,
        0.7,
        GREEN,
        2
    )

    cv2.putText(
        frame,
        "White=0  Grey=1",
        (10, 60),
        FONT,
        0.7,
        GREEN,
        2
    )

    # ----------------------------------------------------------------------
    # SHOW FRAME
    # ----------------------------------------------------------------------

    cv2.imshow("Cube Detector", frame)

    # Optional masks for debugging
    # cv2.imshow("White Mask", white_mask)
    # cv2.imshow("Grey Mask", grey_mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('d'):
        SHOW_DEBUG = not SHOW_DEBUG

# ==========================================================================
# CLEANUP
# ==========================================================================

cap.release()
cv2.destroyAllWindows()

print("Program ended")
