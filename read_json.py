# -*- coding: utf-8 -*-
import numpy as np
import json

photo_flag = 1080
class ReadAnno:
    def __init__(self, json_path, process_mode="keypoints"):
        self.json_data = json.load(open(json_path))
        self.filename = self.json_data['imagePath']
        self.width = self.json_data['imageWidth']
        self.height = self.json_data['imageHeight']
        self.coordis = []
        self.keypoints = []
        self.classes = []

        assert process_mode in ["rectangle", "polygon", "keypoints"]
        if process_mode == "rectangle":
            self.process_polygon_shapes()
        elif process_mode == "polygon":
            self.process_polygon_shapes()
        elif process_mode == "keypoints":
            self.process_keypoints()

    def process_rectangle_shapes(self):
        for single_shape in self.json_data['shapes']:
            bbox_class = single_shape['label']
            xmin = single_shape['points'][0][0]
            ymin = single_shape['points'][0][1]
            xmax = single_shape['points'][1][0]
            ymax = single_shape['points'][1][1]
            self.coordis.append([xmin, ymin, xmax, ymax, bbox_class])

    def process_polygon_shapes(self):

        for single_shape in self.json_data['shapes']:
            bbox_class = single_shape['label']
            temp_points = []
            for couple_point in single_shape['points']:
                x = float(couple_point[0])
                y = float(couple_point[1])
                ###之后要写一个按点提取身体上半身坐标
                temp_points.append([x, y])

            temp_points = np.array(temp_points)
            xmin, ymin = temp_points.min(axis=0)
            xmax, ymax = temp_points.max(axis=0)

            self.coordis.append([xmin, ymin, xmax, ymax, bbox_class])

    def process_keypoints(self):
        temp_keypoint =[]
        for single_shape in enumerate(self.json_data['shapes']):
            for _num,_keypoint in enumerate(single_shape[1]['points']):
                print(_num)
                if _num == 0:
                    self.keypoints.append(_keypoint)
                    self.classes.append(1)
                if _num == 3:
                    temp_keypoint = _keypoint

                if _num == 5:
                    print(5)
                    self.keypoints.append(_keypoint)
                    self.classes.append(2)
                    self.keypoints.append(temp_keypoint)
                    self.classes.append(3)
                    temp_keypoint =[]

    def get_width_height(self):
        return self.width, self.height

    def get_filename(self):
        return self.filename

    def get_coordis(self):
        return self.coordis

    def get_keypoints(self):
        return self.classes,self.keypoints