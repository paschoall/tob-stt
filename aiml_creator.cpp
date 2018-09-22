#include <bits/stdc++.h>

#define OUTPUT_FILE "output.aiml"

#define debug if(true)

using namespace std;

struct variants {
	vector<string> v;
	variants(){}
	variants(string file) {
		ifstream in (file + ".set", ios::in);
		if(in.is_open() == false) throw "Error opening file";
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
	res += "\t\t<pattern> ";
	

	res += que;
	res += "</pattern>\n\t\t<template> ";
	res += ans;
	res += "</template>\n\t</category>\n\n";

	return res;
}

void build_question(vector<string> & list, string & que, int p, string s, string & ans) {
	if(p == que.size()) {
		list.push_back(create_pattern(s, ans));
		if(flag == 0) {
			ans = "<srai> " + s + " </srai>";
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
			cout << message << endl;
			exit(0);
		}
		for(int i = 0; i < var[x].size(); ++i)
			build_question(list, que, p + x.size() + 2, s + var[x][i], ans);
	} else build_question(list, que, p+1, s + que[p], ans);
}
vector<string> processLine(string que, string ans) {
	vector<string> v;

	flag = 0;

	build_question(v, que, 0, "", ans);
	return v;
}

int main(int argc, char * argv[]) {
	string res = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n";
	string out_file;

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
			
			while(in.eof() == false and (question.size() == 0 or question[0] == '\n')) getline(in, question);
			while(in.eof() == false and (answer.size() == 0 or answer[0] == '\n')) getline(in, answer);
			if(in.eof()) break;
			
			vector<string> ret = processLine(question, answer);
			for(string s : ret) res += s;

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