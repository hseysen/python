def split_and_join(line):
    elements = line.split(" ")
    return "-".join(elements)

if __name__ == '__main__':
    line = input()
    result = split_and_join(line)
    print(result)