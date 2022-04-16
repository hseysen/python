def count_substring(string, sub_string):
    c = 0
    
    n = len(string)
    k = len(sub_string)
    
    for i in range(0, n):
        s = string[i:i+k]
        if s == sub_string:
            c += 1
    
    return c

if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()
    
    count = count_substring(string, sub_string)
    print(count)