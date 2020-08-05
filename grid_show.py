# -*- coding: utf-8 -*-

import grid
import numpy as np
import cv2


CASE_WIDTH  = 50


def extract_case(img, i, j):
    return img[i * CASE_WIDTH : (i+1) * CASE_WIDTH,
               j * CASE_WIDTH : (j+1) * CASE_WIDTH,
               :]
    


def extract_case_interior(img, i, j, eps = 0.3):

    case = extract_case(img, i, j)
    
    return case[int((0.5 - eps) * CASE_WIDTH) : int((0.5 + eps) * CASE_WIDTH),
                int((0.5 - eps) * CASE_WIDTH) : int((0.5 + eps) * CASE_WIDTH)]
    




def draw_wall(img, i, j, direction, width, color):
    
    case = extract_case(img, i, j)
  
    if direction == grid.UP:
       pixels_to_draw = case[0:width, :, :]
    
    if direction == grid.DOWN:
        pixels_to_draw = case[-(width+1):, :, :]
    
    if direction == grid.LEFT:
        pixels_to_draw = case[:, 0:width, :]
        
    if direction == grid.RIGHT:
        pixels_to_draw = case[:, -(width+1):, :]
        
    pixels_to_draw[:] = color
    



def draw_cross(img, i, j, color, cross_width = 0.1, cross_height = 0.4):
    
    case = extract_case(img, i, j)

    case[int((0.5 - cross_width) * CASE_WIDTH) : int((0.5 + cross_width) * CASE_WIDTH),
         int((0.5 - cross_height) * CASE_WIDTH) : int((0.5 + cross_height) * CASE_WIDTH),
         :] = color

    case[int((0.5 - cross_height) * CASE_WIDTH) : int((0.5 + cross_height) * CASE_WIDTH), 
         int((0.5 - cross_width) * CASE_WIDTH) : int((0.5 + cross_width) * CASE_WIDTH), 
         :]  = color


robot_colors = [np.array([255., 85., 85.]), # Blue
                np.array([0., 128., 0.]), # Green
                np.array([0., 0., 255.]), # Red
                np.array([31., 220., 220.]) #Yellow
                ]

goal_colors = [np.array([139., 0., 0.]), # Blue
               np.array([144., 238., 144.]), # Green
               np.array([203., 192., 255.]), # Red
               np.array([31., 255., 252.]) #Yellow
              ]    


wall_color = np.array([0, 0, 0])
case_limit_color =  np.array([220, 220, 220]) 


def draw_case_interior(img, i, j, color):
    
    case_interior = extract_case_interior(img, i, j)
    case_interior[:] = color
    

def create_picture(g):
    
    img = np.empty((CASE_WIDTH * 16, CASE_WIDTH * 16, 3), np.uint8)
    
    for i in range(16):
        for j in range(16):
            
            case = extract_case(img, i, j)
            case[:] = np.array([255, 255, 255]) 
            
            for direction in range(4):
                draw_wall(img, i, j, direction, 1, case_limit_color)
    
    for i in range(16):
        for j in range(16):
            
            node = g.node(i, j) 
            
            for direction in range(4):
                if node.blocked_neighbours[direction] == 1:
                    draw_wall(img, i, j, direction, 2, wall_color)
            
    goal_color_id = g.objective_color
    goal_index = g.objective_node.index
    i, j = (goal_index // 16), (goal_index % 16)
    draw_case_interior(img, i, j, goal_colors[goal_color_id])
                    
    for color_id in range(4):
        robot_index = g.robot_nodes[color_id].index
        i, j = (robot_index // 16), (robot_index % 16)
        draw_cross(img, i, j, robot_colors[color_id])
          
    return img

    


def show_picture(name, g):
    
    img = create_picture(g)
    cv2.imshow(name, img)


def wait_key(delay):
   cv2.waitKey(delay)


    
    
    
    