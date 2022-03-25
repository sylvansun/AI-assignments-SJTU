#include <iostream>
#include <queue>
#include <cmath>

const int MAX_N = 100005;
long long num, weight;
double ratio;
std::priority_queue<long long,std::vector<long long>,std::greater<long long> > q;

void read_input();
long long solve();
int main()
{
	read_input();
	std::cout << solve() << std::endl;
}

long long solve() {
	long long rst = 0;
	long long a, b=0;
	while (!q.empty()) {//actually this clause never used
		a = q.top();
		q.pop();
		b = q.top();
		q.pop();
		rst += (a + b);
		if (q.empty()) { break; }
		else {
			q.push(a + b);
		}
	}
	double result = (double)rst * ratio / 100;
	return (long long)ceil(result);
}
void read_input() {
	std::cin >> num >> weight >> ratio;
	long long tmp;
	for (int i = 0;i < num;++i) {
		std::cin >> tmp;
		q.push(tmp);
	}
}
