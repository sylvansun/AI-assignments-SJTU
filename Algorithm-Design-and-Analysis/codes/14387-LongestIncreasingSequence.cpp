//
//  main.cpp
//  14387.LongestIncreasingSequence
//
//  Created by Chalice of the Void on 2022/4/16.
//

#include <iostream>
const int INF=2<<20;
const int MAX_N=10005;

struct Node{
    int v;
    Node* pre;
    Node(){v=0;pre=NULL;}
    Node(int a, Node* p):v(a),pre(p){}
};
Node inf_node(INF,NULL);

Node a[MAX_N];//original data
int n;//length of sequence
Node* lis[MAX_N];//store the current optimal increasing sequence

void read_input();
int solve();
int binary_search(int l,int r,int val);//search on array lis to find element less or equal to
void show_result(Node* p);
void show_state();

int main(int argc, const char * argv[]) {
    read_input();
    int length=solve();
    Node* end=lis[length];
    show_result(end);
    return 0;
}

void show_state(){
    for(int i=1;i<=n;++i){
        std::cout<<lis[i]->v<<" ";
    }
    std::cout<<std::endl;
}
void show_result(Node* p){
    if(p==NULL){
        return;
    }
    show_result(p->pre);
    std::cout<<p->v<<" ";
}

int binary_search(int l, int r,int val){
    if(l==r){
        if(lis[l]->v>=val){
            return l;
        }
        else{
            return l+1;
        }
    }
    int m=l+(r-l)/2;
    if(lis[m]->v==val){
        return m;
    }
    if(lis[m]->v<val){
        return binary_search(m+1,r,val);
    }
    else{
        return binary_search(l,m,val);
    }
}

void read_input(){
    std::cin>>n;
    int tmp;
    for(int i=0;i<n;++i){
        std::cin>>tmp;
        a[i]=Node(tmp,NULL);
        lis[i]=&inf_node;
    }
    lis[n]=&inf_node;
    lis[n+1]=&inf_node;
}


int solve(){
    for(int i=0;i<n;++i){
        int val=a[i].v;
        int pos=binary_search(1, i+1, val);
        if(pos==1){
            lis[pos]=&a[i];
        }
        else{
            a[i].pre=lis[pos-1];
            lis[pos]=&a[i];
        }
        //show_state();
    }
    int result=0;
    for(int i=1;i<=n+1;++i){
        if(lis[i]->v==INF){
            result=i-1;
            break;
        }
    }
    std::cout<<result<<std::endl;
    return result;
}
