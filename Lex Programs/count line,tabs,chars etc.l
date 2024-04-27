%option noyywrap
%{
#include <stdio.h>
#include <string.h>
int charCount = 0;
int wordCount = 0;
int sentenceCount = 0;
int lineCount = 0;
int numberCount = 0;
int spaceCount = 0;
int end = 0;
%}

%%
[A-Za-z]+       { charCount += strlen(yytext); wordCount++; }
[ \t]           { spaceCount++; }
[0-9]+          { numberCount++; }
\n              { lineCount++; }
[.!?]           { sentenceCount++; }
%%

int main()
{
    printf("Enter the text:\n");

    while (!end) 
    {
        yylex();
        if (feof(yyin) || sentenceCount > 0) 
        {
            break;
        }
    }

    printf("Character count: %d\n", charCount);
    printf("Word count: %d\n", wordCount);
    printf("Sentence count: %d\n", sentenceCount);
    printf("Line count: %d\n", lineCount);
    printf("Number count: %d\n", numberCount);
    printf("Space count: %d\n", spaceCount);

    return 0;
}

