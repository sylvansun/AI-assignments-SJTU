max_n=3;
x=1:max_n;
time=zeros(4,max_n);%4 rows represent the time using different methods. Columns are the different sequence length

for a=1:max_n
    N=2^(a*4);%N is the length of sequence
    array=rand(N,1);%generate an array for calculation
    W_N=exp(-1i*2*pi/N);%root of unity with length N
    %method1
    tmp=0;
    profile on;
    for k=0:N-1%compute X[k]
        tmp=0;
        for n=1:N
            tmp=tmp+array(n)*W_N^(k*n-k);
        end
    end
    profile off;
    time(1,a)=profile('info').FunctionTable.TotalTime();
    
    %method2
    F=zeros(N,N);
    profile on;
    for row=1:N
        for col=row:N
            F(row,col)=W_N^((row-1)*(col-1));
            F(col,row)=F(row,col);
        end
    end
    fft_array=F*array;
    profile off;
    time(2,a)=profile('info').FunctionTable.TotalTime();
    
    %method3
    profile on;
    fft(array);
    profile off;
    time(3,a)=profile('info').FunctionTable.TotalTime();
    
    %method4
    profile on;
    %fft(gpuArray(array));
    profile off;
    time(4,a)=profile('info').FunctionTable.TotalTime();

end

plot(4*x,time(1,:),4*x,time(2,:),4*x,time(3,:),4*x,time(4,:));
legend('definition','matrix','fft','GPUfft');
title('Time spent with different DFT computing methods');
xlabel('exponential sequence length');
ylabel('time in seconds');


