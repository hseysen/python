def print_formatted(number):
    n = len(f"{number:b}")
    for i in range(1, number+1):
        print(f"{i:>{n}} {oct(i)[2:]:>{n}} {hex(i)[2:].upper():>{n}} {bin(i)[2:]:>{n}}")

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)