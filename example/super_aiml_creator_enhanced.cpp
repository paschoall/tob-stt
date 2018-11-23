#include <bits/stdc++.h>

#define OUTPUT_FILE "output.aiml"

using namespace std;

struct variants {
	vector<string> v;
	variants(){}
	variants(string file) {
		ifstream in (file + ".set", ios::in);
		if(in.is_open() == false){
			char str[100];
			sprintf(str, "Error opening file %s", file.c_str());
			throw str;
		}
		while(in.eof() == false) {
			string s;
			getline(in, s);
			v.push_back(s);
		}
		in.close();
	}

	string operator[](int pos) {
		if(pos > v.size()) {
			cerr << "Position " << pos << "is invalid\n";
			return "";
		}
		return v[pos];
	}

	int size() {
		return v.size();
	}
};
int flag = 0;

map<string, variants> var;

string create_pattern(string & que, string & ans) {
	string res;
	res += "\t<category>\n";
	res += "\t\t<pattern>";
	

	res += que;
	res += "</pattern>\n\t\t<template>";
	res += ans;
	res += "</template>\n\t</category>\n\n";

	return res;
}

string trim(string & s) {
	string ret;
	char last = ' ';
	for(int i = 0; i < s.size(); ++i) {
		if(s[i] == ' ' and last == ' ') continue;
		ret += s[i];
		last = s[i];
	}

	if(ret[ret.size()-1] == ' ') ret.pop_back();
	return ret;
}

void build_question(vector<string> & list, string & que, int p, string s, string & ans) {
	if(p == que.size()) {
		s = trim(s);
		list.push_back(create_pattern(s, ans));
		if(flag == 0) {
			ans = "<srai>" + s + "</srai>";
			flag = 1;
		}
		return;
	}

	if(que[p] == '?') {
		string x;
		for(int i = p+1; que[i] != '?'; ++i) x += que[i];

		if(var.count(x) == 0) try {
			var[x] = variants(x);
		} catch(const char * message) {
			cout << "fds" << endl;
			cout << message << endl;
			exit(0);
		}
		for(int i = 0; i < var[x].size(); ++i)
			build_question(list, que, p + x.size() + 2, s + var[x][i], ans);
	} else if(que[p] == '^') {
		build_question(list, que, p+1, s, ans);
		build_question(list, que, p+1, s + '*', ans);
	} else build_question(list, que, p+1, s + que[p], ans);
}
vector<string> processLine(vector<string> que, string ans) {
	vector<string> v;

	flag = 0;

	for(string str : que)
		build_question(v, str, 0, "", ans);
	return v;
}

void insert_tabs(string & s) {
	string x;
	for(int i = 0; i < s.size(); ++i) {
		x += s[i];
		if(s[i] == '\n') x += '\t';
	}
	x = '\t' + x;
	if(x[x.size()-1] == '\t') x.pop_back();
	s = x;
}

int main(int argc, char * argv[]) {
	string res = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n";
	string out_file;
	string cur_topic; // current topic

	if(argc != 2 and argc != 3) {
		printf("Usage: %s <input text file> [output file] \n", argv[0]);
		return 0;
	}

	string file = string(argv[1]);
	if(argc == 3) out_file = string(argv[2]);
	else out_file = OUTPUT_FILE;

	ifstream in (file, ios::in);
	if(in.is_open()) {
		while(in.eof() == false) {
			string question, answer;
			
			vector<string> questions;
			while(in.eof() == false and (question.size() == 0 or question[0] == '\n' or question[0] == '-' or question[0] == '@')) {
				getline(in, question);
				if(question.size()) {
					if(question[0] == '-') questions.push_back(question.substr(1));
					else if (question[0] == '@') {
						if(cur_topic == question.substr(1)) {
							res += "\t\t<category><pattern>*</pattern><template><srai><star/></srai></template></category>\n\t</topic>\n";
							cur_topic = "";
						}
						else if(cur_topic == "") {
							cur_topic = question.substr(1);
							res += "\t<topic name = \"" + cur_topic + "\">\n";
						}
						else {
							cerr << "Unformated input\n";
							return 0;
						}
					}
					else if(question[0] != '\n') break;	
				}
			}
			if((question.size() == 0 or question[0] == '\n' or question[0] == '@') and in.eof()) break;

			if(question[0] == '>') answer = question.substr(1);
			else {
				cout << answer << endl;
				cerr << "Unformated input\n";
				return 0;
			}
			
			vector<string> ret = processLine(questions, answer);
			for(string s : ret) {
				if(cur_topic.size()) insert_tabs(s);
				res += s;
			}

		}
		in.close();
		res += "</aiml>\n";
	} else {
		printf("Erro ao abrir arquivo de entrada\n");
		return 0;
	}



	ofstream out (out_file, ios::out);
	if(out.is_open()) {
		out << res;
		out.close();
	} else {
		printf("Erro ao abrir arquivo de saida\n");
		return 0;
	}
}