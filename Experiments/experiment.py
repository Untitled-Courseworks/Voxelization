class SquareEquationException(Exception):
    pass


def solve_square_equation(expr: str)-> list:
    pass


def read_equation(equation: str):
    temp = equation.split("*x")
    if len(temp) != 3 or temp[1][0:2:] != "^2" or (temp[1][2] != "+" or "-"):
        raise SquareEquationException()
    temp[1] = temp[1][2::]
    res = [float(i) for i in temp]
    return res


print(read_equation("2223333"))

print(read_equation("-02.5*x^24-1.5*x+3"))
