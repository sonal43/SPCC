%option noyywrap
%{
#include<stdio.h>
#include<string.h>
int token_count=0;
%}

%%
[ \t\n]        ;
[0-9]+         { printf(" '%s' ", yytext); token_count++;}
[A-Za-z]+     { printf(" '%s' ", yytext); token_count++;}
\"[^\"\n]*\"  { printf(" '%s' ", yytext); token_count++;}
[(){};,"]    { printf(" '%s' ", yytext); token_count++;}
.				;
%%

int main()
{
    char str[100];
    printf("Enter string: ");
    fgets(str, sizeof(str), stdin);
    printf("Tokens: ");
    yy_scan_string(str);
    yylex();

    printf("\nToken Count: %d\n", token_count);
    return 0;
}

