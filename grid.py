# -*- coding: utf-8 -*-

import numpy as np
import grid_extractor
import grid_show


UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3



BLUE = 0
GREEN = 1
RED = 2
YELLOW = 3
    
NO_COLOR = 4


def opposite_direction(direction):
    return (direction + 2) % 4





class Node:
    
    def __init__(self, index, width):
        self.index = index
        self.i = index // width
        self.j = index % width
        self.objective_color = NO_COLOR 
        self.robot_color = NO_COLOR
        self.blocked_neighbours = np.zeros(4, dtype=np.uint8)




POWERS_OF_256 = [1, 256, 256**2, 256**3]
        
class Grid:
    
    @staticmethod
    def from_picture(file_path):
        return grid_extractor.grid_from_picture(file_path)

 
    def __init__(self, width):
        
        self.width = width
        
        self.node_list = []
        
        for node_index in range(width * width):
            self.node_list.append(Node(node_index, width))
            
        for i in range(width):
            self.node(i, 0).blocked_neighbours[LEFT] = 1
            self.node(0, i).blocked_neighbours[UP] = 1
            self.node(i, width-1).blocked_neighbours[RIGHT] = 1
            self.node(width-1, i).blocked_neighbours[DOWN] = 1
    
        self.robot_nodes = [None for i in range(4)]
        self.starting_robot_nodes = [None for i in range(4)]
        
        self.objective_node = None
        self.objective_color = NO_COLOR
        
        self._direction_to_neighbour_offset = np.array([-width, -1, width, 1], dtype = int)
        
        
        
    def set_next_cases_from_direction(self):
        
        self.next_index_from_direction = np.empty(self.width * self.width * 4, dtype = int)
        self.next_i_from_direction = np.empty(self.width * self.width * 4, dtype = int)
        self.next_j_from_direction = np.empty(self.width * self.width * 4, dtype = int)
        
        for node_index in range(self.width * self.width):
            for direction in range(4):
                next_index = self._step_by_step(node_index, direction)
                self.next_index_from_direction[direction + node_index * 4] = next_index
                self.next_i_from_direction[direction + node_index * 4] = next_index // self.width
                self.next_j_from_direction[direction + node_index * 4] = next_index % self.width
                
        
        
        
    def quick_move(self, robot_color, direction):
        
        begining_node = self.robot_nodes[robot_color] 
        begining_index = begining_node.index
        
        begining_i = begining_node.i
        begining_j = begining_node.j
        
        if direction == UP:
            
            final_i = self.next_i_from_direction[direction + begining_index * 4]
            final_j = begining_j
            
            for other_color in range(4):
                
                if other_color == robot_color:
                    continue
                
                other_node = self.robot_nodes[other_color]
                
                if other_node.j != begining_j:
                    continue
                
                other_i = other_node.i
                
                if final_i < other_i < begining_i:
                    final_i = other_i
            
                    
        elif direction == DOWN:
            
            final_i = self.next_i_from_direction[direction + begining_index * 4]
            final_j = begining_j
            
            for other_color in range(4):
                
                if other_color == robot_color:
                    continue
                
                other_node = self.robot_nodes[other_color]
                
                if other_node.j != begining_j:
                    continue
                
                other_i = other_node.i
                
                if begining_i < other_i < final_i:
                    final_i = other_i            
            
        elif direction == LEFT:
            
            final_j = self.next_j_from_direction[direction + begining_index * 4]
            final_i = begining_i
            
            for other_color in range(4):
                
                if other_color == robot_color:
                    continue
                
                other_node = self.robot_nodes[other_color]
                
                if other_node.i != begining_i:
                    continue
                
                other_j = other_node.j
                
                if final_j < other_j < begining_j:
                    final_j = other_j     
                    
                    
        elif direction == RIGHT:
            
            final_j = self.next_j_from_direction[direction + begining_index * 4]
            final_i = begining_i
            
            for other_color in range(4):
                
                if other_color == robot_color:
                    continue
                
                other_node = self.robot_nodes[other_color]
                
                if other_node.i != begining_i:
                    continue
                
                other_j = other_node.j
                
                if begining_j < other_j < final_j:
                    final_j = other_j                          
                    
        
        final_node = self.node_list[final_j + final_i * self.width]    
        begining_node.robot_color = NO_COLOR
        final_node.robot_color = robot_color
        self.robot_nodes[robot_color] = final_node
    
    
    
    
    
    def _step_by_step(self, node_index, direction):
        
        final_node = self.node_list[node_index]
        direction_to_neighbour_offset = self._direction_to_neighbour_offset[direction]
            
        while final_node.blocked_neighbours[direction] == 0: 
            final_node = self.node_list[final_node.index + direction_to_neighbour_offset]
           
        return final_node.index
        
       

    def get_state(self):
        
        output = 0
        
        for color_id in range(4):
            output += self.robot_nodes[color_id].index * POWERS_OF_256[color_id]
        
        return output
    
    
    def set_state(self, state):
        
        for i, node in enumerate(self.robot_nodes):
            node.robot_color = NO_COLOR
            self.robot_nodes[i] = None
            
        for color_id in range(4):
            node_index = state % 256
            node = self.node_list[node_index]
            node.robot_color = color_id
            self.robot_nodes[color_id] = node
            state //= 256
            

    def remove_robots(self):
        
        for node in self.robot_nodes:
            node.robot_color = NO_COLOR
            
        for i in range(4):
            self.robot_nodes[i] = None
        

    def show(self, window_name = 'Grid'):
        grid_show.show_picture(window_name, self)    


    def wait_key(self, delay):
        grid_show.wait_key(delay)

    
    def node(self, i, j):
        return self.node_list[j + i * self.width]
        
    

    def neighbour(self, node, direction):
    
        if node.blocked_neighbours[direction] == 1:
            return None
        
        return self.node_list[node.index + self._direction_to_neighbour_offset[direction]]
        

    def move(self, robot_color, direction):
        
        begining_node = self.robot_nodes[robot_color]
        final_node = begining_node
        direction_to_neighbour_offset = self._direction_to_neighbour_offset[direction]
            
        while 1:
            
            if final_node.blocked_neighbours[direction] == 1:
                break
                 
            next_node = self.node_list[final_node.index + direction_to_neighbour_offset]
           
            if next_node.robot_color != NO_COLOR:
                break
           
            final_node = next_node
            
        begining_node.robot_color = NO_COLOR
        final_node.robot_color = robot_color
        self.robot_nodes[robot_color] = final_node
       
        
    def put_robot(self, i, j, robot_color):
        
        node = self.node(i, j)
        node.robot_color = robot_color
        
        if robot_color != NO_COLOR:    
            self.robot_nodes[robot_color] = node    
            self.starting_robot_nodes[robot_color] = node
            
            
    def put_objective(self, i, j, objective_color):
        
        node = self.node(i, j)
        node.objective_color = objective_color
        
        self.objective_node = node
        self.objective_color = objective_color
            
            
    def put_wall(self, i, j, direction):
        
        node = self.node(i, j)
        neighbour = self.neighbour(node, direction)
        
        node.blocked_neighbours[direction] = 1
        
        if neighbour is not None:
            neighbour.blocked_neighbours[opposite_direction(direction)] = 1
            
            
    def is_won(self):
        return self.objective_node == self.robot_nodes[self.objective_color]
        
        
    def reset_to_starting_state(self):
        
        for node in self.robot_nodes:
            node.robot_color = NO_COLOR
            
        for color, node in enumerate(self.starting_robot_nodes):
            node.robot_color = color
            self.robot_nodes[color] = node
            
            
            
    def allowed_actions(self):
    
        output = []
    
        for color in range(4):
        
            robot_node = self.robot_nodes[color]
        
            for direction in range(4):
            
                if robot_node.blocked_neighbours[direction] == 1:
                    continue
                
                neighbour = self.node_list[robot_node.index + self._direction_to_neighbour_offset[direction]]
            
                if neighbour is None or neighbour.robot_color != NO_COLOR:
                    # There is a wall or a robot on the neighbour
                    continue
            
                output.append((color, direction))
            
        return output
            
        
            
    
        
        
        
            