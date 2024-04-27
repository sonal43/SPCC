%option noyywrap
%{
	#include<stdio.h>
%}
%%
%%
int main()
{
	printf("Hello World!");
	yylex();
	return 0;
}

