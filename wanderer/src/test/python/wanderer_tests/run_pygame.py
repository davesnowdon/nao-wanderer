'''
Created on 13 Apr 2013

@author: dns
'''

import sys
import pygame
import wanderer.grid as grid
from wanderer.robotstate import nao_sonar_model
from util.geometry import Point
import random
import json
import time

CELL_PIX=5

def main():
    pygame.init() 
    
    data = load_sense_data()
    
    
    windowSize = grid.GRID_SIZE*CELL_PIX
    window = pygame.display.set_mode((windowSize, windowSize)) 
    
    board = grid.OccupancyGrid(grid.GRID_SIZE, grid.CELL_SIZE, Point(0,0))
    sonarModel = nao_sonar_model()
    
    send_sense(data, board, window, sonarModel)

    #generate_random_board(board)
    render_grid(window, board)
    
    pygame.display.flip()
    wait_for_exit() 

def load_sense_data(filename="../../../../../data/20130412062536.json"):
    try:
        raw = open(filename, 'r').read()
        if (raw.endswith("\n")):
            raw = raw[:-1]
        if (raw.endswith(",")):
            raw = raw[:-1]
        jsonstring = "[" + raw + "]"
        obj = json.loads(jsonstring.strip())
        return obj
    except Exception as e:
        print e

def generate_random_board(board):
    for i in range(0, 100):
        board.set_cell_at(random.randint(0,grid.GRID_SIZE-1), 
                          random.randint(0,grid.GRID_SIZE-1) , 
                          random.random())

def render_grid(window, board):
    for x in range(0, grid.GRID_SIZE):
        for y in range(0, grid.GRID_SIZE):
            value = board.cell_at(x, y)
            # white = empty, black = occupied
            g = 255 * (1.0 - value)
            color = (g, g, g)
            pygame.draw.rect(window, color, (x*CELL_PIX,y*CELL_PIX,CELL_PIX,CELL_PIX))
            
def wait_for_exit():
    while True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit(0) 
            
                
def send_sense(data, board, window, sonarModel):
    print "Reading sensor data"
    for x in data:
        left = x["leftSonar"]
        right = x["rightSonar"]
        position = x["position"]
        loc = grid.Location(left,right,position)
        #print repr(loc)
        board.update_grid_cells(loc, sonarModel)
        render_grid(window, board)
        pygame.display.flip()
        #time.sleep(0.01)
        #break
    print "done"
              
if __name__ == '__main__':
    main()