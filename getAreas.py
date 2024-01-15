#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

Description: Setting up the points to querry from the OSM heightmap (open-elevation): https://github.com/Jorl17/open-elevation/blob/master/docs/api.md

'''
from PIL import Image
import numpy as np

import heightRequests

class Heightmap:
    """List of points where we sample the height, required the coordinates of the bottom left and top right points 
    and the number of points in each direction (pointsX and pointsY), resuling in a pointsX x pointsY resolution.
    """
    def __init__(self, bottom_left: tuple, top_right: tuple, pointsX: int, pointsY: int) -> None:
        self.bottom_left: tuple(float, float) = bottom_left
        self.top_right: tuple(float, float) = top_right

        self.pX: int = pointsX
        self.pY: int = pointsY

        # Fill up the points:
        step_x = abs(top_right[0] - bottom_left[0]) / pointsX
        step_y = abs(top_right[1] - bottom_left[1]) / pointsY

        self.points = [{"latitude" : bottom_left[0] + step_x * x, "longitude" :  bottom_left[1] + step_y * y} for x in range(0, pointsX) for y in range(0, pointsY)]

        self.jsonBody = {}
        self.jsonBody["locations"] = self.points

        self.elevations: list = []


    def getElevations(self) -> None:
        hr = heightRequests.heighmapRequest(self.jsonBody)
        outputJSON = hr.makeRequest()
        self.elevations = [j["elevation"] for j  in outputJSON["results"]]

    def normalizeElevations(self) -> None:
        """Normalize the elevations to 0 to 255 to be exportable as a grayscale image"""
        minHeight = min(self.elevations)
        maxHeight = max(self.elevations)

        self.elevations = [(d - minHeight)/(maxHeight-minHeight)*255 for d in self.elevations]

    def exportHeightmap(self, outName: str) -> None:
        elevs = np.array(self.elevations).astype(np.uint8)
        elevs = elevs.reshape(self.pX, self.pY)

        image = Image.fromarray(elevs)
        image.save(outName + ".png")
        

    

    