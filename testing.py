from landmarker import LandMarker
import sys


def check_falseflag_stationary_movement_generator():
    previous_x = 0
    previous_y = 0
    previous_z = 0
    min_x_movement = sys.maxsize 
    min_y_movement = sys.maxsize 
    min_z_movement = sys.maxsize 
    max_x_movement = 0
    max_y_movement = 0
    max_z_movement = 0
    runs = 0

    def check_falseflag_stationary_movement(landmarker: LandMarker):
        nonlocal previous_x, previous_y, previous_z, min_x_movement, min_y_movement, min_z_movement, max_x_movement, max_y_movement, max_z_movement, runs

        try:
            landmarks = landmarker.result.hand_world_landmarks
        except AttributeError:
            return

        if len(landmarks) != 0:
            wrist = landmarks[0][0]

            if previous_x == 0 or previous_y == 0 or previous_z == 0:
                previous_x = wrist.x
                previous_y = wrist.y
                previous_z = wrist.z
                return

            if runs < 50:
                runs += 1
                return 

            x_movement = abs(wrist.x - previous_x)
            y_movement = abs(wrist.y - previous_y)
            z_movement = abs(wrist.z - previous_z)

            if x_movement < min_x_movement and x_movement != 0.0:
                min_x_movement = x_movement
            if y_movement < min_y_movement and y_movement != 0.0:
                min_y_movement = y_movement
            if z_movement < min_z_movement and z_movement != 0.0:
                min_z_movement = z_movement

            if x_movement > max_x_movement:
                max_x_movement = x_movement
            if y_movement > max_y_movement:
                max_y_movement = y_movement
            if z_movement > max_z_movement:
                max_z_movement = z_movement

            previous_x = wrist.x
            previous_y = wrist.y
            previous_z = wrist.z

            # print("current")
            # print(round(x_movement*1000, 3), round(y_movement*1000, 3), round(z_movement*1000, 3))
            print("min")
            print(round(min_x_movement*1000, 3), round(min_y_movement*1000, 3), round(min_z_movement*1000, 3))
            print("max")
            print(round(max_x_movement*1000, 3), round(max_y_movement*1000, 3), round(max_z_movement*1000, 3))


    return check_falseflag_stationary_movement

check_falseflag_stationary_movement = check_falseflag_stationary_movement_generator()
