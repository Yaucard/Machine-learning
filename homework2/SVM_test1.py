# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 11:38:52 2020

@author: USER
"""
import pickle
import numpy as np
from os import listdir
from os.path import isfile, join


def print_log():
        path = 'C:\\Users\\USER\\Desktop\\W3_6_8\\zxc1263426\\MLGame-master\\games\\arkanoid\\log'
        Frame = []
        Status = []
        BallPosition = []
        PlatformPosition = []
        Brick = []
        n=0
        files = listdir(path)    ## import os 取路徑底下檔名


        for f in files:         ##將路徑底下的檔名與路徑結合
            allpath = join(path, f)
            if isfile(allpath):
                with open(allpath , "rb") as f1:
        
                        data_list1 = pickle.load(f1)     
                        for ml_name in data_list1.keys():
                            if ml_name == "record_format_version":
                                continue

                target_record = data_list1[ml_name]
                for n in range(0,len(target_record["scene_info"])):
                    BallPosition.append(target_record["scene_info"][n]["ball"])
                    PlatformPosition.append(target_record["scene_info"][n]["platform"])
                    Frame.append(target_record["scene_info"][n]["frame"])
                    Status.append(target_record["scene_info"][n]["status"])
                    Brick.append(target_record["scene_info"][n]["bricks"])

###############################################################################
        PlatX = np.array(PlatformPosition) [:,0][:,np.newaxis]
        PlatX_next = PlatX[1:,:]
        instrust = (PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5

        PlatY = np.array(PlatformPosition) [:,1][:,np.newaxis]
        PlatY_next = PlatY[1:,:]

        Ballarray = np.array(BallPosition[:-1])

        BallX_position = np.array(BallPosition)[:,0][:,np.newaxis]
        BallX_position_next = BallX_position[1:,:]
        Ball_Vx = BallX_position_next - BallX_position[0:len(BallX_position_next),0][:,np.newaxis]

        BallY_position = np.array(BallPosition)[:,1][:,np.newaxis]
        BallY_position_next = BallY_position[1:,:]
        Ball_Vy = BallY_position_next - BallY_position[0:len(BallY_position_next),0][:,np.newaxis]
        
        Ball_Plat_Y = PlatY_next-BallY_position_next

        x = np.hstack((Ballarray,PlatX[0:-1,0][:,np.newaxis],Ball_Vx,Ball_Vy))
        y = instrust
#--------------------------- train & test data
        from sklearn.model_selection import train_test_split
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 41)
#--------------------------- train model
        from sklearn.svm import SVR
        svr = SVR(gamma=0.001,C = 1,epsilon = 0.1,kernel = 'rbf')
        svr.fit(x_train,y_train)
        y_predict = svr.predict(x_test)
        from sklearn.metrics import r2_score #R square
        R2 = r2_score(y_test,y_predict)
        print('R2 = ',R2)
        print(len(BallPosition))
#--------------------------- save
        filename = "C:\\Users\\USER\\Desktop\\W3_6_8\\zxc1263426\\MLGame-master\\games\\arkanoid\\ml\\SVM_example.sav"
        pickle.dump(svr,open(filename,"wb"))
if __name__ == "__main__":
    print_log()