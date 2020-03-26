#include "drmemory_annotations.h"

int main(){
    long var_x = 1;
    long* var_y = new long;
    *var_y = 2;
    long* var_z = new long[3];
    var_z[0] = 3;
    var_z[1] = 4;
    var_z[2] = 5;
    long** var_w = new long*;
    *var_w = var_y;
    long* var_v = var_z + 1;
    DRMEMORY_ANNOTATE_DUMP_MEMORY_LAYOUT();
    long y = 100;
}