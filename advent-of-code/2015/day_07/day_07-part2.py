def parse_operand(operand):
    if operand.isnumeric():
        return int(operand)
    return operand


def parse_inputs(inputs):
    """
    Parse inputs for the operator and operands.
    """
    if len(inputs) == 1:
        return "ASSIGN", [inputs[0]]

    elif len(inputs) == 2:
        return inputs[0], [inputs[1]]

    elif len(inputs) == 3:
        return inputs[1], [inputs[0], inputs[2]]

    else:
        raise ValueError(f"Invalid inputs, unable to parse {inputs}")


def get_wire_value(wires, wire):
    if type(wires[wire]) is int:
        return wires[wire]

    return get_wire_value(wires, wires[wire])


with open("./input/07.txt", "r") as file:
    lines = file.readlines()
    wires = {}
    data = {}

    for line in lines:
        # output is always a wire
        inputs_string, output = line.strip().split(" -> ")
        inputs = inputs_string.split(" ")

        operator, operands = parse_inputs(inputs)
        operands = [parse_operand(op) for op in operands]

        if operator == "ASSIGN":
            data[output] = {
                "operator": "",
                "operands": operands,
            }
        elif operator == "NOT":
            data[output] = {
                "operator": "~",
                "operands": operands,
            }
        elif operator == "AND":
            data[output] = {
                "operator": "&",
                "operands": operands,
            }
        elif operator == "OR":
            data[output] = {
                "operator": "|",
                "operands": operands,
            }
        elif operator == "LSHIFT":
            data[output] = {
                "operator": "<<",
                "operands": operands,
            }
        elif operator == "RSHIFT":
            data[output] = {
                "operator": ">>",
                "operands": operands,
            }

        else:
            print("INVALID", operator)
            raise RuntimeError

    def resolve(wire, depth=0):
        if type(wire) is int:
            return wire

        if wires.get(wire):
            return wires[wire]

        d = data[wire]
        operator = d.get("operator")
        operands = d.get("operands")

        # print(f'Resolving wire="{wire}" @ depth={depth}')

        if operator == "":
            value = resolve(operands[0], depth + 1)

        if operator == "~":
            value = ~resolve(operands[0], depth + 1)

        if operator == "&":
            value = resolve(operands[0], depth + 1) & resolve(operands[1], depth + 1)

        if operator == "|":
            value = resolve(operands[0], depth + 1) | resolve(operands[1], depth + 1)

        if operator == "<<":
            value = resolve(operands[0], depth + 1) << resolve(operands[1], depth + 1)

        if operator == ">>":
            value = resolve(operands[0], depth + 1) >> resolve(operands[1], depth + 1)

        wires[wire] = value
        return value

    signal_a = resolve("a")
    wires = {"b": signal_a}
    signal_a_again = resolve("a")

    print("a:", signal_a)
    print("a again:", signal_a_again)
