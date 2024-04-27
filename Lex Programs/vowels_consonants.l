%option noyywrap
%{
	#include<stdio.h>
	#include<string.h>
	int i=0,j=0,k;
	char vowels[20], cons[20];
%}
%%
[A-Za-z] {
			if(strchr("aeiouAEIOU",yytext[0]) != 0)
			{
				vowels[i++]=yytext[0];
			}
			else
			{
				cons[j++]=yytext[0];
			}
		}
%%
int main()
{
	char str[20];
	printf("Enter string: ");
	gets(str);
	yy_scan_string(str);
	yylex();

	printf("Vowels Count:%d\n",i);
	printf("Vowels : ");
	for(k=0;k<strlen(vowels);k++)
	{
		printf("%c ",vowels[k]);
	}
	printf("\nConsonants Count:%d",j);
	printf("\nConsonants : ");
	for(k=0;k<strlen(cons);k++)
	{
		printf("%c ",cons[k]);
	}
	return 0;
}

