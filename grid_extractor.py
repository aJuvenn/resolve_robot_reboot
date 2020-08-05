#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:32:50 2020

@author: ajuvenn
"""

import numpy as np
import grid

import cv2
import sys



NB_CASES = 16



def extract_case(M, i, j):
    
    height, width, unused = M.shape

    case_width = float(width) / NB_CASES
    case_height = float(height) / NB_CASES
    case_width = float(width) / NB_CASES
    case_height = float(height) / NB_CASES
    
    min_y  = int(case_height * i)
    max_y = min(int(case_height * (i+1)), height)
    
    min_x  = int(case_width * j)
    max_x = min(int(case_width * (j+1)), width)
    
    return M[min_y:max_y, min_x:max_x, :]



def extract_case_interior(M, i, j, eps = 0.2):

    case = extract_case(M, i, j)
    height, width, unused = case.shape
    
    return case[int((0.5 - eps) * height) : int((0.5 + eps) * height),
                int((0.5 - eps) * width) : int((0.5 + eps) * width)]
    
    



        
def has_a_wall(M, i , j, direction, threshold = 100.):
    
    case = extract_case(M, i, j)
  
    if direction == grid.UP:
       pixels_to_check = case[0, :, :]
    
    if direction == grid.DOWN:
        pixels_to_check = case[-1, :, :]
    
    if direction == grid.LEFT:
        pixels_to_check = case[:, 0, :]
        
    if direction == grid.RIGHT:
        pixels_to_check = case[:, -1, :]
    
    pixels_average = np.average(pixels_to_check)
    
    return pixels_average < threshold
    
    
            

def draw_wall(M, i, j, direction):
    
    case = extract_case(M, i, j)
  
    if direction == grid.UP:
       pixels_to_draw = case[0, :, :]
    
    if direction == grid.DOWN:
        pixels_to_draw = case[-1, :, :]
    
    if direction == grid.LEFT:
        pixels_to_draw = case[:, 0, :]
        
    if direction == grid.RIGHT:
        pixels_to_draw = case[:, -1, :]
        
    pixels_to_draw[:] = 255
    


def draw_cross(M, i, j, color):
    
    case = extract_case(M, i, j)
    height, width, unused = case.shape
    case[:, width//2, :] = color
    case[height//2, :, :] = color
    
  

def draw_large_cross(M, i, j, color):
    
    case = extract_case(M, i, j)
    height, width, unused = case.shape
    eps = 0.1
    
    case[int((0.5 - eps) * height) : int((0.5 + eps) * height), :, :] = color
    case[:, int((0.5 - eps) * width) : int((0.5 + eps) * width), :]  = color


   
def average_case_color(M, i, j):
    return np.average(extract_case(M, i,j), axis=(0,1))

def average_case_interior_color(M, i, j):
    return np.average(extract_case_interior(M, i, j), axis=(0,1))




def find_closest_color_cases(M, colors, forbiden_cases_indexes):
    
    min_color_indexes = [None for i in range(4)]
    min_color_distances = [1000. for i in range(4)]
 
    for i in range(NB_CASES):
        for j in range(NB_CASES):
        
            if (i, j) in forbiden_cases_indexes:
                continue
        
            avg_color = average_case_interior_color(M, i, j)

            for k in range(4):
                    
                distance = np.linalg.norm(avg_color - colors[k])
                    
                if distance < min_color_distances[k]:
                    min_color_distances[k] = distance
                    min_color_indexes[k] = (i,j)
                    
    return min_color_indexes, min_color_distances
    




def process_picture(file_path):
    
    M = cv2.imread(file_path)
    output = cv2.imread(file_path)
    
    # Finding walls
    for i in range(NB_CASES):
        for j in range(NB_CASES): 
            for direction in range(4):
                if has_a_wall(M, i, j, direction):
                    draw_wall(output, i, j, direction)
                        
    # Finding robots

    robot_colors = [np.array([255., 85., 85.]), # Blue
                    np.array([0., 128., 0.]), # Green
                    np.array([0., 0., 255.]), # Red
                    np.array([31., 255., 252.]) #Yellow
                    ]

    forbiden_center_indexes = [(7,7), (7,8), (8,7), (8,8)]
        
    min_robot_color_indexes, min_robot_color_distances = find_closest_color_cases(M, robot_colors, 
                                                                                  forbiden_center_indexes)

    for k in range(4):
        draw_cross(output, *min_robot_color_indexes[k], robot_colors[k])
    
    # Finding goal

    goal_colors = [np.array([139., 0., 0.]), # Blue
                   np.array([144., 238., 144.]), # Green
                   np.array([203., 192., 255.]), # Red
                   np.array([31., 255., 252.]) #Yellow
                   ]    
    
    min_goal_color_indexes, min_goal_color_distances = find_closest_color_cases(M, goal_colors, 
                                                                                forbiden_center_indexes + min_robot_color_indexes)
 
    goal_color_id = np.argmin(min_goal_color_distances)
    goal_indexes = min_goal_color_indexes[goal_color_id]
    
    draw_large_cross(output, *goal_indexes, goal_colors[goal_color_id])
    
    return output
        

def show_processing(file_path):
    
    M = process_picture(file_path)
    cv2.imshow('processed grid', M)
    cv2.waitKey()




def grid_from_picture(file_path):
    
    output = grid.Grid(NB_CASES)
    
    M = cv2.imread(file_path)
    
    # Finding walls
    
    for i in range(NB_CASES):
        for j in range(NB_CASES): 
            for direction in range(4):
                if has_a_wall(M, i, j, direction):
                    output.put_wall(i, j, direction)
                        
    # Finding robots

    robot_colors = [np.array([255., 85., 85.]), # Blue
                    np.array([0., 128., 0.]), # Green
                    np.array([0., 0., 255.]), # Red
                    np.array([31., 255., 252.]) #Yellow
                    ]

    forbiden_center_indexes = [(7,7), (7,8), (8,7), (8,8)]
        
    min_robot_color_indexes, min_robot_color_distances = find_closest_color_cases(M, robot_colors, 
                                                                                  forbiden_center_indexes)

    for k in range(4):
        output.put_robot(*min_robot_color_indexes[k], k)
    
    # Finding goal

    goal_colors = [np.array([139., 0., 0.]), # Blue
                   np.array([144., 238., 144.]), # Green
                   np.array([203., 192., 255.]), # Red
                   np.array([31., 255., 252.]) #Yellow
                   ]    
    
    min_goal_color_indexes, min_goal_color_distances = find_closest_color_cases(M, goal_colors, 
                                                                                forbiden_center_indexes + min_robot_color_indexes)
 
    goal_color_id = np.argmin(min_goal_color_distances)
    goal_indexes = min_goal_color_indexes[goal_color_id]
    
    output.put_objective(*goal_indexes, goal_color_id)
    
    
    return output
















