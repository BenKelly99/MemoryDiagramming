#include "drmemory_annotations.h"

int main(){
    long x = 1;
    long* y = new long;
    *y = 2;
    long* z = new long[3];
    z[0] = 3;
    z[1] = 4;
    z[2] = 5;
    long** w = new long*;
    *w = y;
    long* v = z + 1;
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
}