#ifndef LIST_H
#define LIST_H
#include "darknet.h"

mlist *make_list();
int list_find(mlist *l, void *val);

void list_insert(mlist *, void *);


void free_list_contents(mlist *l);

#endif
