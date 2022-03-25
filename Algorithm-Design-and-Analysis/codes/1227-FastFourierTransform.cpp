/*

DISCLAIMER FOR HONOR CODES

Our teacher recommends that we should learn from the template for this code in order to 
understand the elegant way in which the author implements the FFT. So I googled and found 
a version I think is pretty from a website "oiwiki". Here the FFT function is completely 
from that website. I studied this function for a long time and understands its entire idea
now. I do not think that I can write a better version than this.

*/


#include <iostream>
#include <cmath>
#include <complex>

typedef std::complex<double> Comp;  // STL complex
#define M_PI  3.1415926535897932384626433832795028841971694
const int MAX_N = 1 << 20;

Comp tmp[MAX_N];
Comp a[MAX_N], b[MAX_N];

void FFT(Comp* f, int n, int rev) {
    if (n == 1) return;
    for (int i = 0; i < n; ++i) tmp[i] = f[i];
    for (int i = 0; i < n; ++i) {
        if (i & 1)
            f[n / 2 + i / 2] = tmp[i];
        else
            f[i / 2] = tmp[i];
    }
    Comp* g = f, * h = f + n / 2;
    FFT(g, n / 2, rev), FFT(h, n / 2, rev);
    Comp cur(1, 0), step(cos(2 * M_PI / n), sin(2 * M_PI * rev / n));
    for (int k = 0; k < n / 2; ++k) {
        tmp[k] = g[k] + cur * h[k];
        tmp[k + n / 2] = g[k] - cur * h[k];
        cur *= step;
    }
    for (int i = 0; i < n; ++i) f[i] = tmp[i];
}

int total_l;
//a function that returns the minimum of 2's power larger than n
int power2_generate(int n);
//a function that reads the input and calculates the length of transformation
int read_input();
//show result
void show_output(int len);

int main()
{
    int len = read_input();
    FFT(a, len, 1);
    FFT(b, len, 1);
    for (int i = 0;i < len;++i) {
        a[i] = a[i] * b[i];
    }
    FFT(a, len, -1);
    show_output(len);
    return 0;
}

void show_output(int len)
{
    for (int i = 0;i < total_l;++i) {
        double tmp = a[i].real() / len;
        int rst;
        if (tmp > 0) {
            rst = (int)(tmp + 0.5);
        }
        else {
            rst = (int)(tmp - 0.5);
        }
        std::cout << rst << " ";
    }
    std::cout << std::endl;
}
int read_input()
{
    int n, m, len;
    std::cin >> n >> m;
    len =  power2_generate(m + n + 1);
    total_l = m + n + 1;
    for (int i = 0;i <= n;++i) {
        std::cin >> a[i];
    }
    for (int i = 0;i <= m;++i) {
        std::cin >> b[i];
    }
    return len;
}
int power2_generate(int n)
{
    int result = 2;
    while (result < n) {
        result = result << 1;
    }
    return result;
}
