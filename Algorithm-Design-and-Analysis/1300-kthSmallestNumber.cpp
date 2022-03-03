//
//  main.cpp
//  1300.k-thSmallestNumber
//
//  Created by Chalice of the Void on 2022/3/1.
//

#include <iostream>
using namespace std;

const int N = 4e7 + 1;
int n, k;
int a[N];

void read_input_data();
void solve_question(int method);

//the original version. This function creates three new arrays and store the values in them each time. And it turns out that it is very space-comsuming.
int find_k_original(int* a, int asize, int k);
void solution_1();

//below is a better version using the ideas of quicksort. After discussion with my roommate xjy I tried to better my algorithm.
//this algorithm is nothing better in case of speed because we still need to scan the arrays many times. But it saves the space as it does not require us to initialize new arrays every time
int find_k_quicksort(int* a, int left, int right,int k);


int main(int argc, const char * argv[]) {
    read_input_data();
    solve_question(0);
    return 0;
}


int find_k_quicksort(int* a, int left, int right,int k){
    int l=left;
    int r=right;
    int pos=left+(right-left)/2;
    int pivot=a[pos];
    a[pos]=a[r];
    int equal_count=0;
    while(l<r){
        while(a[l]<pivot && l<r){
            l++;
        }
        if(a[l]==pivot){
            equal_count++;
        }
        a[r]=a[l];
        while(a[r]>=pivot && l<r){
            r--;
        }
        a[l]=a[r];
    }
    a[l]=pivot;
    //the logic below is very significant in out codes which solve the case when there are multiple solutions in our array. If you put those with same values into a same array there actually is a problem that it will search the sequence many times. Can consider a case where there are all equal values in an array.
    if(l-left<=k-1 && l-left+equal_count>=k-1){
        return pivot;
    }
    else if(l-left<k-1){
        return find_k_quicksort(a, l, right, k-(l-left));
    }
    else{
        return find_k_quicksort(a, left, r, k);
    }
}

int find_k_original(int* a,int asize, int k)
{
    int pos=asize/2;
    if(!pos){
        pos=1;
    }
    //since our array starts from position 1, we should do a subtle pre-operation
    int rst=a[pos]; //pick a value randomly, here for convenience I simply take the number in the middle of the array..
    int* a_smaller = new int[asize];
    int* a_larger = new int[asize];
    int* a_equal = new int[asize];
    //here the construction of three arrays may cost a little extra space. But it is still within this problem's requirement..
    int n_smaller=0;
    int n_equal=0;
    int n_larger=0;
    for(int i=1;i<=asize;++i){
        if(a[i]<rst){
            n_smaller++;
            a_smaller[n_smaller]=a[i];
        }
        else if(a[i]>rst){
            n_larger++;
            a_larger[n_larger]=a[i];
        }
        else{
            n_equal++;
            a_equal[n_equal]=a[i];
        }
    }
    delete []a;//always remember to release the memory, since we are not going to use a again
    if(n_smaller<k){
        if(n_smaller+n_equal>=k){
            return rst;
        }
        else{
            delete [] a_smaller;
            delete [] a_equal;
            return find_k_original(a_larger,n_larger,k-n_smaller-n_equal);
        }
    }
    else{
        delete [] a_larger;
        delete [] a_equal;
        return find_k_original(a_smaller,n_smaller,k);
    }
}

void solution_1(){
    int* b = new int[N];//the function we are going to call requires us to use dynamic vectors, so here we do a copy of static arry a
    for(int i=1;i<=n;++i){
        b[i]=a[i];
    }
    cout<<find_k_original(b,n,k)<<endl;
}

void solve_question(int method){
    switch(method){
        case 0:
            cout<<find_k_quicksort(a, 1, n, k)<<endl;
            break;
        default:
            solution_1();
    }
}

void read_input_data() {
    int m;
    cin >> n >> k >> m;
    for (int i = 1; i <= m; i++) {
        cin >> a[i];
    }
    unsigned int z = a[m];
    for (int i = m + 1; i <= n; i++) {
        z ^= z << 13;
        z ^= z >> 17;
        z ^= z << 5;
        a[i] = z & 0x7fffffff;
    }
    cout<<endl;
}

//note that vector will not simplify this code much, and it costs more memory spaces as well... On the online judge system when using vector it will report a MLE error.

