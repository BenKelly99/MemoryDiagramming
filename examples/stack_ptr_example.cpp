#include "drmemory_annotations.h"

int main() {
    long x = 10;
    long** y = new long*;
    *y = &x;
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
}