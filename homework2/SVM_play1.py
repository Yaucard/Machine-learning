"""
The template of the main script of the machine learning process
"""
import numpy as np
import pickle
from pathlib import Path

import random
random_id = random.randint(0,100)
ball_position_history=[]

             
class MLPlay:
    def __init__(self):
 
        self.ball_served = False
        
    def update(self, scene_info):
             dir_path = Path(__file__).parent
             data_file_path = dir_path.joinpath("SVM_example.sav")
             with open(data_file_path, "rb") as f:
                 model = pickle.load(f)
             vx = 0
             vy = 0
                    
             platform_center_x = scene_info["platform"][0] +20
             ball_position_history.append(scene_info["ball"])
             if( len(ball_position_history) > 1):
                vy = ball_position_history[-1][1] - ball_position_history[-2][1]
                vx = ball_position_history[-1][0] - ball_position_history[-2][0]
             
             inp_temp=np.array([scene_info["ball"][0], scene_info["ball"][1], platform_center_x,vx,vy])
             input=inp_temp[np.newaxis, :]
            
             if(scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
                   return "RESET"
              
                                              
             if(len(ball_position_history) > 1):
                    move=model.predict(input)
             else:
                move = 0
                
             if not self.ball_served:
                self.ball_served = True
                if random_id%2 == 0:
                   command = "SERVE_TO_RIGHT"
                else:
                   command = "SERVE_TO_LEFT"

             else:
                 if move < 0 :
                     command = "MOVE_LEFT"
                 elif move > 0 :
                     command = "MOVE_RIGHT"            
                 else:
                     command = "NONE"
                     
             return command       
                     
             
    
    def reset(self):
        """
        Reset the status
        """
        global random_id
        random_id = random.randint(0,100)
        self.ball_served = False
