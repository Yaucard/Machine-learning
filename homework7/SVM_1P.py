import pickle
import numpy as np
from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import r2_score
def print_log():
#-----------------------------------------------------------------------------------------------------------------------------------#   
     path = 'C:\\Users\\USER\\Desktop\\W3_6_8\\zxc1263426\\MLGame-master\\games\\pingpong\\log'
     Ballposition=[]
     PlatformPosition_1P=[]
     Ball_speed=[]
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
                 Ballposition.append(target_record["scene_info"][n]["ball"])
                 Ball_speed.append(target_record["scene_info"][n]["ball_speed"])
                 PlatformPosition_1P.append(target_record["scene_info"][n]["platform_1P"])
#-----------------------------------------------------------------------------------------------------------------------------------#
##############################################################################
     PlatX = np.array(PlatformPosition_1P) [:,0][:,np.newaxis]          #板子的X位子
     PlatX_next = PlatX[1:,:]                                           #除了PlatX[0]，其他都要放進PlatX_next
     instrust = (PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5 #算出板子位移的次數    
     
     ## PlatY = np.array(PlatformPosition_2P) [:,1][:,np.newaxis]
     ## PlatY_next = PlatY[1:,:]

     Ballarray = np.array(Ballposition[:-1])   #球的X和Y的座標
     
     
     
     #X位移量
     '''
     BallX_position = np.array(Ballposition)[:,0][:,np.newaxis]
     BallX_position_next = BallX_position[1:,:]
     Ball_Vx = BallX_position_next - BallX_position[0:len(BallX_position_next),0][:,np.newaxis]
     '''
     Ball_Vx = np.array(Ball_speed)[0:-1,0][:,np.newaxis]
     '''
     #Y位移量
     BallY_position = np.array(Ballposition)[:,1][:,np.newaxis]
     BallY_position_next = BallY_position[1:,:]
     Ball_Vy = BallY_position_next - BallY_position[0:len(BallY_position_next),0][:,np.newaxis]
     ''' 
     Ball_Vy = np.array(Ball_speed)[:-1,1][:,np.newaxis]
     ## Ball_Plat_Y = PlatY_next-BallY_position_next
     
     #            球的X和Y的座標      板子的X位子          #X速度   #Y速度
     x = np.hstack((Ballarray,PlatX[:-1,0][:,np.newaxis],Ball_Vx,Ball_Vy))
     y = instrust
     y = np.array(y, dtype=int)
#--------------------------- train & test data

     x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 41)
#--------------------------- train model

     svr = SVR(gamma=0.001,C = 1,epsilon = 0.1,kernel = 'rbf')
     svr.fit(x_train,y_train)
     y_predict = svr.predict(x_test)

     R2 = r2_score(y_test,y_predict)
     print("R2=",R2)
#-----------------------------------------------------------------------------------------------------------------------------------#
     filename = "C:\\Users\\USER\\Desktop\\W3_6_8\\zxc1263426\\MLGame-master\\games\\pingpong\\ml\\SVM_1P_20210105.sav"
     pickle.dump(svr , open(filename,'wb'))
#-----------------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    print_log()