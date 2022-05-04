import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
import time
import os
import numpy as np
import pandas as pd
from pathlib import Path
import signal_functions as sf
import io_task as ld
import evaluate

window=512
shift=128
sample_rate=16000

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1=nn.Linear(80,256)
        self.fc2=nn.Linear(256,128)
        self.fc3=nn.Linear(128,64)
        self.fc4=nn.Linear(64,2)
    def forward(self, x):
        x=F.relu(self.fc1(x))
        x=F.relu(self.fc2(x))
        x=F.relu(self.fc3(x))
        x=torch.sigmoid(self.fc4(x))
        return x

print('sss')
model_path=str(Path.cwd())+'/models_saved/net_3240.pth'
trained_model=Net()
trained_model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
trained_model.eval()

#generate the dataset on dev_label and calculate the prediction and truth
data,dataloader=ld.generate_dataloader('dev_label.txt','/wavs/dev')
predict_label=[]
for (i,path) in enumerate(dataloader):
    devdata,nframe,framerate=ld.read_wave(path)
    numf=int(np.fix((nframe - window) / shift) + 1)
    predict=np.zeros(numf)
    fbank=torch.tensor(sf.get_fbank(devdata,window,shift)).float()
    norm = nn.BatchNorm1d(80)
    data_fbank = fbank
    data_fbank=norm(data_fbank)
    clk=0
    for frame in data_fbank:
        ans=trained_model(frame)
        if(ans[0]>=ans[1]):
            predict[clk]=0
        else:
            predict[clk]=1
        clk=clk+1
    predict_label=np.concatenate((predict_label,predict),axis=0)
    if (i+1)%50==0:
        print('{a}% have been evaluated'.format(a=(i+1)/5))

empty,glb_truth=ld.generate_labels(data,dataloader,window,shift,sample_rate,use_default=True)
AUC,EER=evaluate.get_metrics(predict_label, glb_truth)
ACC=np.count_nonzero(predict_label==glb_truth)/len(glb_truth)

ld.display_result(AUC,EER,ACC)

file = open(os.getcwd()+'/data/test_label_task2.txt', "w+")
test_dir=os.listdir(os.getcwd()+'/wavs/test')
test_task2=[]
for i in range (len(test_dir)):
    testdata,a,b=ld.read_wave(os.getcwd()+'/wavs/test/'+test_dir[i])
    nf=int(np.fix((a - window) / shift) + 1)
    frameaxis=np.zeros(nf)
    data_fbank=torch.tensor(sf.get_fbank(testdata,512,128)).float()
    norm = nn.BatchNorm1d(80)
    data_fbank=norm(data_fbank)
    clk=0
    for frame in data_fbank:
        ans=trained_model(frame)
        if(ans[0]>=ans[1]):
            frameaxis[clk]=0
        else:
            frameaxis[clk]=1
        clk=clk+1
    time_points=sf.smoothing(frameaxis)
    file.write(test_dir[i].split('.')[0]+' ')
    for j in range(len(time_points)):
        file.write(str(time_points[j][0])+','+str(time_points[j][1])+' ')
    file.write('\n')
    if (i+1)%50==0:
        print('{a}% have been evaluated'.format(a=(i+1)/5))
file.close()


