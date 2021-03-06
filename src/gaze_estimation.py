import numpy as np
import time
from openvino.inference_engine import IENetwork, IECore
import os
import cv2
import argparse
import sys


class Model_Gaze:
    '''
    Class for the Gaze Detection Model.
    '''

    def __init__(self, model_name, device='CPU', threshold=0.60, extensions=None):
        self.model_weights = model_name+'.bin'
        self.model_structure = model_name+'.xml'
        self.device = device
        self.threshold = threshold

        self.infer_request_handle = None

        try:
            self.model = IENetwork(self.model_structure, self.model_weights)
        except Exception as e:
            raise ValueError(
                "Could not Initialise the network. Have you enterred the correct model path?")

        self.input_name = next(iter(self.model.inputs))
        self.input_shape = self.model.inputs[self.input_name].shape
        self.output_name = next(iter(self.model.outputs))
        self.output_shape = self.model.outputs[self.output_name].shape
        print('Succesful execute - Gaze Detection')

    def load_model(self):
        self.plugin = IECore()
        self.net_plugin = self.plugin.load_network(
            network=self.model, device_name=self.device, num_requests=1)
        print('Model Loaded - Gaze Detection')

    def predict(self, left_eye_image, right_eye_image, head_pose_angles):

        inp_dic = {

            "left_eye_image": left_eye_image,
            "right_eye_image": right_eye_image,
            "head_pose_angles": head_pose_angles

        }

        infer_request_handle = self.net_plugin.start_async(
            request_id=0, inputs=inp_dic)
        if(infer_request_handle.wait() == 0):
            gaze_vector = infer_request_handle.outputs["gaze_vector"]

        return(gaze_vector)

    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):

        n, c, h, w = [1, 3, 60, 60]

        im_frame = cv2.resize(image, (w, h))
        im_frame = im_frame.transpose((2, 0, 1))
        im_frame = im_frame.reshape((n, c, h, w))
        print('Succesful preprocessing - Gaze Detection')
        return(im_frame)
