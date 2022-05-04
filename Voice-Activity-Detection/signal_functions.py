#########function definition for the two tasks of project1
import numpy as np
import torch

####returns the signal as frames for given input, the default parameters are from the teacher's python files with sampling rate 16000
def get_frame(data,window=512,shift=128):
    nx = len(data)
    wlen=window
    nf = int(np.fix((nx - wlen) / shift) + 1)
    f = np.zeros((nf,wlen))
    for i in range(nf-1):
        for j in range(wlen):
            f[i,j] = data[i*shift+j]
    for i in range(nx-nf*shift):
        f[nf-1,i]=data[(nf-1)*shift+i]
    return f

#calculate the zero crossing rate of a given data with certain window and shift amount
def cal_zcr(data,window,shift):
    signs = np.multiply(get_frame(data[0:-1],window,shift),get_frame(data[1:],window,shift))<0
    return list(np.sum(signs,axis=1)/window)

#calculate the amplitude
def cal_amp(data,window,shift):
    amp = list((abs(get_frame(data,window,shift))).sum(axis = 1))
    return amp


def get_statistics(dataloader,window,shift):
    max_zrcs=[]
    max_amps=[]
    clk=0
    for data_path in dataloader:
        clk=clk+1
        wavedata,nframes,framerate = read(data_path)
        single_zrc=get_zcr(wavedata,window,shift)
        single_amp=get_amplitude(wavedata,window,shift)
        max_zrcs.append(np.max(single_zrc))
        max_amps.append(np.max(single_amp))
    mean_zrc=np.mean(max_zrcs)
    mean_amp=np.mean(max_amps)
    return mean_zrc/4,mean_zrc/8,mean_amp/4,mean_amp/8
    

def check_points(data,AmpHigh=20,AmpLow=10,ZcrHigh=0.2,ZcrLow=0.1,window=512,shift=128,sample_rate=16000):
    # 端点检测
    MaxSilence = 10 #最长语音间隙时间
    MinAudio = 16 #最短语音时间
    Status = 0 #状态0:静音段,1:过渡段,2:语音段,3:结束段
    SilenceTime = 0 #语音间隙时间
    check_points=[]
    amp=cal_amp(data,window,shift)
    zcr=cal_zcr(data,window,shift)
    #print('开始端点检测')
    n = len(data)
    nf = int(np.fix((n - window) / shift) + 1)
    state=np.zeros(nf)
    for n in range(len(zcr)):
        if amp[n] > AmpHigh or zcr[n] > ZcrHigh:
            Status = 2
            SilenceTime = 0
            state[n]=Status
        elif amp[n] > AmpLow or zcr[n] > ZcrLow:
            Status = 1
            state[n]=Status
        else:
            Status = 0
            state[n]=Status
    startpoint=0
    endpoint=0
    Status=0
    for i in range(len(state)):
        if(Status==0 and state[i]==2):
            flag=1
            for j in range(MinAudio):
                flag=flag*state[min(i+j,len(state)-1)]
            if(flag>0):
                startpoint=i
                Status=1
        if(Status==1 and state[i]==0):
            flag=0
            for j in range(MaxSilence):
                flag=flag+state[min(i+j,len(state)-1)]
            if(flag==0):
                endpoint=i
                Status=0
                check_points.append((startpoint,endpoint))
    timeaxis=[]
    for i in range(len(check_points)):
        starttime=(check_points[i][0]*shift)/sample_rate
        endtime=(check_points[i][1]*shift+window)/sample_rate
        timeaxis.append((starttime,endtime))
    return timeaxis,state


def get_fbank(signal,win,inc):
    pre_emphasis = 0.97
    emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
    framed_signal=get_frame(emphasized_signal,win,inc)
    windowed_signal=[np.hamming(win)*f for f in framed_signal]
    NFFT = 256
    mag_frames = np.absolute(np.fft.rfft(windowed_signal, NFFT))
    pow_frames = ((1.0 / NFFT) * (mag_frames ** 2))
    low_freq_mel = 0
    high_freq_mel = 2595 * np.log10(1 + (16000 / 2) / 700)
    nfilt = 80
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
    hz_points = 700 * (10 ** (mel_points / 2595) - 1)
    fbank = np.zeros((nfilt, int(NFFT / 2 + 1)))
    Bin = (hz_points / (16000 / 2)) * (NFFT / 2)
    for i in range(1, nfilt + 1):
        left = int(Bin[i-1])
        center = int(Bin[i])
        right = int(Bin[i+1])
        for j in range(left, center):
            fbank[i-1, j+1] = (j + 1 - Bin[i-1]) / (Bin[i] - Bin[i-1])
        for j in range(center, right):
            fbank[i-1, j+1] = (Bin[i+1] - (j + 1)) / (Bin[i+1] - Bin[i])
    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)
    filter_banks = 20 * np.log10(filter_banks)
    return torch.tensor(filter_banks)

def get_label(nf,time_float):
    maxtime=time_float[-1][1]
    maxframe=(maxtime*16000)/128+1
    label=torch.zeros(nf)
    for time in time_float:
        startframe=(time[0]*16000)/128
        endframe=(time[1]*16000)/128
        label[int(startframe):int(endframe+1)]=1
    return label


def smoothing(predict_label):
    Status = 0
    check_points=[]
    startpoint=0
    endpoint=0
    for i in range(len(predict_label)):
        if(Status==0 and predict_label[i]==1):
            startpoint=i
            Status=1
        if(Status==1 and predict_label[i]==0):
            endpoint=i
            Status=0
            check_points.append((startpoint,endpoint))
    timeaxis=[]
    for i in range(len(check_points)):
        starttime=(check_points[i][0]*128)/16000
        endtime=(check_points[i][1]*128+512)/16000
        timeaxis.append((starttime,endtime))
    return timeaxis
