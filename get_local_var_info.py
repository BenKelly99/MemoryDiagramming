import gdb

class Variable:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

variables = []
frame = gdb.selected_frame()
block = frame.block()
while(block):
    for symbol in block:
        if (symbol.is_argument or symbol.is_variable):
            var_info = {}
            ptr_level = 0
            var_type = symbol.type
            while(var_type.code == gdb.TYPE_CODE_PTR):
                ptr_level += 1
                var_type = var_type.target()
            var_type_str = str(var_type.name) + "*" * ptr_level
            print("(" + var_type_str + ") " + symbol.name + ": " + str(symbol.value(frame)));
            variables.append(Variable(symbol.name, var_type_str, str(symbol.value(frame))));
    block = block.superblock
print("##### GDB DEBUG INFO BEGIN ####")
print("VARIABLES")
for var in variables:
    gdb.execute("p \"" + var.name + " offset\"")
    gdb.execute("p (void*) &" + var.name + " - $sp")
print("##### GDB DEBUG INFO END ####")