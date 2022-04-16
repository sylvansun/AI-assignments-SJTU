//
//  main.cpp
//  14385.EditDistance
//
//  Created by Chalice of the Void on 2022/4/16.
//

#include <iostream>
#include <string>

const int MAX_N=3005;
int dp[MAX_N][MAX_N];
std::string a,b;//the string to edit
int x,y;//two kind of costs
int al,bl;//length of strings

void read_input();
void init_dp();
int solve();
int cal_min(int a,int b,int c);
void show_state();

int main(int argc, const char * argv[]) {
    read_input();
    init_dp();
    std::cout<<solve()<<std::endl;
    return 0;
}

int solve(){//note that al represent columns and bl represent rows
    for(int i=1;i<=bl;++i){
        for(int j=1;j<=al;++j){
            if(b[i-1]==a[j-1]){
                dp[i][j]=cal_min(dp[i-1][j]+x,dp[i][j-1]+x,dp[i-1][j-1]);
            }
            else{
                dp[i][j]=cal_min(dp[i-1][j]+x,dp[i][j-1]+x,dp[i-1][j-1]+y);
            }
        }
    }
    return dp[bl][al];
}

void init_dp(){
    for(int i=1;i<=al;++i){
        dp[0][i]=i*x;
    }
    for(int i=1;i<=bl;++i){
        dp[i][0]=i*x;
    }
}

void read_input(){
    std::cin>>x>>y;
    std::cin>>a>>b;
    al=a.length();
    bl=b.length();
}

void show_state(){
    for(int j=0;j<=bl;++j){
        for(int i=0;i<=al;++i){
            std::cout<<dp[j][i]<<" ";
        }
        std::cout<<std::endl;
    }
    
}
int cal_min(int a,int b,int c){
    int result=a;
    if(b<result){
        result=b;
    }
    if(c<result){
        result=c;
    }
    return result;
}
