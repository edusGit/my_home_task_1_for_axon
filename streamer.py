import cv2


class STREAMER(object):
    def __init__(self):
        self.input_video_full_path = "C:\\axon\\1\\People - 6387.mp4"

    def get_next_frame(self, raw_frames_q, start_event, stop_event):
        cap = cv2.VideoCapture(self.input_video_full_path)
        start_event.set()
        while not stop_event.is_set():
            ret, raw_frame = cap.read()
            if ret:
                raw_frames_q.put(raw_frame)
            else:
                break
        cap.release()
        print("streamer ended")
