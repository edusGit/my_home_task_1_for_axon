import queue

import cv2
import imutils
from common import FRAME_DATA


class DETECTOR(object):
    def __init__(self, raw_frames_q, frame_data_q):
        self.prev_frame = None
        self.frames_counter = 0
        self.raw_frames_q = raw_frames_q
        self.frame_data_q = frame_data_q

    def get_contours(self, stop_event):
        while not stop_event.is_set():
            try:
                new_frame = self.raw_frames_q.get()
                # new_frame = new_frames_q.recv()
                gray_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
                if self.frames_counter == 0:
                    self.prev_frame = gray_frame
                    self.frames_counter += 1
                else:
                    diff = cv2.absdiff(gray_frame, self.prev_frame)
                    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contours = imutils.grab_contours(contours)
                    self.prev_frame = gray_frame
                    self.frames_counter += 1

                    frame_data = FRAME_DATA(new_frame, contours)

                    self.frame_data_q.put(frame_data)
            except queue.Empty:
                pass
