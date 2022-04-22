//
//  main.cpp
//  1163.Chessboard
//
//  Created by Chalice of the Void on 2022/4/21.
//

#include <iostream>
#include <cmath>

const int MAX_M=205;
const int MAX_N=10;
const int MAX_SIZE=64;
const int DIV=1000000007;
int m,n,k;//size m*n with k obstacles
bool obstacle_board[MAX_N][MAX_M];
int s1[MAX_SIZE][MAX_SIZE];
int s2[MAX_SIZE][MAX_SIZE];//show current state and next state

void read_input();
void copy_state();//copy the state of s2 and put it into s1
int solve();

int main(int argc, const char * argv[]) {
    read_input();
    std::cout<<solve()<<std::endl;
    return 0;
}

int solve(){
    int size=pow(2,n);
    for(int col=1;col<=m-1;col++){//enumerate the current column
        copy_state();
        for(int i=0;i<size;++i){
            for(int j=0;j<size;++j){
                int obs1=0;
                int obs2=0;
                for(int k=1;k<=n;++k){//calculate the obstacle state of current and next column
                    obs1=obs1|(obstacle_board[k][col]<<(n-k));
                    obs2=obs2|(obstacle_board[k][col+1]<<(n-k));
                }
                if((i&obs1)||(j&obs2)||((i<<2)&j)||((j<<2)&i)){//impossible states
                    s2[i][j]=0;
                }
                else{
                    s2[i][j]=0;
                    if(col==1){//initialization
                        s2[i][j]=1;
                    }
                    for(int k=0;k<size;++k){
                        if(((j<<1)&k)||((k<<1)&j)){//impossible states
                            continue;
                        }
                        s2[i][j]+=s1[k][i];
                        s2[i][j]%=DIV;
                    }
                }
            }
        }
    }
    int result=0;
    for(int i=0;i<size;++i){
        for(int j=0;j<size;++j){
            result+=s2[i][j];
            result%=DIV;
        }
    }
    return result;
}

void copy_state(){
    for(int i=0;i<MAX_SIZE;++i){
        for(int j=0;j<MAX_SIZE;++j)
            s1[i][j]=s2[i][j];
    }
}

void read_input(){
    std::cin>>m>>n>>k;
    int a,b=0;
    for(int i=0;i<k;++i){
        std::cin>>a>>b;
        obstacle_board[b][a]=true;
    }
}
