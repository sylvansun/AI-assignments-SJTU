#include <iostream>
#include <vector>
#include <queue>

#define max_ve 1000005 //maximum size of vertices and edges
struct edge {
	int end;
	int cost;
};//An edge with end and cost
bool vis[max_ve];
std::vector<edge> ver[max_ve];
int v, e, s, t;

void read_input();
int BFS();

int main()
{
	read_input();
	std::cout << BFS() << std::endl;
	return 0;
}

int BFS() {
	int result = 0;
	std::queue<int> loc;
	std::queue<int> next;
	loc.push(s);
	vis[s] = 1;
	bool arrived = false;
	while (!loc.empty() || !next.empty()) {
		while (!loc.empty()) {//localize all vertices with no cost
			int curr = loc.front();
			loc.pop();
			if (curr == t) {
				arrived = true;
				break;
			}
			int size = ver[curr].size();
			for (int i = 0;i < size;++i) {
				if (vis[ver[curr][i].end]) {//have visited this vertex
					continue;
				}
				if (ver[curr][i].cost) {
					next.push(ver[curr][i].end);
				}
				else {
					loc.push(ver[curr][i].end);
					vis[ver[curr][i].end] = 1;
				}
			}
		}
		if (arrived) {
			break;
		}
		while (!next.empty()) {
			int tmp = next.front();
			vis[tmp] = 1;
			loc.push(tmp);
			next.pop();
		}
		result++;
	}
	return result;
}

void read_input() {
	std::cin >> v >> e >> s >> t;
	int src, dst, len;
	for (int i = 1;i <= e;++i) {
		std::cin >> src >> dst >> len;
		edge tmp;
		tmp.end = dst, tmp.cost = len;
		ver[src].push_back(tmp);
		tmp.end = src;
		ver[dst].push_back(tmp);
	}
}
