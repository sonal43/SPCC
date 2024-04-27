%option noyywrap
%{
	#include<stdio.h>
	int flag=0;
%}

%%
([aA][nN][dD]|[oO][rR]|[bB][uU][tT]|[iI][fF]|[tT][hH][eE][nN]|[bB][eE][cC][aA][uU][sS][eE]|[yY][eE][tT]) {flag=1;}
%%
 
 int main()
 {
 	char str[100];
	printf("Enter the sentence: ");
	gets(str);
	yy_scan_string(str);
	yylex();
	if(flag==1)
		printf("\nIt is a compound sentence.");
	else
		printf("\nIt is a simple sentence."); 
		
	return 0;
}

