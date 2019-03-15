import numpy as np
import random
import matplotlib.pyplot as plt
import os
'''
ConnectX game.
Author: Max Croci
Date: 15.03.2019
'''

class Board:
    variant = 0
    n_rows = 0
    n_cols = 0
    positions = {}      #Dictionary of symbols (values) at positions (keys)
    available_moves = []#List of available moves
    visited_states = [] #List of visited states
    filled_positions =[]#List of positions filled from chosen moves
    chosen_moves = []   #List of moves that have been made

    def __init__(self,variant):
        self.positions = {}
        self.visited_states = []
        self.filled_positions = []
        self.chosen_moves = []
        if variant == "3":
            self.n_rows = 4
            self.n_cols = 4
            self.variant = variant
        elif variant == "4":
            self.n_rows = 6
            self.n_cols = 7
            self.variant = variant

        self.available_moves = [i + 1 for i in range(self.n_cols)]
        for i in range(self.n_rows*self.n_cols):
            self.positions[i+1] = "_"
        self.visited_states.append("_"*self.n_rows*self.n_cols)

    def print_board(self):
        for i in range(self.n_rows):
            row = ""
            for j in range(self.n_cols):
                row += self.positions[1+self.n_cols*i+j]
            print(row)
    
    def move_to_position(self,move): 
        cur_state = self.visited_states[-1]
        for i in range(self.n_rows-1,-1,-1):
            if cur_state[move+i*self.n_cols-1] == "_":
                position = move+i*self.n_cols
                self.filled_positions.append(position)
                self.chosen_moves.append(move)
                return position

    def update(self,move,symbol):
        position = self.move_to_position(move)
        self.positions[position] = symbol
        if position <= self.n_cols:
            self.available_moves.remove(move)

        state = ""
        for i in range(self.n_rows*self.n_cols):
            state += self.positions[1+i]
        
        self.visited_states.append(state)

    def get_next_possible_states(self, symbol):
        cur_state = self.visited_states[-1]
        moves = self.available_moves
        next_possible_states = {} #Dict keyed by moves, values are states
        for move in moves:
            for i in range(self.n_rows-1,-1,-1):
                if move not in next_possible_states:
                    if cur_state[move+i*self.n_cols-1] == "_":
                        new_state = cur_state[:move+i*self.n_cols-1]\
                                + symbol\
                                + cur_state[move+i*self.n_cols:]
                        next_possible_states[move] = new_state
        
        return next_possible_states

    def check_victory(self, symbol):
        last_filled_pos = self.filled_positions[-1] #Only need to check for win around last position
        last_move = self.chosen_moves[-1]
        last_move_row = int(np.floor(1+(last_filled_pos-1)/self.n_cols))
        last_move_col = (last_filled_pos-1)%self.n_cols + 1
        
        if self.variant == "3":
            if last_filled_pos <= 8: #Check vertical if in top two rows
                if self.positions[last_filled_pos] == self.positions[last_filled_pos+self.n_cols]\
                        and self.positions[last_filled_pos] == self.positions[last_filled_pos+self.n_cols*2]:
                    #print("Game is won vertically!")
                    return True

            for i in range (1,self.n_cols-1): #check horizontal
                if self.positions[i+(last_move_row-1)*self.n_cols] != "_"\
                        and self.positions[i+(last_move_row-1)*self.n_cols] == self.positions[i+1+(last_move_row-1)*self.n_cols]\
                        and self.positions[i+(last_move_row-1)*self.n_cols] == self.positions[i+2+(last_move_row-1)*self.n_cols]:
                    #print("Win horizontally!")
                    return True

            #Check diagonals
            itmp = [1, 2, 5, 6]
            istarts = [i for i in itmp if i in self.filled_positions]
            for i in istarts:
                if self.positions[i] == self.positions[i+self.n_cols+1]\
                        and self.positions[i] == self.positions[i+self.n_rows*2+2]:
                    #print("Win -ve diag")
                    return True

            itmp = [3, 4, 7, 8]
            istarts = [i for i in itmp if i in self.filled_positions]
            for i in istarts:
                if self.positions[i] == self.positions[i+self.n_cols-1]\
                        and self.positions[i] == self.positions[i+self.n_rows*2-2]:
                    #print("Win +ve diag")
                    return True
            return False
        
        elif self.variant == "4":
            if last_filled_pos <= 21: #Check vertical if in top three rows
                if self.positions[last_filled_pos] == self.positions[last_filled_pos+self.n_cols]\
                        and self.positions[last_filled_pos] == self.positions[last_filled_pos+self.n_cols*2]\
                        and self.positions[last_filled_pos] == self.positions[last_filled_pos+self.n_cols*3]:
                    #print("Game is won vertically!")
                    return True

            for i in range (1,self.n_cols-2): #check horizontal
                if self.positions[i+(last_move_row-1)*self.n_cols] != "_"\
                        and self.positions[i+(last_move_row-1)*self.n_cols] == self.positions[i+1+(last_move_row-1)*self.n_cols]\
                        and self.positions[i+(last_move_row-1)*self.n_cols] == self.positions[i+2+(last_move_row-1)*self.n_cols]\
                        and self.positions[i+(last_move_row-1)*self.n_cols] == self.positions[i+3+(last_move_row-1)*self.n_cols]:
                    #print("Win horizontally!")
                    return True

            #Check diagonals
            itmp = [1, 2, 3, 4, 8, 9, 10, 11, 15, 16, 17, 18]
            istarts = [i for i in itmp if i in self.filled_positions]
            for i in istarts:
                if self.positions[i] == self.positions[i+8]\
                        and self.positions[i] == self.positions[i+16]\
                        and self.positions[i] == self.positions[i+24]:
                    #print("Win -ve diag")
                    return True

            itmp = [4, 5, 6, 7, 11, 12, 13, 14, 18, 19, 20, 21]
            istarts = [i for i in itmp if i in self.filled_positions]
            for i in istarts:
                if self.positions[i] == self.positions[i+6]\
                        and self.positions[i] == self.positions[i+12]\
                        and self.positions[i] == self.positions[i+18]:
                    #print("Win +ve diag")
                    return True
            return False

        else:
            print("Warning: unrecognised variant!")
            return False

class Bot:
    symbol = "" # "X" or "O"
    win = 0   # win = 1 if bot wins
    V = {}      # Estimated value of states (keys)
    num_wins = 0# Track number of bot wins
    tau = 1     #"Heat" controls exploration v exploitation
    training = True

    def __init__(self,symbol,V,num_wins,tau,training):
        self.symbol = symbol
        self.win = -1
        self.num_wins = num_wins
        self.V = V
        self.tau = tau
        self.training = training
    
    def get_move(self, board):
        next_possible_states = board.get_next_possible_states(self.symbol)
        candidate_moves = []
        candidate_V = []
        candidate_probabilities = []
        
        for poss_move, poss_state in next_possible_states.items():
            if poss_state not in self.V.keys():
                self.V[poss_state] = 0

            candidate_moves.append(poss_move)
            candidate_V.append(self.V[poss_state])


        if self.training:
            candidate_V[:] = [x/self.tau for x in candidate_V]
            candidate_probabilities = list(np.exp(candidate_V)/sum(np.exp(candidate_V)))
            move = int(np.random.choice(candidate_moves,1,candidate_probabilities))
        
        else:
            max_V = max(candidate_V)
            possible_moves = [candidate_moves[i] for i,j in enumerate(candidate_V) if j == max_V]
            move = np.random.choice(possible_moves)

        return move

    def update_V(self,board,REWARD,LEARN_RATE):
        final_state = board.visited_states[-1]
        self.V[final_state] = REWARD*self.win
        for state in board.visited_states:
            if state not in self.V:
                self.V[state] = 0

        n_states_visited = len(board.visited_states)
        for i in range(n_states_visited-1):
            state = board.visited_states[n_states_visited -i -2]
            next_state = board.visited_states[n_states_visited -i -1]
            self.V[state] = self.V[state] + LEARN_RATE*(self.V[next_state] - self.V[state])

        #Mirror states - make use of symmetry
        mirror_visited_states = []
        for state in board.visited_states:
            mirror_state = state[board.n_cols-1::-1]
            for i in range(1,board.n_rows,1):
                mirror_row = state[(i+1)*board.n_cols-1:i*board.n_cols-1:-1]
                mirror_state = mirror_state + mirror_row
        
            self.V[mirror_state] = self.V[state]

