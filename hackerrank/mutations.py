def mutate_string(string, position, character):
    pre = string[:position]
    post = string[position+1:]
    return pre + character + post

if __name__ == '__main__':
    s = input()
    i, c = input().split()
    s_new = mutate_string(s, int(i), c)
    print(s_new)