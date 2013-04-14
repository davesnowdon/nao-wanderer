'''
Created on 13 Apr 2013

@author: dns
'''

import math

from util.geometry import *
from robotstate import UltrasoundModel

GRID_SIZE=100
CELL_SIZE = 0.1
UNKNOWN = 0.5
EMPTY_REGION_UPDATE=-0.1
OCCUPIED_REGION_UPDATE=0.35

class Location(object):
    def __init__(self, leftSonar_, rightSonar_, currLocation_):
        self.leftSonar = leftSonar_
        self.rightSonar = rightSonar_
        self.currLocation = currLocation_
        
    def get_point(self):
        return Point(self.currLocation[0] + 5, self.currLocation[1] + 5)
    
    def get_rotation(self):
        return self.currLocation[5]

'''
Occupancy grid - square grid of cells in which the value of each cell is the probability that
it is occupied
'''
class OccupancyGrid(object):
    def __init__(self, numCells_, cellSize_):
        self.gridSize = numCells_
        self.cellSize = cellSize_
        self.grid = [UNKNOWN for i in range(self.gridSize*self.gridSize)]
    
    def cell_at(self, x, y):
        return self.grid[x+y*self.gridSize]
    
    def set_cell_at(self, x, y, value):
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        self.grid[x+y*self.gridSize] = value
        
    def update_grid_cells(self, sensorValue, sonarModel):
        startAngle = sensorValue.get_rotation() - sonarModel.angularSpread
        endAngle = sensorValue.get_rotation() + sonarModel.angularSpread
        sector = CircleSector(sensorValue.get_point(), startAngle, endAngle, 
                              sensorValue.leftSonar+sonarModel.radialSpread)

        lp = sensorValue.get_point()
        for x in range(0, self.gridSize):
            sx= x*self.cellSize
            for y in range(0, self.gridSize):
                sy= y*self.cellSize
                cornerPoints = [ Point(sx,sy), 
                                 Point(sx+self.cellSize,sy), 
                                 Point(sx,sy + self.cellSize), 
                                 Point(sx+self.cellSize, sy+self.cellSize) ]
                for p  in cornerPoints:
                    if(is_inside_sector(p, lp, startAngle, endAngle, sensorValue.leftSonar)):
                        if (sector.is_inside(p)):
                            self.update_cell(x, y, sensorValue, sonarModel)
                            # only update a cell once
                            break

    # this is called when we know we have a cell in range of a sonar update and we need to update
    # the probability of the cell being occupied
    def update_cell(self, x, y, sensorValue, sonarModel):
        cellCentre = Point(x*self.cellSize+self.cellSize/2, 
                           y*self.cellSize+self.cellSize/2)
        # decide whether the cell is in the "probably empty" region or the "probably occupied" region
        cellDistance = pointDistance(sensorValue.get_point(), cellCentre)
        if (cellDistance < sensorValue.leftSonar-sonarModel.radialSpread):
            # probably empty region
            self.set_cell_at(x, y, self.cell_at(x, y) + EMPTY_REGION_UPDATE)
        else:
            # probably occupied region
            self.set_cell_at(x, y, self.cell_at(x, y) + OCCUPIED_REGION_UPDATE)
        

