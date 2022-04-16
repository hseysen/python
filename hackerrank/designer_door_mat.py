# Enter your code here. Read input from STDIN. Print output to STDOUT


n, m = map(int, input().split())
symbol = ".|."
space = "-"
welcome = "WELCOME"
k = (n - 1) // 2

for i in range(k):
    line = f"{symbol * (2*i + 1):{space}^{m}}"
    print(line)
    
middle_line = f"{welcome:{space}^{m}}"
print(middle_line)

for i in range(k-1, -1, -1):
    line = f"{symbol * (2*i + 1):{space}^{m}}"
    print(line)
