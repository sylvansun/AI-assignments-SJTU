#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <algorithm>

long long v, e;
const long long MAX_V = 100005;
struct Edge {
	long long to;
	long long cost;//cost should be either a or b
	long long a;
	long long b;
	Edge(long long t, long long x, long long y) :to(t), a(x), b(y), cost(x) {}//always assume not a bridge
};

struct Edge_sort {
	long long s;
	long long t;
	long long cost;
	Edge_sort(long long a, long long b, long long c) :s(a),t(b),cost(c){}
};
bool cmp(Edge_sort a, Edge_sort b) {
	return a.cost < b.cost;
}
std::vector<Edge_sort> vec;
long long p[MAX_V];//parents of each nodes


//use uG to generate dG and rG, then use dG and rG to find the bridges and mark them in uG, finally find the MST of uG
std::vector<Edge> uG[MAX_V];
std::vector<Edge> dG[MAX_V];
std::vector<Edge> rG[MAX_V];

std::stack<long long> post_order;
bool vis[MAX_V];
long long comp_type[MAX_V];//denote the strongly connected component type of a given vertex

void read_input();
void clear_vis();
void genDFS(long long curr_vertex);//generate dG and rG by DFS search tree
void origDFS(long long curr_vertex);//do DFS on dG and sort the vertices
void revDFS(long long curr_vertex, long long type);//do DFS on rG and assign the type of scc
void find_scc();
void find_bridge();//find the bridges and determine the cost
long long MST();//minimal spanning tree
long long find_p(long long x);//find the parent of x

int main()
{
	read_input();
	genDFS(1);
	find_scc();
	find_bridge();
	std::cout << MST() << std::endl;
	return 0;
}

long long MST()
{
	long long len = vec.size();
	std::sort(vec.begin(), vec.end(),cmp);
	for (long long i = 1;i <= v;++i) {
		p[i] = i;
	}
	long long result = 0;
	long long edge_count = 0;
	for (long long i = 0;i < len;++i) {
		Edge_sort curr = vec[i];
		long long ps = find_p(curr.s);
		long long pt = find_p(curr.t);
		if (ps != pt) {
			edge_count++;
			result += curr.cost;
			if (edge_count == v - 1) {
				return result;
			}
			p[ps] = pt;//change the father
		}
	}
	return result;
}

long long find_p(long long x)
{
	if (p[x] == x) { return x; }
	p[x] = find_p(p[x]);
	return p[x];
}

void find_bridge()
{
	for (long long i = 1;i <= v;++i) {
		long long curr_type = comp_type[i];
		long long edge_number = uG[i].size();
		for (long long j = 0;j < edge_number;++j) {
			long long next_vertex = uG[i][j].to;
			if (next_vertex < i) { continue; }//we only find once
			if (comp_type[next_vertex] != curr_type) {//find a bridge when edge polong longing out of scc
				uG[i][j].cost = uG[i][j].b;//adjust the cost for bridges
			}
			vec.push_back(Edge_sort(i, next_vertex, uG[i][j].cost));
		}
	}
}

void find_scc()
{
	clear_vis();
	for (long long i = 1;i <= v;++i) {
		if (!vis[i]) {
			origDFS(i);
		}
	}
	clear_vis();
	long long component_type = 0;
	while (!post_order.empty()) {
		long long curr_vertex = post_order.top();
		post_order.pop();
		if (!vis[curr_vertex]) {
			revDFS(curr_vertex, ++component_type);
		}
	}
}

void revDFS(long long curr_vertex, long long type) {
	vis[curr_vertex] = true;
	comp_type[curr_vertex] = type;
	long long edge_number = rG[curr_vertex].size();
	for (long long i = 0;i < edge_number;++i) {
		long long next_vertex = rG[curr_vertex][i].to;
		if (!vis[next_vertex]) {
			revDFS(next_vertex, type);
		}
	}
}

void origDFS(long long curr_vertex) {
	vis[curr_vertex] = true;//mark the vertex as visited
	long long edge_number = dG[curr_vertex].size();
	for (long long i = 0;i < edge_number;++i) {
		long long next_vertex = dG[curr_vertex][i].to;
		if (!vis[next_vertex]) {
			origDFS(next_vertex);
		}
	}
	post_order.push(curr_vertex);
}

void genDFS(long long curr_vertex) {
	vis[curr_vertex] = true;//mark the vertex as visited
	long long edge_number = uG[curr_vertex].size();
	for (long long i = 0;i < edge_number;++i) {
		Edge curr_edge(uG[curr_vertex][i]);//actually a faster way to copy an edge
		long long next_vertex = curr_edge.to;
		//Edge curr_edge(next_vertex, uG[curr_vertex][i].a, uG[curr_vertex][i].b);//
		if (!vis[next_vertex]) {//a tree edge
			genDFS(next_vertex);
			dG[curr_vertex].push_back(curr_edge);
			rG[next_vertex].push_back(Edge(curr_vertex,curr_edge.a,curr_edge.b));
		}
		else {//a back edge
			dG[next_vertex].push_back(Edge(curr_vertex, curr_edge.a, curr_edge.b));
			rG[curr_vertex].push_back(curr_edge);
		}
	}
}

void clear_vis()
{
	for (long long i = 1;i <= v;++i) {
		vis[i] = false;
	}
}
void read_input()
{
	std::cin >> v >> e;
	long long s, t, x, y;
	for (long long i = 1;i <= e;++i) {
		std::cin >> s >> t >> x >> y;
		uG[s].push_back(Edge(t, x, y));
		uG[t].push_back(Edge(s, x, y));
	}
}
