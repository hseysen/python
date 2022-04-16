alphabet = "abcdefghijklmnopqrstuvwxyz"

def helper(i, k):
    ardicilliq = [alphabet[k - j] for j in range(i+1)] + [alphabet[k - j] for j in range(i-1, -1, -1)]
    return "-".join(ardicilliq)

def print_rangoli(size):
    size = size - 1
    k = size
    
    for i in range(k):
        line = f"{helper(i, k):-^{4*k+1}}"
        print(line)
    
    print(helper(k, k))
        
    for i in range(k-1, -1, -1):
        line = f"{helper(i, k):-^{4*k+1}}"
        print(line)
        
    # size = 3 -> n = 9
    # size = 5 -> n = 17
    # size = 10 -> n = 37
    # n = 4*k+1
    

if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)