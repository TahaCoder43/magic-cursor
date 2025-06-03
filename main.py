import cv2 as cv
# import ffmpegcv

cam = cv.VideoCapture(0)

while cam.isOpened():
    success, frame = cam.read()
    if success:
        cv.imshow("Frame", frame)
        key = cv.waitKey(20)
        if key == ord("q"):
            break
    else: 
        break

# import mediapipe as mp
#
# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
# VisionRunningMode = mp.tasks.vision.RunningMode
#
# # Create a hand landmarker instance with the live stream mode:
# def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#     print('hand landmarker result: {}'.format(result))
#
# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
#     running_mode=VisionRunningMode.LIVE_STREAM,
#     result_callback=print_result)
#
# with HandLandmarker.create_from_options(options) as landmarker:
