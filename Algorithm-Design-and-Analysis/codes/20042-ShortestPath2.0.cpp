#include <iostream>
#include <vector>
#include <queue>

const int MAX_V = 100005;
const int MAX_E = 300005;
const int INF = 0x7fffffff;
struct Edge {
	int cost;
	int to;
	Edge(int a, int b) :cost(a), to(b) {}
	friend bool operator <(const Edge& a,const Edge& b)  { return a.cost < b.cost; }
	friend bool operator ==(const Edge& a, const Edge& b) { return a.cost == b.cost; }
	friend bool operator >(const Edge& a, const Edge& b) { return a.cost > b.cost; }
};
int v, e, s, t;
std::vector<Edge> edges[MAX_V];
int dis[MAX_V];
bool vis[MAX_V];
std::priority_queue<Edge,std::vector<Edge>,std::greater<Edge> > q;
void read_input();
void initialization(int src);
int BFS_dijkstra(int src,int dst);

int main()
{
	read_input();
	initialization(s);
	std::cout << BFS_dijkstra(s,t) << std::endl;
	return 0;
}

int BFS_dijkstra(int src,int dst) 
{
	int size = edges[src].size();
	vis[src] = true;
	for (int i = 0;i < size;++i) {
		q.push(edges[src][i]);
		dis[edges[src][i].to] = edges[src][i].cost;//update without comparison at initialization process
	}
	int currnext = 0;
	int currcost = 0;
	while (!q.empty()) {
		currnext = q.top().to;
		currcost = q.top().cost;
		q.pop();
		if (currnext == dst) {
			return dis[dst];
		}
		if (!vis[currnext]) {
			vis[currnext] = true;
			int curredgenum = edges[currnext].size();
			for (int j = 0;j < curredgenum;++j) {
				Edge tmp(edges[currnext][j].cost, edges[currnext][j].to);
				if (dis[tmp.to] > currcost + tmp.cost) {
					dis[tmp.to] = currcost + tmp.cost;
					q.push(Edge(dis[tmp.to], tmp.to));
				}
			}
		}
	}
	return dis[dst];
}

void initialization(int src)
{
	for (int i = 1;i <= v;++i) {
		dis[i] = INF;
	}
	dis[src] = 0;
}
void read_input()
{
	std::cin >> v >> e >> s >> t;
	int x, y, z;
	for (int i = 1;i <= e;++i) {
		std::cin >> x >> y >> z;
		edges[x].push_back(Edge(z, y));
		edges[y].push_back(Edge(z, x));
	}
}
