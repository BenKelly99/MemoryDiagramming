# MemoryDiagramming

This project is designed to create memory diagrams for C++ programs
for use in debugging or educational environments. The program is
reliant on an memory annotation feature in [Dr. Memory](https://github.com/DynamoRIO/drmemory)

Authors:
Ben Kelly
ELi Schiff

Instructions for installing Dr. Memory for use in Memory Diagramming:

At the current phase in development, the program relies on Dr. Memory
being installed in a specific location and using a specific version.
Linux is the only OS currently supported by the diagramming tool.

Create and navigate to directory `/work/DrMemory/releases/`

`wget https://github.com/DynamoRIO/drmemory/releases/download/release_2.3.18351/DrMemory-Linux-2.3.18351.tar.gz`

`tar -xzf DrMemory-Linux-2.3.18351.tar.gz`

You will need a recent version of the g++ compiler, the gdb debugging tool, and python3
First, clone the repository:

`git clone https://github.com/BenKelly99/MemoryDiagramming.git`

Navigate to the folder containing the repo

To run the tool, use
`python3 run_memory_dump.py foo.cpp` where foo.cpp is the souce file you wish to use

Features and limitations:
Currently, we support programs with only a main function. Programs with functions may work,
but cannot be guaranteed to run properly.
The tool support both dynamically and statically allocated primitives, arrays, and objects.
