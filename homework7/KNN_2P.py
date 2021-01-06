import pickle
import numpy as np
from os import listdir
from os.path import isfile, join
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


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
                 PlatformPosition_1P.append(target_record["scene_info"][n]["platform_2P"])
#-----------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------#
     np.set_printoptions(threshold=np.inf)
     PlatX = np.array(PlatformPosition_1P)[:,0][:,np.newaxis]               #板子的X位子
     PlatX_next = PlatX[1:,:]                                               #除了PlatX[0]，其他都要放進PlatX_next
     instruct = (PlatX_next - PlatX[0:len(PlatX_next),0][:, np.newaxis])/5  #算出板子位移的次數 
     
     #X位移量
     '''
     BallX=np.array(Ballposition)[:,0][:,np.newaxis]
     BallX_next=BallX[1:,:]
     vx=(BallX_next-BallX[0:len(BallX_next),0][:,np.newaxis])
     '''
     Ball_Vx = np.array(Ball_speed)[:-1,0][:,np.newaxis]     #Ball_X速度
     
     #Y位移量
     '''
     BallY=np.array(Ballposition)[:,1][:,np.newaxis]
     BallY_next=BallY[1:,:]
     vy=(BallY_next-BallY[0:len(BallY_next),0][:,np.newaxis])
     '''
     Ball_Vy = np.array(Ball_speed)[:-1,1][:,np.newaxis]     #Ball_Y速度
     
     Ballarray = np.array(Ballposition[:-1])                #球的X和Y的座標   
     
     #            球的X和Y的座標   板子的X位子               #X速度   #Y速度
     x = np.hstack((Ballarray , PlatX[:-1,0][:,np.newaxis],Ball_Vx,Ball_Vy))
     y = instruct
     y = np.array(y, dtype=int)

     x_train,x_test,y_train,y_test = train_test_split(x , y, test_size = 0.2,random_state = 1)


     knn = KNeighborsClassifier(n_neighbors = 5)

     knn.fit(x_train,y_train)

     yknn_bef_scaler = knn.predict(x_test)
     acc_knn_bef_scaler = accuracy_score(yknn_bef_scaler , y_test)
     print(acc_knn_bef_scaler)
#-----------------------------------------------------------------------------------------------------------------------------------#
     filename = "C:\\Users\\USER\\Desktop\\W3_6_8\\zxc1263426\\MLGame-master\\games\\pingpong\\ml\\knn_2P.sav"
     pickle.dump(knn , open(filename,'wb'))
#-----------------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    print_log()