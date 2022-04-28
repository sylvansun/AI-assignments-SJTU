%prepare the global paremeters and variables for the program
length=10;% total length of rectangle window
orig_sig = rectwin(length);% the original signal in discrete form
f=100;% sampling frequency
T=1/f;% period
sampling_sig=zeros(2*f*length,1);% generate the sampling signal
for i=1:1000
    sampling_sig(2*i)=1;%sample every 0.01 seconds. For an array of length 2000, we sample at the even indexes
end

%codes for q1
sig = zeros(2*f*length,1);%formulate the original signal into the same format as sampling signal
for i=1:length
    sig(i*f*2)=orig_sig(i);%the original signal should take value one at ten points only
end
orig_sampled=zeros(2000,1);
for i=1:2000
    orig_sampled(i)=sig(i)*sampling_sig(i);
end
orig_sampled_fft=fft(orig_sampled);

%codes for q2
shifted=zeros(2000,1);
for i=1:10
    shifted(2*f*i-1)=sig(i*f*2);%shift the original signal left for 0.5*T
end
shifted_sampled=zeros(2000,1);
for i=1:2000
    shifted_sampled(i)=shifted(i)*sampling_sig(i);
end
shifted_sampled_fft=fft(shifted_sampled);

%codes for q3
[a1,a2] = buttord(0.5,0.9,1,20);
[b1,b2] = butter(a1,a2,'low');
filtered = filter(b1,b2,shifted);%generate the filterd signal for question3
filtered_sampled=zeros(2000,1);
for i=1:2000
    filtered_sampled(i)=filtered(i)*sampling_sig(i);
end
filtered_sampled_fft=fft(filtered_sampled);

%save the pictures
saveas(plot(orig_sampled),'./figures/q1 time domain.jpg','jpg')
saveas(plot(abs(orig_sampled_fft)),'./figures/q1 amplitude.jpg','jpg')
saveas(plot(angle(orig_sampled_fft)),'./figures/q1 angle.jpg','jpg')
saveas(plot(shifted_sampled),'./figures/q2 time domain.jpg','jpg')
saveas(plot(abs(shifted_sampled_fft)),'./figures/q2 amplitude.jpg','jpg')
saveas(plot(angle(shifted_sampled_fft)),'./figures/q2 angle.jpg','jpg')
saveas(plot(filtered_sampled),'./figures/q3 time domain.jpg','jpg')
saveas(plot(abs(filtered_sampled_fft)),'./figures/q3 amplitude.jpg','jpg')
saveas(plot(angle(filtered_sampled_fft)),'./figures/q3 angle.jpg','jpg')

%show the result
subplot(331),plot(orig_sampled),title('q1 time domain');
subplot(332),plot(abs(orig_sampled_fft)),title('q1 amplitude');
subplot(333),plot(angle(orig_sampled_fft)),title('q1 angle');

subplot(334),plot(shifted_sampled),title('q2 time domain');
subplot(335),plot(abs(shifted_sampled_fft)),title('q2 amplitude');
subplot(336),plot(angle(shifted_sampled_fft)),title('q2 angle');

subplot(337),plot(filtered_sampled),title('q3 time domain');
subplot(338),plot(abs(filtered_sampled_fft)),title('q3 amplitude');
subplot(339),plot(angle(filtered_sampled_fft)),title('q3 angle');

saveas(gcf,'./figures/all_results.jpg','jpg')



