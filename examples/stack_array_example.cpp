#include "drmemory_annotations.h"

int main(){
    long arr[3];
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    long x = 5;
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
}