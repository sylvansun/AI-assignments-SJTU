length=10;
orig_sig = rectwin(length);
f=100;
T=1/f;
sampling_sig=zeros(2*f*length,1);
for i=1:1000
    sampling_sig(2*i)=1;
end

sig = zeros(2*f*length,1);
for i=1:length
    sig(i*f*2)=orig_sig(i);
end
orig_sampled=zeros(2000,1);
for i=1:2000
    orig_sampled(i)=sig(i)*sampling_sig(i);
end
orig_sampled_fft=fft(orig_sampled);


shifted=zeros(2000,1);
for i=1:10
    shifted(2*f*i-1)=sig(i*f*2);
end
shifted_sampled=zeros(2000,1);
for i=1:2000
    shifted_sampled(i)=shifted(i)*sampling_sig(i);
end
shifted_sampled_fft=fft(shifted_sampled);

[a1,a2] = buttord(0.5,0.9,1,20);
[b1,b2] = butter(a1,a2,'low');
filtered = filter(b1,b2,shifted);
filtered_sampled=zeros(2000,1);
for i=1:2000
    filtered_sampled(i)=filtered(i)*sampling_sig(i);
end
filtered_sampled_fft=fft(filtered_sampled);

subplot(331),plot(orig_sampled),title('q1 time domain');
subplot(332),plot(abs(orig_sampled_fft)),title('q1 amplitude');
subplot(333),plot(angle(orig_sampled_fft)),title('q1 angle');

subplot(334),plot(shifted_sampled),title('q2 time domain');
subplot(335),plot(abs(shifted_sampled_fft)),title('q2 amplitude');
subplot(336),plot(angle(shifted_sampled_fft)),title('q2 angle');

subplot(337),plot(filtered_sampled),title('q3 time domain');
subplot(338),plot(abs(filtered_sampled_fft)),title('q3 amplitude');
subplot(339),plot(angle(filtered_sampled_fft)),title('q3 angle');







