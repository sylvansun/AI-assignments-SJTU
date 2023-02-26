#include <iostream>
#include <map>
#include <vector>
#include <string>

using namespace std;

class Solution {
private:
    map<char,int> letter_count;
    map<char,int> current_count;
    int words_num;
    int states;
public:
    void store_letters(vector<char>& letters){
        int len = letters.size();
        for(char c='a';c<='z';++c){
            letter_count[c]=0;
            current_count[c]=0;
        }
        for(int i=0;i<len;++i){
            letter_count[letters[i]]+=1;
        }
    }
    void show_count(){
        for(char c='a';c<='z';++c){
            cout<<current_count[c]<<" ";
        }
        cout<<endl;
    }
    bool add_word(string& s){
        bool valid = true;
        int len = s.size();
        for(int i=0;i<len;++i){
            char cur = s[i];
            current_count[cur]+=1;
            if(current_count[cur]>letter_count[cur]){
                valid = false;
            }
        }
        return valid;
    }
    bool check_valid(){
        bool valid = true;
        for(char c='a';c<='z';++c){
            if(current_count[c]>letter_count[c]){
                valid = false;
            }
        }
        return valid;
    }
    void delete_word(string& s){
        int len = s.size();
        for(int i=0;i<len;++i){
            current_count[s[i]]-=1;
        }
    }
    int maxScoreWords(vector<string>& words, vector<char>& letters, vector<int>& score) {
        store_letters(letters);
        words_num = words.size();
        states = (1<<words_num)-1;
        int final_result = 0;
        for (int i=1;i<=states;++i){
            int whichword = -1;
            bool valid = false;
            int result = 0;
            for (int j=1;j<states;j=(j<<1)){
                whichword++;
                bool prev = (i-1)&j;
                bool next = (i)&j;
                
                //show_count();
                if(prev&&!next){
                    delete_word(words[whichword]);
                }
                if(!prev&&next){
                    add_word(words[whichword]);
                }
                //show_count();
            }
            valid = check_valid();
            if(valid){
                for(char c='a';c<='z';++c){
                    result += current_count[c]*score[c-'a'];
                }
                if(result>final_result){
                    final_result = result;
                    cout<<"state "<<i<<endl;
                }
            }
        }
        return final_result;
    }
};

int main(){
    Solution s;
    vector<string> words = {"dog","cat","dad","good"};
    vector<char> letters = {'a','a','c','d','d','d','g','o','o'};
    vector<int> score = {1,0,9,5,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0};
    cout<<s.maxScoreWords(words,letters,score)<<endl;
    //cout<<"hello world"<<endl;
    return 0;
}