import cv2

from vision import frames

class ComputerVision:

    cap = cv2.VideoCapture(0)

    def __init__(self):
        print("")

    def start_recording(self):
        print("Computer Vision Started...")
        while True:
            ret, frame = self.cap.read()
            frame = frames.rescale_frame(frame, percent=30)

            cv2.imshow('frame', frame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    def stop_recording(self):
        cv2.destroyWindow(self.cap)
        print("Computer Vision Stopped...")
