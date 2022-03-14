//
//  main.cpp
//  1232-NegativeCycle
//
//  Created by Chalice of the Void on 2022/3/14.
//

#include <iostream>
#include <queue>
#include <vector>

#define MAX_E 5005 //max number of edges
#define MAX_V 3005 //max number of vertices
#define INF 99999999 //initial state of distance
struct Edge {
    int dst;
    int cost;
};//since we assing a list for every vertex, we do not need a src component for edge

std::vector<Edge> edge[MAX_V];//the edges from any vertex
int q_count[MAX_V];//count the times of each vertex in the queue, to judge the existence of negative cycle
bool vis[MAX_V];
std::queue<int> q;//the queue for SPFA
int dist[MAX_V];
int v, e;

void initialize_dist(int src);
void read_input();
bool SPFA();
void show_output(bool c);

int main()
{
    read_input();
    initialize_dist(1);//initialize once for each new vertex that has never been considered
    bool result=SPFA();
    show_output(result);
    return 0;
}

bool SPFA(){
    bool find = false;
    for (int i = 1;i <= v;++i) {
        if (q_count[i] || (i > 1 && dist[i] < INF)) {
            continue;
        }//we want to pick a vertex which has not been considered as source
        q.push(i);
        q_count[i]++;//update the number of q_count each time enqueue happens
        vis[i] = true;
        while (!q.empty()) {
            int cur = q.front();
            q.pop();
            vis[cur] = 0;
            int edgenumber = edge[cur].size();
            for (int j = 0;j < edgenumber;++j) {//for every edge from a single vertex, update the dist
                int currdst = edge[cur][j].dst;
                int currcost = edge[cur][j].cost;
                if (dist[currdst] > dist[cur] + currcost) {
                    dist[currdst] = dist[cur] + currcost;
                    if (!vis[currdst]) {
                        vis[currdst] = 1;
                        q_count[currdst]++;
                        if (q_count[currdst] >= v) {
                            return true;
                        }
                        q.push(currdst);
                    }
                }
            }
        }
    }
    return false;
}

void show_output(bool c) {
    if (c) {
        std::cout << "Yes" << std::endl;
    }
    else {
        std::cout << "No" << std::endl;
    }
}

void read_input() {
    std::cin >> v >> e;
    int x, y, z;
    for (int i = 0;i < e;++i) {
        std::cin >> x >> y >> z;
        Edge tmp;
        tmp.dst = y, tmp.cost = z;
        edge[x].push_back(tmp);
    }
}

void initialize_dist(int src) {
    for (int i = 1;i <= v;++i) {
        dist[i] = INF;
    }
    dist[src] = 0;
}
