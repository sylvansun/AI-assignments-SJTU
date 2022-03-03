%generate PSF and original image
psf=ones(5,5)*0.04;
orig=imread('./figures/baboon.bmp');
%generate blurred image
blurred=conv2(orig,psf);
%generate noised images with different SNR
noised30=awgn(blurred,30,'measured');
noised20=awgn(blurred,20,'measured');
noised10=awgn(blurred,10,'measured');
%deconvolution with different methods
direct30=deconvwnr(noised30,psf);
direct20=deconvwnr(noised20,psf);
direct10=deconvwnr(noised10,psf);
wiener30=deconvwnr(noised30,psf,1/30);
wiener20=deconvwnr(noised20,psf,1/20);
wiener10=deconvwnr(noised10,psf,1/10);
lucy30=deconvlucy(noised30,psf);
lucy20=deconvlucy(noised20,psf);
lucy10=deconvlucy(noised10,psf);
%show the result 
subplot(531),imshow(orig),title('original image');
subplot(532),imshow(blurred,[]),title('blurred image');
subplot(534),imshow(noised30,[]),title('blurred and noised in 30 dB');
subplot(535),imshow(noised20,[]),title('blurred and noised in 20 dB');
subplot(536),imshow(noised10,[]),title('blurred and noised in 10 dB');
subplot(537),imshow(direct30,[]),title('direct filtering, 30 dB');
subplot(538),imshow(direct20,[]),title('direct filtering, 20 dB');
subplot(539),imshow(direct10,[]),title('direct filtering, 10 dB');
subplot(5,3,10),imshow(wiener30,[]),title('wiener filtering, 30 dB');
subplot(5,3,11),imshow(wiener20,[]),title('wiener filtering, 20 dB');
subplot(5,3,12),imshow(wiener10,[]),title('wiener filtering, 10 dB');
subplot(5,3,13),imshow(lucy30,[]),title('lucy filtering, 30 dB');
subplot(5,3,14),imshow(lucy20,[]),title('lucy filtering, 20 dB');
subplot(5,3,15),imshow(lucy10,[]),title('lucy filtering, 10 dB');
%save the pictures
imwrite(blurred/255,'./figures/blurred image.bmp','bmp')
imwrite(noised30/255,'./figures/blurred and noised in 30 dB.bmp','bmp')
imwrite(noised20/255,'./figures/blurred and noised in 20 dB.bmp','bmp')
imwrite(noised10/255,'./figures/blurred and noised in 10 dB.bmp','bmp')
imwrite(direct30/255,'./figures/direct filtering, 30 dB.bmp','bmp')
imwrite(direct20/255,'./figures/direct filtering, 20 dB.bmp','bmp')
imwrite(direct10/255,'./figures/direct filtering, 10 dB.bmp','bmp')
imwrite(wiener30/255,'./figures/wiener filtering, 30 dB.bmp','bmp')
imwrite(wiener20/255,'./figures/wiener filtering, 20 dB.bmp','bmp')
imwrite(wiener10/255,'./figures/wiener filtering, 10 dB.bmp','bmp')
imwrite(lucy30/255,'./figures/lucy filtering, 30 dB.bmp','bmp')
imwrite(lucy20/255,'./figures/lucy filtering, 20 dB.bmp','bmp')
imwrite(lucy10/255,'./figures/lucy filtering, 10 dB.bmp','bmp')
