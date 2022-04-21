//
//  main.cpp
//  1433_v2.StockSpeculation
//
//  Created by Chalice of the Void on 2022/4/21.
//

#include <iostream>
#include <queue>

const int MAX_N=100005;
std::priority_queue<int> q;
int price[MAX_N];
int n;//number of days
void read_input();
long long solve();
int main(int argc, const char * argv[]) {
    read_input();
    std::cout<<solve()<<std::endl;
    return 0;
}

long long solve(){
    long long result=0;
    q.push(price[n]);
    for(int i=n-1;i>0;--i){
        if(price[i]<q.top()){//there exists a stock exchange, push twice
            result=result+(q.top()-price[i]);
            q.pop();
            q.push(price[i]);
        }
        q.push(price[i]);
    }
    return result;
}

void read_input(){
    std::cin>>n;
    for(int i=1;i<=n;++i){
        std::cin>>price[i];
    }
}
