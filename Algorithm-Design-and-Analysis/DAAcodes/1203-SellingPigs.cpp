//
//  main.cpp
//  1203.SellingPigs
//
//  Created by Chalice of the Void on 2022/5/9.
//

#include <iostream>
#include <cstring>
#include <queue>
const int MAX_N=105;
const int MAX_M=1005;
const int INF=0x7fffffff;

int m,n;
int src,dst;//two unused vertex as the source and destination

int dis[MAX_N];
bool vis[MAX_M];//mark after the first visit
int last[MAX_M];//update at each visit
int load[MAX_M];//number of max load

int graph[MAX_N][MAX_N];

void construct_graph();
bool BFS();
int DFS(int ver, int flow);
int cal_min(int a,int b);
int solve();
void show_graph();

int main(){
    construct_graph();
    std::cout<<solve()<<std::endl;
    return 0;
}

int solve(){
    int result=0;
    while(BFS()){
        int currflow=DFS(src,INF);
        result+=currflow;
    }
    return result;
}

int DFS(int ver, int flow){
    if(ver==dst){
        dis[dst]=-1;
        return flow;
    }
    for(int i=1;i<=dst;++i){
        if((graph[ver][i]>0)&&(dis[i]==dis[ver]+1)){
            int minflow=DFS(i,cal_min(flow,graph[ver][i]));
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
    memset(dis,-1,sizeof(dis));
    dis[src]=0;
    std::queue<int> q;
    q.push(src);
    while(!q.empty()){
        int ver=q.front();
        q.pop();
        for(int i=1;i<=dst;++i){
            if(graph[ver][i]&&(dis[i]<0)){
                q.push(i);
                dis[i]=dis[ver]+1;
            }
        }
    }
    if(dis[dst]>0){
        return true;
    }
    else{
        return false;
    }
}

int cal_min(int a,int b){
    if(a<b){return a;}
    else{return b;}
}

void construct_graph(){
    std::cin>>m>>n;
    dst=n+1;
    for(int i=1;i<=m;++i){
        std::cin>>load[i];
    }
    for(int i=1;i<=n;++i){//customers
        int loop,tmp;
        std::cin>>loop;
        for(int j=1;j<=loop;++j){
            std::cin>>tmp;
            if(last[tmp]==0){
                graph[src][i]+=load[tmp];
            }
            else{
                graph[last[tmp]][i]=INF;
            }
            last[tmp]=i;
        }
        std::cin>>graph[i][dst];
    }
}
