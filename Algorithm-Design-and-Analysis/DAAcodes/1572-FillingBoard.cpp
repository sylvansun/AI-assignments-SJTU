//
//  main.cpp
//  1572.FillingBoard
//
//  Created by Chalice of the Void on 2022/5/9.
//

#include <iostream>
#include <queue>
#include <cstring>

const int BoardSize=35;
const int MAX_N=4100;
const int INF=0xfffffff;

bool board[BoardSize][BoardSize];
int T,n,m,k;
int src,dst;
int graph[MAX_N][MAX_N];
int dis[MAX_N];

void clear_board();
void read_board();
void construct_graph();
bool BFS();
int DFS(int ver, int flow);
int cal_min(int a,int b);
int solve();
void show_graph();

int main(int argc, const char * argv[]) {
    std::cin>>T;
    for(int i=1;i<=T;++i){
        clear_board();
        read_board();
        construct_graph();
        int rst=solve();
        if((rst*2)==(m*n-k)){
            std::cout<<"YES"<<std::endl;
        }
        else{
            std::cout<<"NO"<<std::endl;
        }
    }
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
        if(graph[ver][dst]&&(dis[dst]<0)){
            q.push(dst);
            dis[dst]=dis[ver]+1;
            return true;
        }
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

void construct_graph(){
    memset(graph,0,sizeof(graph));
    for(int i=1;i<=n;++i){//n rows
        for(int j=1;j<=m;++j){//m columns
            if(board[i][j]){
                continue;
            }
            if((i+j)%2==0){
                graph[src][(i<<6)+j]=1;
                graph[(i<<6)+j][((i-1)<<6)+j]=INF;
                graph[(i<<6)+j][((i+1)<<6)+j]=INF;
                graph[(i<<6)+j][(i<<6)+j+1]=INF;
                graph[(i<<6)+j][(i<<6)+j-1]=INF;
            }
            else{
                graph[(i<<6)+j][dst]=1;
                graph[((i-1)<<6)+j][(i<<6)+j]=INF;
                graph[((i+1)<<6)+j][(i<<6)+j]=INF;
                graph[(i<<6)+j+1][(i<<6)+j]=INF;
                graph[(i<<6)+j-1][(i<<6)+j]=INF;
            }
        }
    }
}

void clear_board(){
    for(int i=0;i<BoardSize;++i){
        for(int j=0;j<BoardSize;++j){
            board[i][j]=0;
        }
    }
}

void read_board(){
    std::cin>>n>>m>>k;
    int x,y=0;
    for(int i=1;i<=k;++i){
        std::cin>>x>>y;
        board[x][y]=1;
    }
    dst=(n<<6)+m+1;
}

int cal_min(int a,int b){
    if(a<b){return a;}
    else{return b;}
}
