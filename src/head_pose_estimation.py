import numpy as np
import time
from openvino.inference_engine import IENetwork, IECore
import os
import cv2
import argparse
import sys


class Model_Head:
    '''
    Class for the Head Pose Detection Model.
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
        print('Succesful execute - Head Pose Detection')

    def load_model(self):
        self.plugin = IECore()
        self.net_plugin = self.plugin.load_network(
            network=self.model, device_name=self.device, num_requests=1)
        print('Model Loaded - Head Pose Detection')

    def predict(self, image):
        infer_request_handle = self.net_plugin.start_async(
            request_id=0, inputs={self.input_name: self.preprocess_input(image)})
        if(infer_request_handle.wait() == 0):
            net_output_yaw = infer_request_handle.outputs["angle_y_fc"]
            net_output_pitch = infer_request_handle.outputs["angle_p_fc"]
            net_output_roll = infer_request_handle.outputs["angle_r_fc"]

        print('Prediction Complete - Head Pose Detection')
        return(net_output_yaw, net_output_pitch, net_output_roll)

    def check_model(self):
        raise NotImplementedError

    def preprocess_input(self, image):
        n, c, h, w = self.input_shape
        im_frame = cv2.resize(image, (w, h))
        im_frame = im_frame.transpose((2, 0, 1))
        im_frame = im_frame.reshape((n, c, h, w))
        print('Succesful preprocessing - Head Pose Detection')
        return(im_frame)
