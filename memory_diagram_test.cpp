#include "drmemory_annotations.h"
#include <iostream>

int main()
{
    int i,**j,k,l,*m;
    i = 0;
    j = new int*[3];
    j[0] = new int;
    j[1] = &i;
    m = *(j+1);
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
    j[1] = &k;
    k=10;
    *(j[0]) = 5;
    j[2] = j[0];
    *(j[0]) = 18;
    *m = 4;
    l = 3;
    char *ch = new char[13];
    ch[4] = 'x';
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
    std::cerr << "goodbye\n";
    return 0;
}