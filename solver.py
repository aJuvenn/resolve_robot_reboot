# -*- coding: utf-8 -*-

import sys
from grid import Grid, LEFT, RIGHT, UP, DOWN, BLUE, RED, GREEN, YELLOW

import time



 

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
       
    
   
            
def solve(g : Grid, state, state_to_max_try, state_to_solution, max_try):
    
    if max_try == 0:  
        g.set_state(state)
        if g.is_won():
            return []
        return None
    
    solution = state_to_solution.get(state, None)
    
    if solution is not None:
        return solution
    
    state_max_try = state_to_max_try.get(state, 0)
    
    if state_max_try >= max_try:
        return None
    
    state_to_max_try[state] = max_try
    
    g.set_state(state)
    allowed_actions = g.allowed_actions()
    
    found_sub_solution = None
    found_action = None
     
    for action in allowed_actions:
    
        g.set_state(state)
        g.quick_move(*action)
        sub_state = g.get_state()
            
        sub_solution = solve(g, sub_state, state_to_max_try, state_to_solution, max_try - 1)
            
        if sub_solution is not None:
            if found_sub_solution is None or len(sub_solution) < len(found_sub_solution):
                found_sub_solution = sub_solution
                found_action = action
    
    if found_sub_solution is None:
        return None
    
    output = [found_action] + found_sub_solution
    state_to_solution[state] = output
    
    return output




def find_solution(g : Grid, max_solution_size):
    
    g.reset_to_starting_state()
    starting_state = g.get_state()
    
    state_to_max_try = dict()
    state_to_solution = dict()
    
    for max_try in range(max_solution_size + 1):
        
        start = time.time()
        print("Trying {} action length solutions...".format(max_try))
        
        sol = solve(g, starting_state, state_to_max_try, state_to_solution, max_try)
        
        if sol is not None:
            return sol
        
        stop = time.time()
        print("Research on {} action length solutions done in {} seconds.".format(max_try, stop - start))
        
        
    return None
        
        
    
    
    

if __name__ == '__main__':


    g = Grid.from_picture(sys.argv[1])
    g.show(sys.argv[1])
    g.wait_key(0)
    
    max_action_list_size = int(sys.argv[2])
    
    print('Solving...')
    
    solution = find_solution(g, max_action_list_size)
    
    if solution is None:
        print('No solution found in less than {} moves'.format(max_action_list_size))
        exit()
    
    print_action_list(solution)
    
    while True:
        
        g.reset_to_starting_state()
        g.show(sys.argv[1])
        g.wait_key(2000)
        
        for action in solution:
            g.wait_key(1000)
            g.move(*action)
            g.show(sys.argv[1])
        
        g.wait_key(2000)
    
    
    
    
    
    
    
    
    
    
    