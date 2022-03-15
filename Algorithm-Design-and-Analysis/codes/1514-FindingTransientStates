//
//  main.cpp
//  1514.RandomWalk
//
//  Created by Chalice of the Void on 2022/3/15.
//

#include <iostream>
#include <stack>
#include <vector>

//global variables
const int MAX_V=500005;
std::vector<int> orig_graph[MAX_V];
std::vector<int> rev_graph[MAX_V];//the graph with same vertices but all edges reversed
std::stack<int> post_order;//push a vertex after leaving
bool vis[MAX_V];
int comp_type[MAX_V];//denote the strongly connected component type of a given vertex
int type_number[MAX_V];//number of vertices of each components
int v,e;//number of vertices and edges

//function definition region
void read_input();
void DFS(int curr_vertex);//do DFS on the original graph and sort the vertices
void revDFS(int curr_vertex,int type);//do DFS on the reversed graph and assign the type of strongly connected compenonts for each vertex
void sc_components();//calculate the strongly connected components
int find_transience();//find the number of transient states

//main procedure
int main(int argc, const char * argv[]) {
    read_input();
    sc_components();
    std::cout<<find_transience()<<std::endl;
    return 0;
}

//function implementation region
int find_transience(){
    int result=0;
    for(int i=1;i<=v;++i){
        int curr_type=comp_type[i];
        if(!type_number[curr_type]){
            continue;//if we have counted the number of transient state for this specific scc, then do not have to consider it again.
        }
        int edge_number=orig_graph[i].size();
        for(int j=0;j<edge_number;++j){
            int next_vertex=orig_graph[i][j];
            if(comp_type[next_vertex]!=comp_type[i]){//out-degree of scc not equal to zero, find a transient state
                result+=type_number[curr_type];
                type_number[curr_type]=0;
                break;
            }
        }
    }
    return result;
}

void sc_components(){
    for(int i=1;i<=v;++i){
        if(!vis[i]){
            DFS(i);
        }
    }
    for(int i=1;i<=v;++i){
        vis[i]=false;//clear the vis array so that it can be reused for the reverse DFS process
    }
    int component_type=0;
    while(!post_order.empty()){
        int curr_vertex=post_order.top();
        post_order.pop();
        if(!vis[curr_vertex]){
            revDFS(curr_vertex,++component_type);
        }
    }
    //if the program requires us to return the number of sc_components, we can return the value of type here...
}

void revDFS(int curr_vertex,int type){
    vis[curr_vertex]=true;
    comp_type[curr_vertex]=type;
    type_number[type]++;
    int edge_number=rev_graph[curr_vertex].size();
    for(int i=0;i<edge_number;++i){
        int next_vertex=rev_graph[curr_vertex][i];
        if(!vis[next_vertex]){
            revDFS(next_vertex,type);
        }
    }
}

void DFS(int curr_vertex){
    vis[curr_vertex]=true;//mark the vertex as visited
    int edge_number=orig_graph[curr_vertex].size();
    for(int i=0;i<edge_number;++i){
        int next_vertex=orig_graph[curr_vertex][i];
        if(!vis[next_vertex]){
            DFS(next_vertex);
        }
    }
    post_order.push(curr_vertex);
}

void read_input(){
    int src,dst;
    std::cin>>v>>e;
    for(int i=0;i<e;++i){
        std::cin>>src>>dst;
        orig_graph[src].push_back(dst);
        rev_graph[dst].push_back(src);
    }
}
