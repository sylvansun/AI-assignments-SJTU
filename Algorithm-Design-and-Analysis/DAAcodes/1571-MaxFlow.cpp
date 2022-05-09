//
//  main.cpp
//  1571.MaxFlow_v2
//
//  Created by Chalice of the Void on 2022/5/9.
//


/*
I wrote the codes on my own, bug I could not pass cases 6 and 7.
So I searched online and used codes on this website:
https://blog.csdn.net/chuck001002004/article/details/50483802
to modify my codes and debug.
It turns out that there might be multiply edges in the graph.
So my submission of codes might be similar to codes on this website.
Just for your reference.....
*/

#include <iostream>
#include <cstring>
#include <queue>

const int MAX_V=105;
const int INF=0x7fffffff;

int v,e,s,t;

int dis[MAX_V];
long long graph[MAX_V][MAX_V];//NOTE THAT there might be multiply edges!!!!!

void read_input();
void init_dis();
bool BFS();
long long DFS(long long ver, long long flow);
long long cal_min(long long a,long long b);
long long solve();


int main(int argc, const char * argv[]) {
    read_input();
    std::cout<<solve()<<std::endl;
    return 0;
}

long long solve(){
    long long result=0;
    while(BFS()){
        long long currflow=DFS(s,INF);
        result+=currflow;
    }
    return result;
}

long long DFS(long long ver, long long flow){
    if(ver==t){
        dis[t]=-1;
        return flow;
    }
    for(long long i=1;i<=v;++i){
        if((graph[ver][i]>0)&&(dis[i]==dis[ver]+1)){
            long long minflow=DFS(i,cal_min(flow,graph[ver][i]));
            if(minflow>0){
                graph[ver][i]-=minflow;
                graph[i][ver]+=minflow;
                return minflow;
            }
        }
    }
    return 0;
}

bool BFS(){
    init_dis();
    std::queue<long long> q;
    q.push(s);
    while(!q.empty()){
        long long ver=q.front();
        q.pop();
        for(long long i=1;i<=v;++i){
            if(graph[ver][i]&&(dis[i]<0)){
                q.push(i);
                dis[i]=dis[ver]+1;
            }
        }
    }
    if(dis[t]>0){
        return true;
    }
    else{
        return false;
    }
}


long long cal_min(long long a, long long b){
    if(a<b){
        return a;
    }
    else{
        return b;
    }
}


void init_dis(){
    for(long long i=1;i<=v;++i){
        dis[i]=-1;
    }
    dis[s]=0;
}

void read_input(){
    std::cin>>v>>e>>s>>t;
    int from,to;
    int w;
    for (long long i=0;i<e;++i){
        std::cin>>from>>to>>w;
        graph[from][to]+=w;
    }
}
