from time import perf_counter
import math
from typing import Any, Tuple
from cv2.typing import Point
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions import drawing_utils
from mediapipe.python.solutions.hands import HAND_CONNECTIONS
import numpy as np
import sys
import cv2

finger_tip_indexes = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20,
}

vision = mp.tasks.vision

class LandMarker:
    def __init__(self, live_recording_size: Tuple[int,int]):
        def update_result(result, output_image: mp.Image, timestamp_ms: int):
            self.result = result
            

        self.options = vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path='./hand_landmarker.task'),
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=update_result,
            min_tracking_confidence=0.3,
        )

        self.result = vision.HandLandmarkerResult
        self.landmarker = vision.HandLandmarker.create_from_options(self.options)
        self.box_padding_percentage = 0.1
        self.label_font_face = cv2.FONT_HERSHEY_DUPLEX
        self.label_height = 10
        self.label_thickness = 1
        self.label_scale = 1
        self.label_color = (0, 0, 0)
        self.live_recording_size = live_recording_size

        for scale in range(1, 101, 1):
            scale = scale / 10
            height_for_scale = cv2.getTextSize("I", self.label_font_face, scale, self.label_thickness)[0][1]
            if height_for_scale > 15:
                self.label_scale = scale
                break


    def detect_async(self, frame: mp.Image, start: int):
        frame_timestamp_ms = round(perf_counter() * 1000) - start
        self.landmarker.detect_async(frame, frame_timestamp_ms)

    def close(self):
        self.landmarker.close()

    def draw_landmarks(self, image: np.ndarray) -> np.ndarray:
        try: 
            each_hand_landmarks = self.result.hand_landmarks
        except AttributeError:
            return image

        if len(each_hand_landmarks) == 0:
            return image

        for i in range(len(each_hand_landmarks)):
            hand_landmarks = each_hand_landmarks[i]

            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            for landmark in hand_landmarks:
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                ])

            drawing_utils.draw_landmarks(image, hand_landmarks_proto, HAND_CONNECTIONS)

        return image

    def label_hand(self, label: str, image: np.ndarray) -> np.ndarray:
        try: 
            each_hand_landmarks = self.result.hand_landmarks
        except AttributeError:
            return image

        if len(each_hand_landmarks) == 0:
            return image

        for hand_landmarks in each_hand_landmarks:
            hand_min_x = math.inf
            hand_max_x = -math.inf
            hand_min_y = math.inf
            hand_max_y = -math.inf

            for landmark in hand_landmarks:
                if landmark.x < hand_min_x:
                    hand_min_x = landmark.x
                if landmark.x > hand_max_x:
                    hand_max_x = landmark.x

                if landmark.y < hand_min_y:
                    hand_min_y = landmark.y
                if landmark.y > hand_max_y:
                    hand_max_y = landmark.y

            box_padding_x = (hand_max_x - hand_min_x) * self.box_padding_percentage
            box_padding_y = (hand_max_y - hand_min_y) * self.box_padding_percentage
            from_x = hand_min_x - box_padding_x
            to_x = hand_max_x + box_padding_x
            from_y = hand_min_y - box_padding_y
            to_y = hand_max_y + box_padding_y


            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.append(landmark_pb2.NormalizedLandmark(x=from_x, y=from_y, z=0.1))
            hand_landmarks_proto.landmark.append(landmark_pb2.NormalizedLandmark(x=to_x, y=from_y, z=0.1))
            hand_landmarks_proto.landmark.append(landmark_pb2.NormalizedLandmark(x=to_x, y=to_y, z=0.1))
            hand_landmarks_proto.landmark.append(landmark_pb2.NormalizedLandmark(x=from_x, y=to_y, z=0.1))
            drawing_utils.draw_landmarks(image, hand_landmarks_proto, [(0, 1), (1, 2), (2, 3), (3, 0)])
            print("min x max y")
            from_x_px = round(from_x * self.live_recording_size[0])
            from_y_px = round(from_y * self.live_recording_size[1])

            image = cv2.putText(
                image,
                label,
                (from_x_px, from_y_px - self.label_height),
                self.label_font_face,
                self.label_scale,
                self.label_color,
                self.label_thickness
            )

        return image
        

    def has_ordered(self, distance_threshold: float = 0.035, finger_in_ok_sign="index") -> bool:
        try:
            landmarks = self.result.hand_world_landmarks
            if len(landmarks) == 0:
                return False

            finger_tip_index = finger_tip_indexes[finger_in_ok_sign]
            thumb_tip = landmarks[0][4]
            finger_tip = landmarks[0][finger_tip_index]
            distance_of_tips = math.sqrt(
                (finger_tip.x - thumb_tip.x)**2 +
                (finger_tip.y - thumb_tip.y)**2 +
                (finger_tip.z - thumb_tip.z)**2
            )
            print(finger_in_ok_sign, distance_of_tips)
            has_ordered_click = distance_of_tips < distance_threshold

            return has_ordered_click
        except AttributeError as _:
            return False

    def on_mouse(self, y_threshold=0.013, z_threshold=0.008) -> tuple[bool, Any]:
        try:
            landmarks = self.result.hand_world_landmarks
            if len(landmarks) == 0:
                return False, None

            index_joints = landmarks[0][5:8]
            knuckle_pip_delta_y = abs(index_joints[1].y - index_joints[0].y)
            pip_dip_delta_z = abs(index_joints[2].z - index_joints[1].z)
    

            if knuckle_pip_delta_y > y_threshold and pip_dip_delta_z > z_threshold:
                on_mouse = True
            else:
                on_mouse = False

            return on_mouse, landmarks[0][0]
        except AttributeError as _:
            return False, None

