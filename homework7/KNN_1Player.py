"""
The template of the main script of the machine learning process
"""
import numpy as np
import pickle
import random

filename = "C:\\Users\\USER\\Desktop\\W3_6_8\\zxc1263426\\MLGame-master\\games\\pingpong\\ml\\knn_1P_20210105.sav" 
model = pickle.load(open(filename,'rb'))
ball_position_history = []
BallPosition=[]
ball_served_random=random.randrange(1,3)
wait_frame=0
        

class MLPlay:
    def __init__(self,side):
 
        self.ball_served = False
        self.side = side
        
    def update(self, scene_info):
             
     global wait_frame
     while True:
        if scene_info["status"] != "GAME_ALIVE":    #比出勝負
            return "RESET"  #遊戲重製
        if not self.ball_served:    #如果未發球
            self.ball_served = True
            #print("ball_pos:",scene_info["ball"])
            if(ball_served_random==1):
                return "SERVE_TO_RIGHT"  #往右發球
            else:
                return "SERVE_TO_LEFT"  #往左發球
                
        else:
            ball_position_history.append(scene_info["ball"])
            BallPosition=np.asarray(ball_position_history[-1])
            PlatX = np.asarray(scene_info["platform_1P"][-2])
            Ball_Vx=np.asarray(scene_info["ball_speed"][-2])
            Ball_Vy=np.asarray(scene_info["ball_speed"][-1])
            data_x = np.hstack((BallPosition,PlatX,Ball_Vx,Ball_Vy))
            input_data_x = data_x[np.newaxis, :]
            move = model.predict(input_data_x)
            #print(move)
            
            if(move <0):
                return "MOVE_LEFT"
            elif(move >0):
                return "MOVE_RIGHT"
            else:
                return "NONE"           
            return "NONE"
                     
             
    
    def reset(self):
        """
        Reset the status
        """
        global ball_served_random
        self.ball_served = False
        ball_served_random=random.randrange(1,3)
