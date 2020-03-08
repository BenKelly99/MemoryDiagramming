#include "drmemory_annotations.h"
#include <iostream>

int main()
{
    long i,**j,k,l,*m;
    i = 0;
    j = new long*[3];
    j[0] = new long;
    j[1] = &i;
    m = *(j+1);
    j[1] = &k;
    k=10;
    *(j[0]) = 5;
    j[2] = j[0];
    *(j[0]) = 18;
    *m = 4;
    l = 3;
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
    return 0;
}