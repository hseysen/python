if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    
    s_arr = set(arr)
    arr = list(s_arr)
    arr.sort()
    print(arr[-2])
