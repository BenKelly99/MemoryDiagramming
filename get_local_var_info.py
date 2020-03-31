import gdb

class Variable:
    def __init__(self, name, type, value, base_size):
        self.name = name
        self.type = type
        self.value = value
        self.base_size = base_size

variables = []
frame = gdb.selected_frame()
block = frame.block()
while(block):
    for symbol in block:
        if (symbol.is_argument or symbol.is_variable):
            var_info = {}
            var_type = symbol.type
            last_arr = None
            ptr_array_end = ""
            while(var_type.code == gdb.TYPE_CODE_PTR or var_type.code == gdb.TYPE_CODE_ARRAY):
                if(var_type.code == gdb.TYPE_CODE_PTR):
                    ptr_array_end += "*"
                    last_arr = None
                    var_type = var_type.target()
                elif(var_type.code == gdb.TYPE_CODE_ARRAY):
                    ptr_array_end += "[]"
                    last_arr = var_type
                    var_type = var_type.target()
            var_type_str = "Unknown Type"
            if last_arr != None:
                size = str(int(last_arr.sizeof / var_type.sizeof))
                var_type_str = "STACK-ARRAY LENGTH[" + size + "] " + str(var_type.name) + ptr_array_end[0::-1] + size + "]"
            else:
                var_type_str = str(var_type.name) + ptr_array_end
            print("(" + var_type_str + ") " + symbol.name + ": " + str(symbol.value(frame)));
            variables.append(Variable(symbol.name, var_type_str, str(symbol.value(frame)), var_type.sizeof));
    block = block.superblock
print("##### GDB DEBUG INFO BEGIN ####")
for var in variables:
    gdb.execute("p \"" + var.name + "\"")
    gdb.execute("p \"" + var.type + "\"")
    gdb.execute("p (void*) &" + var.name + " - $sp")
    gdb.execute("p \"" + str(var.base_size) + "\"")
print("##### GDB DEBUG INFO END ####")