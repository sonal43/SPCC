%option noyywrap
%{
	#include<stdio.h>
	#include<string.h>
	int count_upper=0,count_lower=0, i=0, j=0,k;
	char lower[100], upper[100];
%}
%%
[A-Z] {count_upper++;
		upper[i++]=yytext[0];}
[a-z] {count_lower++;
		lower[j++]=yytext[0];}
%%
int main()
{
	char str[20];
	printf("Enter string: ");
	gets(str);
	yy_scan_string(str);
	yylex();

	printf("Upper Letter Count:%d\n",count_upper);
	printf("Upper Case Letters : ");
	for(k=0;k<strlen(upper);k++)
	{
		printf("%c ",upper[k]);
	}
	printf("\nLower Letter Count:%d",count_lower);
	printf("\nLower Case Letters : ");
	for(k=0;k<strlen(lower);k++)
	{
		printf("%c ",lower[k]);
	}
	return 0;
}

