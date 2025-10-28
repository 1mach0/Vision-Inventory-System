"""
Purpose:
Provides a hardware-agnostic way to access camera frames.

What it does:
Wraps OpenCV’s VideoCapture.
Handles .start_video(), .stop_video(), .get_frame().
Handles resizing, error catching, and thread safety if needed.

Used by:
All app use-cases needing live images (validation, label scanning, face verification).
"""

import cv2 as cv

class CameraAdapter:
    def __init__(self, src=0):
        self.cam = None
        self.src = src

    def start_video(self):
        self.cam = cv.VideoCapture(self.src)
        if not self.cam.isOpened():
            raise RuntimeError(f"Cannot open camera {self.src}")

    def get_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            raise RuntimeError(f"Cannot receive frame from camera, exiting...")

        return frame

    def release(self):
        if self.cam:
            self.cam.release()



# if __name__ == "__main__":
#     cam = CameraAdapter(0)
#     cam.start_video()
#     while True:
#         frame = cam.get_frame()
#         cv.imshow("Camera", frame)
#         if cv.waitKey(1) == ord('q'):
#             break
#     cam.release()
