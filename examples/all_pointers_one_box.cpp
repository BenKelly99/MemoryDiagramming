#include "drmemory_annotations.h"

int main(){
    new long;
    new long;
    new long;
    long* c = new long;
    long* v1 = c;
    long* v2 = c;
    long* v3 = c;
    long* v4 = c;
    long* v5 = c;
    long* v6 = c;
    long* v7 = c;
    long* v8 = c;
    long* v9 = c;
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
}
