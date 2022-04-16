def merge_the_tools(string, k):
    n = len(string)
    
    for i in range(0, n, k):
        s = string[i:i+k]
        temp = ""
        for c in s:
            if c not in temp:
                temp += c
        print(temp)
        

if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)