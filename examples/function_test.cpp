#include "drmemory_annotations.h"

void function(){
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
    return;
}

int main(){
    long x = 5;
    long* y = new long;
    *y = 5;
    function();
}