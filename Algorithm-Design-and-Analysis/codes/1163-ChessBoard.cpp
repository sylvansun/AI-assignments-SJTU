//
//  main.cpp
//  1163.Chessboard
//
//  Created by Chalice of the Void on 2022/4/21.
//

#include <iostream>

const int MAX_M=205;
const int MAX_N=10;
const int DIV=1000000007;
int m,n,k;
bool obstacle_board[MAX_N][MAX_M];
int s1[64][64];
int s2[64][64];//show current state and next state

void read_input();
void show_obstacle();
void show_state();
int pow2(int a);
void copy_state();//copy the state of s2 and put it into s1
int solve();

int main(int argc, const char * argv[]) {
    read_input();
    std::cout<<solve()<<std::endl;
    return 0;
}

int solve(){
    int result=0;
    int size=pow2(n);
    //first initialize s2 array
    int cc=1;//current column
    for(int i=0;i<size;++i){
        for(int j=0;j<size;++j){
            int obs1=0;
            int obs2=0;
            for(int k=1;k<=n;++k){//calculate the obstacle state of current and next column
                obs1=obs1|(obstacle_board[k][cc]<<(n-k));
                obs2=obs2|(obstacle_board[k][cc+1]<<(n-k));
            }
            if((i&obs1)||(j&obs2)){
                s2[i][j]=0;
            }
            else if(((i<<2)&j)||((j<<2)&i)){
                s2[i][j]=0;
            }
            else{
                s2[i][j]=1;
            }
        }
    }
    //show_state();
    //then solve the problem
    for(int col=2;col<=m-1;col++){
        copy_state();
        cc=col;
        for(int i=0;i<size;++i){
            for(int j=0;j<size;++j){
                int obs1=0;
                int obs2=0;
                for(int k=1;k<=n;++k){//calculate the obstacle state of current and next column
                    obs1=obs1|(obstacle_board[k][cc]<<(n-k));
                    obs2=obs2|(obstacle_board[k][cc+1]<<(n-k));
                }
                if((i&obs1)||(j&obs2)){
                    s2[i][j]=0;
                }
                else if(((i<<2)&j)||((j<<2)&i)){
                    s2[i][j]=0;
                }
                else{
                    s2[i][j]=0;
                    for(int k=0;k<size;++k){
                        if(((j<<1)&k)||((k<<1)&j)){
                            continue;
                        }
                        s2[i][j]+=s1[k][i];
                        s2[i][j]%=DIV;
                    }
                }
            }
        }
        //show_state();
    }
    for(int i=0;i<size;++i){
        for(int j=0;j<size;++j){
            result+=s2[i][j];
            result%=DIV;
        }
    }
    return result;
}

void copy_state(){
    for(int i=0;i<64;++i){
        for(int j=0;j<64;++j)
            s1[i][j]=s2[i][j];
    }
}

void show_state(){
    int size=pow2(n);
    for(int i=0;i<size;++i){
        for(int j=0;j<size;++j){
            std::cout<<s2[i][j]<<" ";
        }
        std::cout<<std::endl;
    }
}

void show_obstacle(){
    for(int i=1;i<=n;++i){
        for(int j=1;j<=m;++j){
            std::cout<<obstacle_board[i][j]<<" ";
        }
        std::cout<<std::endl;
    }
}

int pow2(int a){
    int result=1;
    for(int i=1;i<=a;++i){
        result*=2;
    }
    return result;
}
void read_input(){
    std::cin>>m>>n>>k;
    int a,b=0;
    for(int i=0;i<k;++i){
        std::cin>>a>>b;
        obstacle_board[b][a]=true;
    }
}
