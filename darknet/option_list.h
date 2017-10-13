#ifndef OPTION_LIST_H
#define OPTION_LIST_H
#include "list.h"

typedef struct{
    char *key;
    char *val;
    int used;
} kvp;


int read_option(char *s, mlist *options);
void option_insert(mlist *l, char *key, char *val);
char *option_find(mlist *l, char *key);
int option_find_int_quiet(mlist *l, char *key, int def);
float option_find_float(mlist *l, char *key, float def);
float option_find_float_quiet(mlist *l, char *key, float def);
void option_unused(mlist *l);

#endif
