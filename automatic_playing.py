#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:40:36 2020

@author: ajuvenn
"""

import pyautogui
from grid import Grid, LEFT, RIGHT, UP, DOWN, RED, BLUE, YELLOW, GREEN
import solver


def color_to_button_path(color):
    
    if color == BLUE:
        return 'buttons/blue.png'
    
    if color == RED:
        return 'buttons/red.png'   
    
    if color == GREEN:
        return 'buttons/green.png'
    
    if color == YELLOW:
        return 'buttons/yellow.png'    
    
    
    
def direction_to_key_name(direction):
    
    if direction == LEFT:
        return 'left'
    
    if direction == RIGHT:
        return 'right'   
    
    if direction == UP:
        return 'up'
    
    if direction == DOWN:
        return 'down'        
    
    

    
def play(g : Grid, grid_coords, robot_color, direction):
    
    robot_node = g.robot_nodes[robot_color]
    robot_i = robot_node.i
    robot_j = robot_node.j

    grid_width = grid_coords[-1] 
    grid_left = grid_coords[0]
    grid_top = grid_coords[1]
    
    button_x = grid_left + int((float(grid_width) * (robot_j + 0.5)) / 16.)
    button_y = grid_top + int((float(grid_width) * (robot_i + 0.5)) / 16.)
    
    pyautogui.click(button_x, button_y)
    key_to_press = direction_to_key_name(direction)
    pyautogui.press(key_to_press)
    
    g.move(robot_color, direction)





def compute_grid_coords(restart_button_coords):
    
    left, top, width, height = restart_button_coords
    
    restart_button_center = pyautogui.center(restart_button_coords)
    
    x, y = restart_button_center
    
    min_width_height = min(width, height)
    grid_width = 8 * min_width_height
    grid_left = x - 4 * min_width_height
    grid_top = y - 4 * min_width_height
    
    return (grid_left, grid_top, grid_width, grid_width)




def screenshot_grid(grid_picture_output_path, grid_coords):
    pyautogui.screenshot(grid_picture_output_path, region = grid_coords)




def automatic_play(maximum_solution_length, pause = 0.25):
    
    pyautogui.PAUSE = pause
  
    restart_button_coords = pyautogui.locateOnScreen('buttons/restart.png')

    if restart_button_coords is None:
        raise(Exception("Couldn't find restart button on screen"))
        
    restart_button_center = pyautogui.center(restart_button_coords)
    pyautogui.click(*restart_button_center)

    grid_coords = compute_grid_coords(restart_button_coords)
     
    for i in range(5):
        
        pyautogui.moveTo(0, 0)
        grid_picture_path = "./saved_grids/grid_{}.png".format(i)
        screenshot_grid(grid_picture_path, grid_coords)
        g = Grid.from_picture(grid_picture_path)
        
        actions = solver.find_solution(g, maximum_solution_length)
        
        if actions is None:
            raise(Exception, "No solution found")
            
        g.reset_to_starting_state()
            
        for action in actions:
            play(g, grid_coords, *action)
        
        
        
        
        
        
if __name__ == '__main__':
    
    automatic_play(20)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        