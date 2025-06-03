import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import cProfile

from mediapipe.python.solutions.drawing_utils import cv2

from mouse import Controller, Mouse
from landmarker import LandMarker
from testing import check_falseflag_stationary_movement

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

cam = cv.VideoCapture(0)
live_recording_size = (round(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), round(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
landmarker = LandMarker(live_recording_size)
mouse = Mouse()
controller = Controller()

def handle_mouse(frame: np.ndarray) -> np.ndarray:
    has_clicked = landmarker.has_ordered(0.04, "index")
    if has_clicked:
        mouse.click()
    else:
        mouse.release_click()

    on_mouse, wrist = landmarker.on_mouse(0.015, 0.01)
    # if on_mouse:
    #     mouse.move(wrist, 10000)

    if has_clicked and on_mouse: 
        frame = landmarker.label_hand("Dragging", frame)
    elif has_clicked: 
        frame = landmarker.label_hand("Holding left click", frame)
    elif on_mouse: 
        frame = landmarker.label_hand("Moving mouse", frame)


    return frame


def main():
    start_time = round(time.perf_counter() * 1000)
    mode = "msedge_surf"
    while cam.isOpened():
        success, frame = cam.read()
        if success:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            landmarker.detect_async(mp_image, start_time)
            frame_with_landmarks = landmarker.draw_landmarks(frame)

            if mode == "mouse":
                annotated_frame = handle_mouse(frame_with_landmarks)
            else:
                annotated_frame = controller.handle_orders(frame_with_landmarks, mode, landmarker)

            cv.imshow("Frame", annotated_frame)
            key = cv.waitKey(20)
            if key == ord("q"):
                break
        else: 
            break

if __name__ == "__main__":
    main()
