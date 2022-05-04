import pandas as pd
import numpy as np
from pathlib import Path
import wave as wv
import signal_functions as sf
import os

def generate_dataloader(file_name,folder):
    data=pd.read_csv(str(Path.cwd())+'/data/'+file_name,header=None,delimiter='-')
    sub_column=data[2].str.split(' ',n=1,expand=True)
    data.drop(2,inplace=True,axis=1)
    for i in range(sub_column.shape[1]):
        data.insert(i+2,i+2,sub_column[i])
    dataloader=[]
    for i in range(500):
        dataloader.append(str(Path.cwd())+folder+'/{a}-{b}-{c}.wav'.format(a=data.iloc[i,0],b=data.iloc[i,1],c=data.iloc[i,2]))
    return data,dataloader

def display_result(acc,auc,eer):
    print("Results for the plain linear classifiers")
    print("Total Accuracy: ",acc)
    print("Total AUC: ",auc)
    print("Total EER:",eer)
    

def write_result(dir):
    file = open(os.getcwd()+'/data/test_label_task1.txt', "w+")
    for i in range(len(dir)):
        file.write(dir[i].split('.')[0]+' ')
        data,nframe,framerate=read_wave(os.getcwd()+'/wavs/test/'+dir[i])
        time_point,pred=sf.cal_interval(data)
        for j in range(len(time_point)):
            file.write(str(time_point[j][0])+','+str(time_point[j][1])+' ')
        file.write('\n')
        if (i+1)%50==0:
            print('{a}% have been evaluated'.format(a=(i+1)/10))
    file.close()
    
def read_wave(path):
    file = wv.open(path,'rb')
    params = file.getparams()
    framerate,nframes = params[2:4]
    wave = np.fromstring(file.readframes(nframes),dtype = np.short)
    file.close()
    wave = wave * 1.0 / (max(abs(wave)))
    return wave,nframes,framerate

def generate_labels(data,dataloader,window=512,shift=128,sample_rate=16000,use_default=True,amphigh=20,amplow=10,zcrhigh=0.2,zcrlow=0.1):
    if use_default==False:
        zcrhigh,zcrlow,amphigh,amplow=sf.solve_task1(dataloader,window,shift)
    ground_truth=np.zeros(0)
    prediction=np.zeros(0)
    for i in range(len(dataloader)):
        curr_data,nframe,framerate=read_wave(dataloader[i])
        time_point,curr_pred=sf.cal_interval(curr_data,amphigh,amplow,zcrhigh,zcrlow,window,shift)
        curr_label=np.zeros(len(curr_pred))
        true_point=data[3][i].split()
        curr_len=len(true_point)
        for j in range(curr_len):
            start=float(true_point[j].split(',')[0])
            end=float(true_point[j].split(',')[1])
            curr_label[round(start*sample_rate/shift):round(end*sample_rate/shift)]=1
        ground_truth=np.concatenate((ground_truth,curr_label))
        prediction=np.concatenate((prediction,curr_pred))
        if (i+1)%50==0:
            print('{a}% have been evaluated'.format(a=(i+1)/5))
    return prediction,ground_truth
