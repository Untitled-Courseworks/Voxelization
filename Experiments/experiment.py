def convert_base(num, to_base=10, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


def is_polyndrom(n: int) -> int:
    for base in range(2, 37):
        num = convert_base(str(n), base, 10)
        if num == num[::-1]:
            return base
    return 0


print(is_polyndrom(99998))
