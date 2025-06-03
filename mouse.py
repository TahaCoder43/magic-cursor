import uinput
from time import perf_counter, sleep
from typing import List
import numpy as np

from landmarker import LandMarker

class Mouse:
    def __init__(self):
        events = [
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.REL_X,
            uinput.REL_Y,
        ]
        self.previous_wrist_x: int = 0
        self.previous_wrist_y: int = 0
        self.mouse = uinput.Device(events)
        self.bait_movement_threshold_y = 0.004
        self.bait_movement_threshold_x = 0.006
        self.is_holding_click = False

    def click(self):
        if not self.is_holding_click:
            self.mouse.emit(uinput.REL_X, 1, syn=False)
            sleep(0.1)
            self.mouse.emit(uinput.BTN_LEFT, 1)
            sleep(0.1)
            self.mouse.emit(uinput.BTN_LEFT, 0)
            self.is_holding_click = True
    
    def release_click(self):
        if self.is_holding_click:
            self.is_holding_click = False

    def move(self, wrist, sensitivity: int = 100):
        wrist_x = round(wrist.x * sensitivity)
        wrist_y = round(wrist.y * sensitivity)
        delta_x = wrist_x - self.previous_wrist_x
        delta_y = wrist_y - self.previous_wrist_y
        # print(wrist.x, self.previous_wrist_x, wrist.y, self.previous_wrist_y)

        if abs(delta_x) > self.bait_movement_threshold_x * sensitivity:
            self.mouse.emit(uinput.REL_X, delta_x*-1, syn=True) # X movmeent is inversed
        if abs(delta_y) > self.bait_movement_threshold_y * sensitivity:
            self.mouse.emit(uinput.REL_Y, delta_y, syn=True)

        self.previous_wrist_x = wrist_x
        self.previous_wrist_y = wrist_y


class Controller:
    def __init__(self):
        events = [
            uinput.KEY_SPACE,
            uinput.KEY_RIGHT,
            uinput.KEY_LEFT,
        ]
        self.controller = uinput.Device(events)
        self.is_controlling = False

    def handle_orders(self, frame: np.ndarray, mode: str, landmarker: LandMarker) -> np.ndarray:
        match mode:
            case "geometry_dash":
                frame = self.handle_geometry_dash_orders(frame, landmarker)
            case "msedge_surf":
                frame = self.handle_msedge_surf_orders(frame, landmarker)

        return frame

    def handle_geometry_dash_orders(self, frame: np.ndarray,  landmarker: LandMarker) -> np.ndarray:
        has_triggered_action1 = landmarker.has_ordered(0.03, "index")
        if has_triggered_action1:
            frame = landmarker.label_hand("Triggering action 1", frame)
            if not self.is_controlling:
                self.controller.emit_click(uinput.KEY_SPACE)
                self.is_controlling = True
        else:
            self.is_controlling = False

        return frame

    def handle_msedge_surf_orders(self, frame: np.ndarray, landmarker: LandMarker) -> np.ndarray:
        has_triggered_action1 = landmarker.has_ordered(0.045, "index")
        has_triggered_action2 = landmarker.has_ordered(0.045, "middle")
        has_triggered_action3 = landmarker.has_ordered(0.045, "ring")
        if has_triggered_action1:
            frame = landmarker.label_hand("Triggering action 1", frame)
            if not self.is_controlling:
                self.controller.emit_click(uinput.KEY_LEFT)
                self.is_controlling = True
        elif has_triggered_action2:
            frame = landmarker.label_hand("Triggering action 2", frame)
            if not self.is_controlling:
                self.controller.emit_click(uinput.KEY_RIGHT)
                self.is_controlling = True
        elif has_triggered_action3:
            frame = landmarker.label_hand("Triggering action 3", frame)
            if not self.is_controlling:
                self.controller.emit_click(uinput.KEY_SPACE)
                self.is_controlling = True
        else:
            self.is_controlling = False

        return frame

    
