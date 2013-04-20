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
        return Point(self.currLocation[0], self.currLocation[1])
    
    def get_rotation(self):
        return self.currLocation[5]

'''
Occupancy grid - square grid of cells in which the value of each cell is the probability that
it is occupied
'''
class OccupancyGrid(object):
    def __init__(self, numCells_, cellSize_, origin_):
        self.gridSize = numCells_
        self.cellSize = cellSize_
        self.origin = origin_
        self.grid = [UNKNOWN for i in range(self.gridSize*self.gridSize)]
    
    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.name() == other.name() and  self.__dict__ == other.__dict__
    
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
        # transform points to be relative to centre of grid
        half_width = (self.gridSize * self.cellSize) / 2.0
        lp = pointSum(sensorValue.get_point(), Point(half_width, half_width))
        updateRadius = sensorValue.leftSonar+sonarModel.radialSpread
        sector = CircleSector(lp, startAngle, endAngle, updateRadius)
        
        # work out the maximum size of the area we need to update to avoid checking cells that
        # cannot overlap the area covered by the sensor update
        (minX, minY, maxX, maxY) = self.get_update_region(lp, updateRadius)
        
        for x in range(minX, maxX+1):
            sx= x*self.cellSize
            for y in range(minY, maxY+1):
                sy= y*self.cellSize
                cornerPoints = [ Point(sx,sy), 
                                 Point(sx+self.cellSize,sy), 
                                 Point(sx,sy + self.cellSize), 
                                 Point(sx+self.cellSize, sy+self.cellSize) ]
                numCornersInSector = 0
                for p  in cornerPoints:
                    if (sector.is_inside(p)):
                        numCornersInSector = numCornersInSector + 1
                if numCornersInSector > 0:
                    self.update_cell(x, y, numCornersInSector, sensorValue, sonarModel)


    # this is called when we know we have a cell in range of a sonar update and we need to update
    # the probability of the cell being occupied
    def update_cell(self, x, y, numCornersInSector, sensorValue, sonarModel):
        cellCentre = Point(x*self.cellSize+self.cellSize/2, 
                           y*self.cellSize+self.cellSize/2)
        # decide whether the cell is in the "probably empty" region or the "probably occupied" region
        cellDistance = pointDistance(sensorValue.get_point(), cellCentre)
        updateFactor = float(numCornersInSector) / 4.0
        if (cellDistance < sensorValue.leftSonar-sonarModel.radialSpread):
            # probably empty region
            self.set_cell_at(x, y, self.cell_at(x, y) + EMPTY_REGION_UPDATE * updateFactor)
        else:
            # probably occupied region
            self.set_cell_at(x, y, self.cell_at(x, y) + OCCUPIED_REGION_UPDATE * updateFactor)
        
    def get_update_region(self, robotPosition, updateRadius):
        cellX = int((robotPosition.x - self.origin.x) / self.cellSize)
        cellY = int((robotPosition.y - self.origin.y) / self.cellSize)
        cellRadius = int(round(0.5 + updateRadius / self.cellSize))
        minX = cellX-cellRadius if (cellX-cellRadius) > 0 else 0
        minY = cellY-cellRadius if (cellY-cellRadius) > 0 else 0
        maxX = cellX+cellRadius if (cellX+cellRadius) < self.gridSize else self.gridSize-1
        maxY = cellY+cellRadius if (cellY+cellRadius) < self.gridSize else self.gridSize-1
        return (minX, minY, maxX, maxY)

    # used to support JSON serialisation of custom classes
    def to_json(self):
        return { 'gridSize': self.gridSize,
                 'cellSize' : self.cellSize,
                 'origin-x' : self.origin.x,
                 'origin-y' : self.origin.y,
                 'grid' : self.grid }

    # used to enable this class & sub types to be reconstituted from JSON
    @classmethod
    def from_json(klass, json_object):
        obj = klass(json_object['gridSize'], 
                    json_object['cellSize'],
                    Point(json_object['origin-x'], json_object['origin-y']))
        obj.grid = json_object['grid']
        return obj
