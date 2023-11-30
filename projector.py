import queue
import cv2
import time

MIN_AREA = 1000

class PROJECTOR(object):
    def __init__(self, new_frame_data_detection_queue):
        self.frame_data_q = new_frame_data_detection_queue

    def present_detection_frame(self, stop_event):
        while not stop_event.is_set():
            try:
                new_frame_data = self.frame_data_q.get()
                # new_frame_data = new_frame_data_detection_queue.recv()
                if new_frame_data is not None:
                    new_frame = new_frame_data.frame
                    contours = new_frame_data.contours

                    # loop over the contours
                    for c in contours:
                        # if the contour is too small, ignore it
                        if cv2.contourArea(c) < MIN_AREA:
                            continue
                        # compute the bounding box for the contour, draw it on the frame,
                        # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(new_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    blurred_frame = cv2.blur(new_frame, (10, 10))
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    cv2.putText(blurred_frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                                cv2.LINE_AA)
                    cv2.imshow("frame", blurred_frame)
                    cv2.waitKey(10)
            except queue.Empty:
                pass
