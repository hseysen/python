if __name__ == '__main__':
    N = int(input())
    xs = []
    
    for _ in range(N):
        command = input().split()
        if command[0] == "insert":
            i = int(command[1])
            e = int(command[2])
            xs.insert(i, e)
        elif command[0] == "print":
            print(xs)
        elif command[0] == "remove":
            e = int(command[1])
            xs.remove(e)
        elif command[0] == "append":
            e = int(command[1])
            xs.append(e)
        elif command[0] == "sort":
            xs.sort()
        elif command[0] == "pop":
            xs.pop()
        elif command[0] == "reverse":
            xs.reverse()
        
