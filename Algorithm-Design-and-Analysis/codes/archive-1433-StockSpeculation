//
//  main.cpp
//  1433.StockSpeculation
//
//  Created by Chalice of the Void on 2022/4/15.
//

#include <iostream>

const int MAX_N=100005;//max number of days
const int INF=2<<20;

int price[MAX_N];
long long a[MAX_N],b[MAX_N];
int n;

void read_input();//note that the prices will be stored in p[1]~p[n]
long long solve();
long long cal_max(long long a,long long b,long long c);
void init();//initilize array a
void show_state();;//tool function to check state of array a

int main(int argc, const char * argv[]) {
    read_input();
    init();
    std::cout<<solve()<<std::endl;
    //show_state();
    return 0;
}

long long solve(){
    for(int i=1;i<=n;++i){//enumerate the days from 1 to n
        b[0]=cal_max(a[0],a[1]+price[i],-INF);
        for(int j=1;j<=i;++j){//enumerate the current stock holding from 1 to i, since current holding cannot be larger than i
            b[j]=cal_max(a[j-1]-price[i],a[j],a[j+1]+price[i]);
        }
        for(int j=0;j<=n;++j){
            a[j]=b[j];
        }
        //show_state();
    }
    return a[0];
}

void read_input(){
    std::cin>>n;
    for(int i=1;i<=n;++i){
        std::cin>>price[i];
    }
}

void init(){
    for(int i=1;i<=n;++i){
        a[i]=-INF;
        b[i]=-INF;
    }
}

void show_state(){
    for(int i=0;i<=n;++i){
        std::cout<<a[i]<<" ";
    }
    std::cout<<std::endl;
}
long long cal_max(long long a,long long b,long long c){
    long long result=a;
    if(b>result){
        result=b;
    }
    if(c>result){
        result=c;
    }
    return result;
}

