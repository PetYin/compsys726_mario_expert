"""
This the primary class for the Mario Expert agent. It contains the logic for the Mario Expert agent to play the game and choose actions.

Your goal is to implement the functions and methods required to enable choose_action to select the best action for the agent to take.

Original Mario Manual: https://www.thegameisafootarcade.com/wp-content/uploads/2017/04/Super-Mario-Land-Game-Manual.pdf
"""

import json
import logging
import random
import numpy as np
import time

import cv2
from mario_environment import MarioEnvironment
from pyboy.utils import WindowEvent



# Function to check if there is a non-zero value in front of a 1
def check_monsters(game_area):
    for i in range(game_area.shape[0]):  # Iterate over rows
        for j in range(1, game_area.shape[1]):  # Start from the second column
            if game_area[i, j] == 1 and game_area[i, j-1] != 0:
                return True
    return False

# Function to search the area around a specific coordinate (i, j)
def search_coordinate(game_area, coord, radius, target_value):
    i, j = coord
    found_positions = []
    # Define the range for the neighborhood
    for x in range(max(0, i - radius), min(game_area.shape[0], i + radius + 1)):
        for y in range(max(0, j - radius), min(game_area.shape[1], j + radius + 1)):
            if game_area[x, y] == target_value:
                found_positions= [x, y]
    
    return found_positions
# Function to search the area below a specific coordinate (i, j)
def cordBelow(game_area, coord, target_value):
    i, j = coord
    found_positions = False
    
    # Define the range for the search below the coordinate
    for x in range(i + 1, game_area.shape[0]):
        if game_area[x, j] == target_value:
            found_positions = True
            break
    
    return found_positions

# Function to search the area below a specific coordinate (i, j)
def cordAbove(game_area, coord, target_value):
    i, j = coord
    found_positions = False
    
    # Define the range for the search below the coordinate
    for x in range(i - 1, 0, -1):  # Move upwards from the coordinate
        for y in range(j + 1, game_area.shape[1]-1, +1):  # Move upwards from the coordinate
            if game_area[x, y] == target_value:
                found_positions = True
                break
    
    return found_positions
# Function to search the area below a specific coordinate (i, j)
def cordBehind(game_area, coord, target_value):
    i, j = coord
    found_positions = False
    
     # Define the range for the search below the coordinate
    for x in range(i - 1, 0, -1):  # Move upwards from the coordinate
        for y in range(j - 1, 0, -1):  # Move upwards from the coordinate
            if game_area[x, y] == target_value:
                found_positions = True
                break
    
    return found_positions
class MarioController(MarioEnvironment):
    """
    The MarioController class represents a controller for the Mario game environment.

    You can build upon this class all you want to implement your Mario Expert agent.

    Args:
        act_freq (int): The frequency at which actions are performed. Defaults to 10.
        emulation_speed (int): The speed of the game emulation. Defaults to 0.
        headless (bool): Whether to run the game in headless mode. Defaults to False.
    """

    def __init__(
        self,
        act_freq: int = 10,
        emulation_speed: int = 5,
        headless: bool = False,
    ) -> None:
        super().__init__(
            act_freq=act_freq,
            emulation_speed=emulation_speed,
            headless=headless,
        )

        self.act_freq = act_freq

        # Example of valid actions based purely on the buttons you can press
        valid_actions: list[WindowEvent] = [
            WindowEvent.PRESS_ARROW_DOWN,
            WindowEvent.PRESS_ARROW_LEFT,
            WindowEvent.PRESS_ARROW_RIGHT,
            WindowEvent.PRESS_ARROW_UP,
            WindowEvent.PRESS_BUTTON_A,
            WindowEvent.PRESS_BUTTON_B,
        ]

        release_button: list[WindowEvent] = [
            WindowEvent.RELEASE_ARROW_DOWN,
            WindowEvent.RELEASE_ARROW_LEFT,
            WindowEvent.RELEASE_ARROW_RIGHT,
            WindowEvent.RELEASE_ARROW_UP,
            WindowEvent.RELEASE_BUTTON_A,
            WindowEvent.RELEASE_BUTTON_B,
        ]

        self.valid_actions = valid_actions
        self.release_button = release_button

    def run_action(self, action: int) -> None:
        """
        This is a very basic example of how this function could be implemented

        As part of this assignment your job is to modify this function to better suit your needs

        You can change the action type to whatever you want or need just remember the base control of the game is pushing buttons
        """

        # Simply toggles the buttons being on or off for a duration of act_freq
        self.pyboy.send_input(self.valid_actions[action])

        # This is the frequency at which the actions are performed according to the act_freq
        for _ in range(self.act_freq):
            self.pyboy.tick()

        self.pyboy.send_input(self.release_button[action])


class MarioExpert:
    """
    The MarioExpert class represents an expert agent for playing the Mario game.

    Edit this class to implement the logic for the Mario Expert agent to play the game.

    Do NOT edit the input parameters for the __init__ method.

    Args:
        results_path (str): The path to save the results and video of the gameplay.
        headless (bool, optional): Whether to run the game in headless mode. Defaults to False.
    """

    def __init__(self, results_path: str, headless=False):
        self.results_path = results_path

        self.environment = MarioController(headless=headless)
        self.flag1 = False
        self.video = None

    def choose_action(self):
        state = self.environment.game_state()
        frame = self.environment.grab_frame()
        game_area = self.environment.game_area()
        print(f"State: {state}")
        # print(f"Frame: {frame}")
        print(f"Game Area: {game_area}")
        # Implement your code here to choose the best action
        # time.sleep(0.1)
        action = 2 # Example action
        
        # Read Mario Location
        marioX = 0
        marioY = 0
        print(f"Game Area Shape: {game_area.shape}")
        # Iterate through the array and update the leftmost and bottommost coordinates
        for x in range(game_area.shape[0]):
            for y in range(game_area.shape[1]):
                if game_area[x,y] == 1:  # Mario
                    marioX = x
                    marioY = y
        print(f"Mario Location: ({marioX}, {marioY})")

       
        # Check if the x position of game is less than 600
        if state['x_position'] < 650 and state['stage'] == 1:
            #Check if a monster is approaching Mario
            if (game_area[marioX, marioY+3] == 15 or game_area[marioX, marioY+4] == 15 or game_area[marioX, marioY+5] == 15 or game_area[marioX, marioY+6] == 15):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 15 or game_area[marioX, marioY+1] == 15):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 15) or cordBelow(game_area, [marioX, marioY], 15) or cordBelow(game_area, [marioX, marioY-1], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            # Search for the treasure
            elif (search_coordinate(game_area, [marioX, marioY], 10, 6)!=[]):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if there is a block of 13 is above and behind or not
            elif ((game_area[marioX-3, marioY-1] == 13)or(game_area[marioX-2, marioY-1] == 13)or(game_area[marioX-4, marioY-1] == 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
            #Check if Mario is blocked by a tube or not
            elif (game_area[marioX, marioY+2] == 14):
                # if yes then jump
                action = 4
                print("Jumping for tube")
            #Check if Mario is blocked by a wall or not
            elif (game_area[marioX, marioY+2] == 10):
                # if yes then jump
                action = 4
                print("Jumping for wall")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 750 and state['stage'] == 1:
            #Check if a monster is approaching Mario
            if (game_area[marioX, marioY+3] == 15 or game_area[marioX, marioY+4] == 15 or game_area[marioX, marioY+5] == 15 or game_area[marioX, marioY+6] == 15):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 15 or game_area[marioX, marioY+1] == 15):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 15) or cordBelow(game_area, [marioX, marioY], 15) or cordBelow(game_area, [marioX, marioY-1], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            # Search for future monsters
            elif (cordAbove(game_area, [marioX, marioY], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if Mario is blocked by a wall or not
            elif (game_area[marioX, marioY+2] == 10):
                # if yes then jump
                action = 4
                print("Jumping for wall")
        elif state['x_position'] < 830 and state['stage'] == 1:
            #Check if a monster is approaching Mario
            if (game_area[marioX, marioY+3] == 15 or game_area[marioX, marioY+4] == 15 or game_area[marioX, marioY+5] == 15 or game_area[marioX, marioY+6] == 15):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 15 or game_area[marioX, marioY+1] == 15):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 15) or cordBelow(game_area, [marioX, marioY], 15) or cordBelow(game_area, [marioX, marioY-1], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if there is a block of 13 is above and behind or not
            elif ((game_area[marioX-3, marioY-1] == 13)or(game_area[marioX-2, marioY-1] == 13)or(game_area[marioX-4, marioY-1] == 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
            # Search for future monsters
            elif (cordAbove(game_area, [marioX, marioY], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if Mario is blocked by a wall or not
            elif (game_area[marioX, marioY+2] == 10):
                # if yes then jump
                action = 4
                print("Jumping for wall")
            #Check if Mario is blocked by a tube or not
            elif (game_area[marioX, marioY+2] == 14):
                # if yes then jump
                action = 4
                print("Jumping for tube")
        elif state['x_position'] < 920 and state['score'] < 2850  and state['stage'] == 1:
            #Check if Mario is blocked by a plate or not
            if (game_area[marioX-1, marioY+2] == 12):
                # if yes then jump
                action = 4
                print("Jumping for plate")
            elif (game_area[marioX-1, marioY+2] == 13):
                # if yes then jump
                action = 4
                print("Jumping for plate")
            # Check if the next one is 12 followed by 0
            elif (game_area[marioX+1, marioY+1] == 12 and game_area[marioX+1, marioY+2] == 0):
                # if yes then jump
                action = 4
                print("Jumping for plate")
            #Check if there is a block of 13 is above and behind or not
            elif (cordBehind(game_area, [marioX, marioY+1], 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
            # Check if all area under is 0 or not
            elif (game_area[15, marioY+3] == 0 or game_area[15, marioY+4] == 0):
                # if yes then hold
                action = 3
                print("Holding for hole")
            # Check if all area under is 0 or not
            elif (game_area[15, marioY+2] == 0 or game_area[15, marioY+3] == 0):
                # if yes then hold
                action = 1
                print("left for hole")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 980 and state['stage'] == 1:
            if (game_area[15, marioY+1] == 0 or game_area[15, marioY+2] == 0):
                # if yes then hold
                action = 4
                print("Jumping for hole")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 1100 and state['stage'] == 1:
            #Check if Mario is blocked by a tube or not
            if (game_area[marioX, marioY+2] == 14):
                # if yes then jump
                action = 4
                print("Jumping for tube")
            else:
                action = 2
                print("Moving forward")
        # elif state['x_position'] < 1100 and state['score'] == 2850:
        #     if (game_area[marioX-1, marioY-6] == 12):
        #         # if yes then jump
        #         action = 4
        #         print("Jumping for plate")
        #     elif(game_area[marioX+1, marioY-2] == 12):
        #         # if yes then go left
        #         action = 1
        #         print("Left for coin")
        #     elif(cordBehind(game_area, [marioX, marioY-1], 13)):
        #         # if yes then go left
        #         action = 1
        #         print("Left for coin")
        #     #Check if the Mario is under the block of value 13 or not within 2 units
        #     elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
        #         action = 4
        #         print("Jumping for coin")
        #     else:
        #         action = 2
        #         print("Moving forward")
        elif state['x_position'] < 1400 and state['stage'] == 1:
            if (game_area[15, marioY+1] == 0 or game_area[15, marioY] == 0):
                # if yes then hold
                action = 4
                print("Jumping for hole")
            #Check if Mario is blocked by a tube or not
            elif (game_area[marioX, marioY+1] == 14 and state['time'] < 335):
                # if yes then jump
                action = 4
                print("Jumping for tube")
            elif (game_area[marioX, marioY+3] == 16 or game_area[marioX, marioY+4] == 16 or game_area[marioX, marioY+5] == 16 or game_area[marioX, marioY+6] == 16):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 16 or game_area[marioX, marioY+1] == 16):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 16) or cordBelow(game_area, [marioX, marioY], 16) or cordBelow(game_area, [marioX, marioY-1], 16)):
                # if true then hold
                action = 3
                print("Holding for monster")
            # Search for the treasure
            elif (search_coordinate(game_area, [marioX, marioY], 10, 6)!=[]):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if there is a block of 13 is above and behind or not
            elif ((game_area[marioX-3, marioY-1] == 13)or(game_area[marioX-2, marioY-1] == 13)or(game_area[marioX-4, marioY-1] == 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
        elif state['x_position'] < 1450 and state['stage'] == 1:
            if (game_area[marioX, marioY+3] == 15 or game_area[marioX, marioY+4] == 15 or game_area[marioX, marioY+5] == 15 or game_area[marioX, marioY+6] == 15):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 15 or game_area[marioX, marioY+1] == 15):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 15) or cordBelow(game_area, [marioX, marioY], 15) or cordBelow(game_area, [marioX, marioY-1], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if there is a block of 13 is above and behind or not
            elif ((game_area[marioX-3, marioY-1] == 13)or(game_area[marioX-2, marioY-1] == 13)or(game_area[marioX-4, marioY-1] == 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 1500 and state['stage'] == 1:
            if (game_area[marioX, marioY+3] == 18 or game_area[marioX, marioY+4] == 18 or game_area[marioX, marioY+5] == 18 or game_area[marioX, marioY+6] == 18):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 18 or game_area[marioX, marioY+1] == 18):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 18) or cordBelow(game_area, [marioX, marioY], 18) or cordBelow(game_area, [marioX, marioY-1], 18)):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if there is a block of 13 is above and behind or not
            elif ((game_area[marioX-3, marioY-1] == 13)or(game_area[marioX-2, marioY-1] == 13)or(game_area[marioX-4, marioY-1] == 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 1615 and state['stage'] == 1:
             #Check if Mario is blocked by a tube or not
            if (game_area[marioX, marioY+2] == 14):
                # if yes then jump
                action = 4
                print("Jumping for tube")
            elif (game_area[marioX, marioY+2] == 10):
                # if yes then jump
                action = 4
                print("Jumping for tube")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 1650 and state['stage'] == 1:
            #Check if a monster is approaching Mario
            if (game_area[marioX, marioY+3] == 15 or game_area[marioX, marioY+4] == 15 or game_area[marioX, marioY+5] == 15 or game_area[marioX, marioY+6] == 15):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 15 or game_area[marioX, marioY+1] == 15):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 15) or cordBelow(game_area, [marioX, marioY], 15) or cordBelow(game_area, [marioX, marioY-1], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            #Check if there is a block of 13 is above and behind or not
            elif ((game_area[marioX-3, marioY-1] == 13)or(game_area[marioX-2, marioY-1] == 13)or(game_area[marioX-4, marioY-1] == 13)):
                # if yes then go left
                action = 1
                print("Left for coin")
            #Check if the Mario is under the block of value 13 or not within 2 units
            elif ((game_area[marioX-3, marioY+1] == 13)or(game_area[marioX-2, marioY+1] == 13)or(game_area[marioX-4, marioY+1] == 13) or(game_area[marioX-5, marioY+1] == 13)):
                action = 4
                print("Jumping for coin")
            # Search for future monsters
            elif (cordAbove(game_area, [marioX, marioY], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            else:
                action = 2
                print("Moving forward")
        elif state['x_position'] < 1870 and state['stage'] == 1:
            #Check if a monster is approaching Mario
            if (game_area[marioX, marioY+3] == 15 or game_area[marioX, marioY+4] == 15 or game_area[marioX, marioY+5] == 15 or game_area[marioX, marioY+6] == 15):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+2] == 15 or game_area[marioX, marioY+1] == 15):
                # if yes then jump
                action = 4
                print("Jumping for monster")
            elif (cordBelow(game_area, [marioX, marioY+1], 15) or cordBelow(game_area, [marioX, marioY], 15) or cordBelow(game_area, [marioX, marioY-1], 15)):
                # if true then hold
                action = 3
                print("Holding for monster")
            elif (game_area[marioX, marioY+1] == 10 or game_area[marioX, marioY+2] == 10):
                # if yes then hold
                action = 4
            elif (game_area[marioX, marioY+1] == 14 or game_area[marioX, marioY+2] == 14):
                # if yes then hold
                action = 4
            else:
                action = 2
        elif state['x_position'] < 2000 and state['time'] <= 381 and state['stage'] == 1:
            if (game_area[marioX+1, marioY] == 14 or game_area[marioX+1, marioY-1] == 14):
                # if yes then hold
                action = 4
            elif (game_area[marioX, marioY+1] == 10 or game_area[marioX, marioY+2] == 10):
                # if yes then hold
                action = 4
            elif (game_area[marioX, marioY+2] == 14):
                # if yes then jump
                action = 4
            else:
                action = 2
        elif 2000<state['x_position'] < 2100 and state['stage'] == 1:
            if (game_area[marioX, marioY+3] == 18 or game_area[marioX, marioY+4] == 18 or game_area[marioX, marioY+5] == 18 or game_area[marioX, marioY+6] == 18):
                # if true then hold
                action = 3
            elif (game_area[marioX, marioY+2] == 18 or game_area[marioX, marioY+1] == 18):
                # if yes then jump
                action = 4
            elif (cordBelow(game_area, [marioX, marioY+1], 18) or cordBelow(game_area, [marioX, marioY], 18) or cordBelow(game_area, [marioX, marioY-1], 18)):
                # if true then hold
                action = 3
            else :
                action = 2
        elif 2100<state['x_position'] < 2150 and state['time'] <= 372 and state['stage'] == 1:
            if (game_area[marioX, marioY+3] == 18 or game_area[marioX, marioY+4] == 18 or game_area[marioX, marioY+5] == 18 or game_area[marioX, marioY+6] == 18):
                # if true then hold
                action = 3
            elif (game_area[marioX, marioY+2] == 18 or game_area[marioX, marioY+1] == 18):
                # if yes then jump
                action = 4
            elif (cordBelow(game_area, [marioX, marioY+1], 18) or cordBelow(game_area, [marioX, marioY], 18) or cordBelow(game_area, [marioX, marioY-1], 18)):
                # if true then hold
                action = 3
            else :
                action = 2
        elif 2150<state['x_position'] < 2250 and state['stage'] == 1:
            if (game_area[15, marioY+1] == 0):
                # if yes then hold
                action = 4
            elif (game_area[marioX, marioY+2] == 10 or game_area[marioX, marioY+1] == 10):
                # if yes then jump
                action = 4
            else :
                action = 2
        elif 2250<state['x_position'] < 2500 and state['stage'] == 1:
            if (game_area[15, marioY+1] == 0 or game_area[15, marioY] == 0):
                # if yes then hold
                action = 4
            elif (game_area[marioX, marioY+2] == 10 or game_area[marioX, marioY+1] == 10):
                # if yes then jump
                action = 4
            elif (game_area[marioX-1, marioY+2] == 10 or game_area[marioX-1, marioY+1] == 10):
                # if yes then jump
                action = 4
            else:
                action = 2
        elif 2500<state['x_position'] < 2600 and state['stage'] == 1:
            action = 2
        else:
            action = 3
            print("Holding")
            
        return action

    def step(self):
        """
        Modify this function as required to implement the Mario Expert agent's logic.

        This is just a very basic example
        """

        # Choose an action - button press or other...
        action = self.choose_action()

        # Run the action on the environment
        self.environment.run_action(action)

    def play(self):
        """
        Do NOT edit this method.
        """
        self.environment.reset()

        frame = self.environment.grab_frame()
        height, width, _ = frame.shape

        self.start_video(f"{self.results_path}/mario_expert.mp4", width, height)

        while not self.environment.get_game_over():
            frame = self.environment.grab_frame()
            self.video.write(frame)

            self.step()

        final_stats = self.environment.game_state()
        logging.info(f"Final Stats: {final_stats}")

        with open(f"{self.results_path}/results.json", "w", encoding="utf-8") as file:
            json.dump(final_stats, file)

        self.stop_video()

    def start_video(self, video_name, width, height, fps=30):
        """
        Do NOT edit this method.
        """
        self.video = cv2.VideoWriter(
            video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

    def stop_video(self) -> None:
        """
        Do NOT edit this method.
        """
        self.video.release()
