#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_SIZE 100

int isKeyword(char buffer[]) 
{
    char *keywords[] = {"auto", "break", "case", "char", "const", "continue", "default",
                        "do", "double", "else", "enum", "extern", "float", "for", "goto",
                        "if", "int", "long", "register", "return", "short", "signed",
                        "sizeof", "static", "struct", "switch", "typedef", "union",
                        "unsigned", "void", "volatile", "while"};
    int i;
    int total_keywords = sizeof(keywords) / sizeof(keywords[0]);
    for (i = 0; i < total_keywords; ++i) 
    {
        if (strcmp(keywords[i], buffer) == 0) 
        {
            return 1; 
        }
    }
    return 0; 
}

int main() 
{
    char ch, buffer[15], operators[] = "+-*/%=", punctuations[] = ",;:(){}";
    char op[MAX_SIZE], iden[MAX_SIZE][15], lit[MAX_SIZE][15], key[MAX_SIZE][10], punc[MAX_SIZE][15];
    int op_count = 0, iden_count = 0, lit_count = 0, key_count = 0, punc_count = 0;
    FILE *fp;
    int i, j = 0, k;
    int found;

    fp = fopen("program.txt", "r");
    if (fp == NULL) 
    {
        printf("Error while opening the file\n");
        exit(1);
    }

    while ((ch = fgetc(fp)) != EOF) 
    {
        for (i = 0; i < strlen(operators); ++i) 
        {
            if (ch == operators[i]) 
            {
                found = 0;
                for (k = 0; k < op_count; ++k) 
                {
                    if (op[k] == ch) 
                    {
                        found = 1;
                        break;
                    }
                }
                if (!found) 
                {
                    op[op_count++] = ch;
                }
                break;
            }
        }

        for (i = 0; i < strlen(punctuations); ++i) 
        {
            if (ch == punctuations[i]) 
            {
                int found = 0;
                for (int k = 0; k < punc_count; ++k) 
                {
                    if (punc[k][0] == ch) 
                    {
                        found = 1;
                        break;
                    }
                }
                if (!found) 
                {
                    punc[punc_count][0] = ch;
                    punc[punc_count++][1] = '\0';
                }
                break;
            }
        }

        if (isalnum(ch) || ch == '_') 
        {
            buffer[j++] = ch;
        } 
        else if ((ch == ' ' || ch == '\n' || ispunct(ch)) && (j != 0)) 
        {
            buffer[j] = '\0';
            j = 0;

            if (isKeyword(buffer)) 
            {
                int found = 0;
                for (int k = 0; k < key_count; ++k) 
                {
                    if (strcmp(key[k], buffer) == 0) 
                    {
                        found = 1;
                        break;
                    }
                }
                if (!found) 
                {
                    strcpy(key[key_count++], buffer);
                }
            } 
            else 
            {
                if (isdigit(buffer[0])) 
                {
                    int found = 0;
                    for (int k = 0; k < lit_count; ++k) 
                    {
                        if (strcmp(lit[k], buffer) == 0) 
                        {
                            found = 1;
                            break;
                        }
                    }
                    if (!found) 
                    {
                        strcpy(lit[lit_count++], buffer);
                    }
                } 
                else 
                {
                    int found = 0;
                    for (int k = 0; k < iden_count; ++k) 
                    {
                        if (strcmp(iden[k], buffer) == 0) 
                        {
                            found = 1;
                            break;
                        }
                    }
                    if (!found) 
                    {
                        strcpy(iden[iden_count++], buffer);
                    }
                }
            }
        }
    }

    printf("Operators: ");
    for (i = 0; i < op_count; ++i) 
    {
        printf("%c ", op[i]);
    }
    printf("\n");

    printf("Identifiers: ");
    for (i = 0; i < iden_count; ++i) 
    {
        printf("%s ", iden[i]);
    }
    printf("\n");

    printf("Literals: ");
    for (i = 0; i < lit_count; ++i) 
    {
        printf("%s ", lit[i]);
    }
    printf("\n");

    printf("Keywords: ");
    for (i = 0; i < key_count; ++i) 
    {
        printf("%s ", key[i]);
    }
    printf("\n");

    printf("Punctuations: ");
    for (i = 0; i < punc_count; ++i) 
    {
        printf("%s ", punc[i]);
    }
    printf("\n");

    fclose(fp);
    return 0;
}