if __name__ == "__main__":
    import cv2
    from streamer import STREAMER
    from detector import DETECTOR
    from projector import PROJECTOR
    import multiprocessing


    class VIDEO_STREAM_ANALYZER(object):
        def __init__(self):
            self.raw_frames_q = multiprocessing.Queue()
            frame_data_q = multiprocessing.Queue()
            self.streamer = STREAMER()
            self.detector = DETECTOR(self.raw_frames_q, frame_data_q)
            self.projector = PROJECTOR(frame_data_q)

        def activate(self):
            start_event = multiprocessing.Event()
            stop_event = multiprocessing.Event()

            streamer_process = multiprocessing.Process(target=self.streamer.get_next_frame, args=(self.raw_frames_q, start_event, stop_event))
            detector_process = multiprocessing.Process(target=self.detector.get_contours, args=(stop_event, ))
            projector_process = multiprocessing.Process(target=self.projector.present_detection_frame, args=(stop_event, ))

            streamer_process.start()
            try:
                start_event.wait()

                detector_process.start()

                projector_process.start()

                streamer_process.join()
            finally:
                stop_event.set()
                streamer_process.join()
                detector_process.join()
                projector_process.join()
                cv2.destroyAllWindows()


    vsa = VIDEO_STREAM_ANALYZER()
    vsa.activate()

