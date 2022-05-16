%prepare global parameters
orig = imread('roman.jpg');
r = orig(:,:,1);
g = orig(:,:,2);
b = orig(:,:,3);
max = uint8(255*ones(900,1440));
min = uint8(zeros(900,1440));

rng default; 
norm = normrnd(10,1,1000,1);
exp = exprnd(1,1000,1);
hnorm = histogram(norm,64).Values;
hexp = histogram(exp,64).Values;


q1 = histeq(r);
q2exp = histeq(r,hexp);
q2norm = histeq(r,hnorm);
subplot(421),imshow(r),title('channel R');
subplot(422),imhist(r),title('channel R histogram');
subplot(423),imshow(q1),title('channel R equalization');
subplot(424),imhist(q1),title('histogram after equalization');
subplot(425),imshow(q2exp),title('channel R exponential match');
subplot(426),imhist(q2exp),title('histogram after exponential match');
subplot(427),imshow(q2norm),title('channel R normal match');
subplot(428),imhist(q2norm),title('histogram after normal match');

req = histeq(r);
geq = histeq(g);
beq = histeq(b);
q4 = cat(3,req,geq,beq);
req_norm = histeq(r,hexp);
geq_norm = histeq(g,hexp);
beq_norm = histeq(b,hexp);
q5 = cat(3,req_norm,geq_norm,beq_norm);

%subplot(311),imshow(orig);
%subplot(312),imshow(q4);
%subplot(313),imshow(q5);



