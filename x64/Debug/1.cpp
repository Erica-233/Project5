#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 检查字符串是否对称
bool isPalindrome(const string& s) {
    int n = s.length();
    for (int i = 0; i < n / 2; ++i) {
        if (s[i] != s[n - i - 1]) {
            return false;
        }
    }
    return true;
}

int main() {
    vector<string> strings;
    string s;
    while (cin >> s) {
        strings.push_back(s);
    }

    // 按长度和字典序排序对称字符串
    sort(strings.begin(), strings.end(), [](const string& a, const string& b) {
        if (a.size() != b.size()) return a.size() < b.size();
        return a < b;
    });

    // 输出对称字符串
    for (const auto& str : strings) {
        if (isPalindrome(str)) {
            cout << str << endl;
        }
    }

    return 0;
}