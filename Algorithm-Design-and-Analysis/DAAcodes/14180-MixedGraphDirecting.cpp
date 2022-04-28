#include <iostream>
#include <queue>

#define MAX_N 100005

int degree[MAX_N];//the in-degree of the n vertices
int order[MAX_N];//the topological order after the directed edges are all added
std::queue<int> edges[MAX_N];//edges[i] contains all directed edges from vertex i
std::queue<int> deg0;//a dynamic queue contain all vertices with degree 0
int currod;//current order in the topological sorting process
int n, p1, p2;

void read_input();
void show_output();
void partial_tpsort();

int main()
{
	read_input();
	partial_tpsort();
	show_output();
	return 0;
}

void partial_tpsort() {
	int currver;//current vertex 
	int nextver;//next vertex
	while (!deg0.empty()) {
		currver = deg0.front();
		deg0.pop();
		while (!edges[currver].empty()) {//consider all directed edges from vertex currver
			nextver = edges[currver].front();
			edges[currver].pop();
			degree[nextver]--;
			if (!degree[nextver]) {//becomes a source
				deg0.push(nextver);
				order[nextver] = ++currod;
			}
		}
	}
}

void read_input() {
	std::cin >> n >> p1 >> p2;
	int a, b;//denote the edges in loop
	for (int i = 0;i < p1;i++) {
		std::cin >> a >> b;
		edges[a].push(b);
		degree[b]++;
	}
	for (int i = 1;i <= n;++i) {
		if (!degree[i]) {
			deg0.push(i);
			order[i] = ++currod;
		}
	}
}
void show_output() {
	int a, b;
	for (int i = 0;i < p2;++i) {
		std::cin >> a >> b;
		if (order[a] < order[b]) {
			std::cout << a << " " << b << std::endl;
		}
		else {
			std::cout << b << " " << a << std::endl;
		}
	}
}
