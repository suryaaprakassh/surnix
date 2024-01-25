import sys


def format_types(types):
    return_string = ""
    for type in types.split(", "):
        split_value = type.split(" ")
        return_string += f"{split_value[1]}, "

    return return_string


def define_type(f, base_name, class_name, types):
    f.write(f"    def __init__(self, {format_types(types)}):\n")
    fields = types.split(", ")
    for field in fields:
        name = field.split(" ")[1]
        f.write(f"        self.{name} = {name}\n")
    f.write("\n\n")
    f.write(f"    def accept(self, visitor):\n")
    f.write(f"        return visitor.visit_{class_name}(self)\n")


def define_visitor(types,  output_dir):
    path = output_dir + "/Visitor.py"
    with open(path, 'a') as f:
        f.write("from abc import abstractmethod\n")
        for type in types:
            class_name = type.split(":")[0].strip()
            # f.write(f"from {class_name} import {class_name}\n")
        f.write("\n\n")
        f.write("class Visitor:\n")
        for type in types:
            class_name = type.split(":")[0].strip()
            f.write(f"    @abstractmethod\n")
            f.write(f"    def visit_{class_name}(self, expr: {class_name}):\n")
            f.write(f"        pass\n")


def define_ast(output_dir, base_name, types):
    for type in types:
        class_name = type.split(":")[0].strip()
        fields = type.split(":")[1].strip()
        path = output_dir + "/" + class_name + ".py"
        with open(path, 'w') as f:
            f.write(f"from {base_name} import {base_name}\n\n")
            f.write(f"class {class_name}({base_name}):\n")
            define_type(f, base_name, class_name, fields)
            f.write("\n\n")
    define_visitor(types,  output_dir)


def main():
    args = sys.argv
    if (len(args) != 2):
        print("Usage: python GenerateAst.py <output directory>")
        return
    output_dir = args[1]
    define_ast(output_dir, "Expr", [
        "Assign   : Token name, Expr value",
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : object value",
        "Unary    : Token operator, Expr right",
        "Variable : Token name"
    ])
    define_ast(output_dir, "Stmt", [
        "Expression : Expr expression",
        "Print : Expr expression",
        "Var : Token name, Expr initializer",
        "Block : List statements"
    ])


if __name__ == "__main__":
    main()
