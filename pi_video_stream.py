import sys
sys.path.append('..')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import imutils
from imutils.video import FPS
import time
from datetime import datetime
from configparser import ConfigParser
import wiringpi as wpi
import os
import tables
import csv
import io



class pi_video_stream():
    def __init__(self, data_path):
        # Read config file
        config = ConfigParser()
        config.read('config.ini')
        cfg = 'tracker_cage_record'
        res = list(map(int, config.get(cfg, 'resolution').split(', ')))
        fr = int(config.get(cfg, 'framerate'))
        iso = int(config.get(cfg, 'iso'))
        sensormode = int(config.get(cfg, 'sensor_mode'))
        
        self.data_path = data_path
        self.record_time_sec = int(config.get(cfg, 'record_time_sec'))

        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = res
        self.camera.framerate = fr
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1,1)
        # Camera.exposure_mode ='off'
        self.camera.shutter_speed = 30000
        self.camera.iso = iso
        self.camera.sensor_mode = sensormode
        self.rawCapture = PiRGBArray(self.camera, size=res)

        # allow the camera to warmup
        time.sleep(0.1)

    def setdown(self):
        self.out.release()
        self.camera.stop_preview()  
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
        
        
    def record_prep(self):
        # Starting camera and preview
        self.vstream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        self.camera.start_preview(fullscreen=False, window=(0,0,256,256))
        self.fps = FPS().start()
        self.out = cv2.VideoWriter(self.data_path + os.sep + 'frame.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20.0, self.camera.resolution)
        print("Start recording\n\n")
        
        
    def record(self):
        # Capturing frame by frame
        '''
        for i, filename in enumerate(
                self.camera.capture_continuous(self.data_path + os.sep +'frame{counter:02d}.jpg', use_video_port = True)):
            self.fps.update()
        '''
        for img in self.vstream:
            # Update frame count
            self.fps.update()

            # Write to video
            self.out.write(img.array)
            #cv2.imwrite(self.data_path + os.sep + 'frame' + str(self.fps._numFrames) +'.jpg' ,img.array)
            self.rawCapture.seek(0)

        
            
        
       


        

