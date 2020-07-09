import cv2
from numpy import ndarray


class InputFeeder:
    def __init__(self, input_type, input_file=None):
        print(input_type, '---', input_file)
        self.input_type = input_type
        if input_type == 'video' or input_type == 'image':
            self.input_file = input_file

    def load_data(self):
        if self.input_type == 'video':
            self.cap = cv2.VideoCapture(self.input_file)
        elif self.input_type == 'cam':
            self.cap = cv2.VideoCapture(0)

        else:
            self.cap = cv2.imread(self.input_file)

    def next_batch(self):
        while True:
            for _ in range(10):
                _, frame = self.cap.read()
            print(type(frame))
            # print(frame)
            # exit(0)
            yield frame

    def close(self):
        if not self.input_type == 'image':
            self.cap.release()
