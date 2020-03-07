import sys
import os
import re
import subprocess
import json


if __name__ == "__main__":
    arguments = " ".join(sys.argv[1::])
    os.system("mkdir -p /tmp/memory_diagram")
    os.system("rm -rf /tmp/memory_diagram/*")
    os.system("g++ " + arguments + " -I/work/drmemory/releases/DrMemory-Linux-2.3.18322/drmf/include /work/drmemory/releases/DrMemory-Linux-2.3.18322/drmf/lib64/release/libdrmemory_annotations.a -o /tmp/memory_diagram/a.out")
    result = subprocess.run("/work/drmemory/releases/DrMemory-Linux-2.3.18322/bin64/drmemory -brief -- /tmp/memory_diagram/a.out", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    json_files = re.findall(r'^\s*~~Dr\.M~~ Memory layout written to: (\/tmp\/Dr\. Memory\/DrMemory-a\.out\..*?\.json)$', result.stderr.decode('utf-8'), re.MULTILINE)
    json_outputs = []
    for file in json_files:
        with open(file) as f:
            json_outputs.append(json.load(f))

    print(json.dumps(json_outputs, indent=4, sort_keys=True))
