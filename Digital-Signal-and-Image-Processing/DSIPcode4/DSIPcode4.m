%global parameters
fftlen=512;
freq=5000;

%read_input and variables for q1
[y,Fs]=audioread('demo.mp3');

%variables for q2
q2 = y(:,1);
q2_1 = downsample(q2,round(Fs/(freq*1)));
audiowrite('q2_5khz.wav',q2_1,(freq*1));
q2_2 = downsample(q2,round(Fs/(freq*2)));
audiowrite('q2_10khz.wav',q2_2,(freq*2));
q2_3 = downsample(q2,round(Fs/(freq*3)));
audiowrite('q2_15khz.wav',q2_3,(freq*3));

%variables for q3
q3_1=resample(q2_1,Fs,freq*1);
audiowrite('q3_5khz.wav',q3_1,Fs);
q3_2=resample(q2_2,Fs,freq*2);
audiowrite('q3_10khz.wav',q3_2,Fs);
q3_3=resample(q2_3,Fs,freq*3);
audiowrite('q3_15khz.wav',q3_3,Fs);

%q4
wp=[260 380]/1000;
ws=[255 405]/1000;
[n,wn] =ellipord(wp,ws, 3, 50);
[b, a] =ellip(n, 3, 50, wn);
q4_ftd=filter(b, a, y);
q4 = 4*q4_ftd+y;
audiowrite('q4.wav',q4,Fs);

%plot the result
subplot(721),plot(y),title('q1');
subplot(722),stft(y(:,1),Fs,'FFTLength',fftlen),colormap jet;

subplot(723),plot(q2_1),title('q2 5khz');
subplot(724),stft(q2_1,freq*1,'FFTLength',fftlen),colormap jet;
subplot(725),plot(q2_2),title('q2 10khz');
subplot(726),stft(q2_2,freq*2,'FFTLength',fftlen),colormap jet;
subplot(727),plot(q2_3),title('q2 15khz');
subplot(728),stft(q2_3,freq*3,'FFTLength',fftlen),colormap jet;

subplot(7,2,9),plot(q3_1),title('q3 5khz');
subplot(7,2,10),stft(q3_1,Fs,'FFTLength',fftlen),colormap jet;
subplot(7,2,11),plot(q3_2),title('q3 10khz');
subplot(7,2,12),stft(q3_2,Fs,'FFTLength',fftlen),colormap jet;
subplot(7,2,13),plot(q3_3),title('q3 15khz');
subplot(7,2,14),stft(q3_3,Fs,'FFTLength',fftlen),colormap jet;

