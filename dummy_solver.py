# -*- coding: utf-8 -*-

import sys
from grid import Grid, LEFT, RIGHT, UP, DOWN, BLUE, RED, GREEN, YELLOW




def color_to_name(color):
    
    if color == BLUE:
        return 'BLUE'
    
    if color == RED:
        return 'RED'   
    
    if color == GREEN:
        return 'GREEN'
    
    if color == YELLOW:
        return 'YELLOW'    
    
    
    
def position_to_name(position):
    
    if position == LEFT:
        return 'LEFT'
    
    if position == RIGHT:
        return 'RIGHT'   
    
    if position == UP:
        return 'UP'
    
    if position == DOWN:
        return 'DOWN'        
    
    
    

    




def print_action_list(action_list):
    
    for color, position in action_list:
        print("({}, {}) ".format(color_to_name(color), position_to_name(position)))
    
    
def play_action_list(g : Grid, action_list):
    
    g.reset_to_starting_state()
    
    for (color, direction) in action_list:
        g.move(color, direction)
        
    
    
def action_list_suceed(g : Grid, action_list):
    
    play_action_list(g, action_list)
    
    return g.is_won()
        
    
    

def add_one_action_to_action_lists(action_lists):
    
    output = []
    
    if action_lists == []:
        for color in range(4):
            for position in range(4):
                output.append([(color, position)])
        return output
    
    
    for action_list in action_lists:
        for color in range(4):
            for position in range(4):
                new_action_list = action_list + [(color, position)]
                output.append(new_action_list)
                
    return output
                
            

def find_solution(g : Grid, max_action_list_size):
    
    action_lists = []
    
    for i in range(max_action_list_size+1):
        
        action_lists = add_one_action_to_action_lists(action_lists)
        
        for action_list in action_lists:
            if action_list_suceed(g, action_list):
                return action_list
        
    return None
    
    



def code_to_action(n):
    return (n//4, n%4)


def action_to_code(action):
    return 4*action[0] + action[1]
    
    

def update_to_next_action_list(action_list):
    
    
    for i, action in enumerate(action_list):
        
        code = action_to_code(action)
        
        if code < 15:
            # can be just increased, returning
            action_list[i] = code_to_action(code+1)
            return
        
        # must be set to zero, the loop continue on the next value
        action_list[i] = code_to_action(0)    
    
    # If we are here, a new element must be added    
    action_list.append(code_to_action(0))
    
        
        
        

def find_solution_bis(g : Grid, max_action_list_size):
    
    action_list = []
    
    while len(action_list) <= max_action_list_size:
        
        update_to_next_action_list(action_list)
        
        if action_list_suceed(g, action_list):
            return action_list
        
    return None


if __name__ == '__main__':


    g = Grid.from_picture(sys.argv[1])
    
    max_action_list_size = int(sys.argv[2])
    
    print('Solving...')
    
    solution = find_solution_bis(g, max_action_list_size)
    
    if solution is None:
        print('No solution found in less than {} moves'.format(max_action_list_size))
        exit()
    
    print_action_list(solution)
    
    while True:
        
        g.reset_to_starting_state()
        g.show()
        g.wait_key(2000)
        
        for action in solution:
            g.wait_key(1000)
            g.move(*action)
            g.show()
        
        g.wait_key(2000)
        
        
        
        
        
    
    
    
    
    
    

    