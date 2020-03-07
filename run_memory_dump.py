import sys
import os

if __name__ == "__main__":
    arguments = " ".join(sys.argv[1::])
    os.system("mkdir -p /tmp/memory_diagram")
    os.system("rm -rf /tmp/memory_diagram/*")
    os.system("g++ " + arguments + " -I/work/drmemory/releases/DrMemory-Linux-2.3.18322/drmf/include /work/drmemory/releases/DrMemory-Linux-2.3.18322/drmf/lib64/release/libdrmemory_annotations.a -o /tmp/memory_diagram/a.out")
    os.system("/work/drmemory/releases/DrMemory-Linux-2.3.18322/bin64/drmemory -brief -- /tmp/memory_diagram/a.out")
