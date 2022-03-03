//
//  main.cpp
//  1301.BubblingBubbles
//
//  Created by Chalice of the Void on 2022/3/1.
//

#include <iostream>
using namespace std;

const int N = 1e6+10;

struct inverse_count
{
    int n;
    int count;
};

inverse_count dataset[N];
int datasize;

void read();
void show_result();
void merge(inverse_count* a,int asize);//merge an array a with size asize, during which we also count the number of inversed pairs.

int main(int argc, const char * argv[]) {
    read();
    merge(dataset,datasize);
    show_result();
    return 0;
}

void read(){
    cin>>datasize;
    for(int i=0;i<datasize;++i){
        cin>>dataset[i].n;
        dataset[i].count=0;
    }
}

void show_result(){
    for(int i=0;i<datasize;++i){
        cout<<dataset[i].count<<" ";
    }
    cout<<endl;
}

void merge(inverse_count* a,int asize){
    if(asize==1){
        return;
    }
    int lsize=asize/2;
    int rsize=asize-lsize;
    inverse_count* a1=new inverse_count[lsize];
    for(int i=0;i<lsize;++i){
        a1[i]=a[i];
    }
    inverse_count* a2=new inverse_count[rsize];
    for(int i=0;i<rsize;++i){
        a2[i]=a[i+lsize];
    }
    merge(a1,lsize);
    merge(a2,rsize);
    int pos=0;
    int pos1=0;
    int pos2=0;
    //the while loop below carries out the merge process of given two sequences
    while(true){
        if(a1[pos1].n<a2[pos2].n){//not a inverse pair
            a1[pos1].count = a1[pos1].count + pos2;
            a[pos]=a1[pos1];
            pos1++;
        }
        else{//a inverse pair
            a2[pos2].count+=(lsize-pos1);
            a[pos]=a2[pos2];
            pos2++;
        }
        pos++;
        if(pos2==rsize){//no elements in the latter sequence
            while(pos1<lsize){
                a1[pos1].count = a1[pos1].count + pos2;
                a[pos]=a1[pos1];
                pos1++;
                pos++;
            }
            break;
        }
        if(pos1==lsize){//no elements in the former sequence
            while(pos2<rsize){
                a[pos]=a2[pos2];
                pos2++;
                pos++;
            }
            break;
        }
    }
    delete [] a1;
    delete [] a2;
    return;
}
