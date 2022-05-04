import pandas as pd
import numpy as np
from pathlib import Path
import wave
import evaluate
import io_task as ld
import signal_functions as sf
import os

#define global parameters by our teachers' python file
sample_rate=16000
window=512 #16000*0.032
shift=128 #16000*0.008

#generate the dataset on dev_label and calculate the prediction and truth
data,dataloader=ld.generate_dataloader('dev_label.txt','/wavs/dev')

#if you want to calculate the parameters to check the correctness, simply change use_default to False 
glb_prediction,glb_truth=ld.generate_labels(data,dataloader,window,shift,sample_rate,use_default=True)

#calculate the model evaluation parameters based on our teachers' script
AUC,EER=evaluate.get_metrics(glb_prediction,glb_truth)
ACC=np.count_nonzero((glb_truth==glb_prediction))/len(glb_truth)

#show the result for task1
ld.display_result(ACC,AUC,EER)

#generate the txt file on test set for task 1
test_dir=os.listdir(os.getcwd()+'/wavs/test')
ld.write_result(test_dir)
