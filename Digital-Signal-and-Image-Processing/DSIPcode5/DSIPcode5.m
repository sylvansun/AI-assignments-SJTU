%prepare global parameters
orig = imread('roman.jpg');
r = orig(:,:,1);
g = orig(:,:,2);
b = orig(:,:,3);
max = uint8(255*ones(900,1440));
min = uint8(zeros(900,1440));

rng default; 
norm = normrnd(40,2,1000,1);
exp = exprnd(1,1000,1);
uni = unifrnd(40,100,1000,1);
hnorm = histogram(norm,64).Values;
hexp = histogram(exp,64).Values;
huni = histogram(uni,64).Values;



q1 = histeq(r);
q2exp = histeq(r,hexp);
q2norm = histeq(r,hnorm);
q3 = histeq(r,huni);
subplot(521),imshow(r),title('Original Image channel R');
subplot(522),imhist(r),title('channel R histogram');
subplot(523),imshow(q1),title('Question1 channel R equalization');
subplot(524),imhist(q1),title('histogram after equalization');
subplot(525),imshow(q2exp),title('Question2 channel R exponential match');
subplot(526),imhist(q2exp),title('histogram after exponential match');
subplot(527),imshow(q2norm),title('Question2 channel R normal match');
subplot(528),imhist(q2norm),title('histogram after normal match');
subplot(529),imshow(q3),title('Question3 channel R uniform match');
subplot(5,2,10),imhist(q3),title('histogram after uniform match');

req = histeq(r);
geq = histeq(g);
beq = histeq(b);
q4 = cat(3,req,geq,beq);
req_norm = histeq(r,hexp);
geq_norm = histeq(g,hexp);
beq_norm = histeq(b,hexp);
q5 = cat(3,req_norm,geq_norm,beq_norm);


subplot(131),imshow(orig),title('Original Image');
subplot(132),imshow(q4),title('Q4');
subplot(133),imshow(q5),title('Q5');




