def minion_game(string):
    vowels = "AEIOU"
    string = string.upper()
    # herfin yerlesdiyi yer - i
    # sozun uzunlugu - n
    # hemin herfle baslayan substringlerin sayi - x
    # i + x = n
    # x = n - i
    
    kevin = 0
    stuart = 0
    n = len(string)
    for i in range(n):
        character = string[i]
        if character in vowels:
            kevin += n - i
        else:
            stuart += n - i
            
    if kevin > stuart:
        print("Kevin", kevin)
    elif stuart > kevin:
        print("Stuart", stuart)
    else:
        print("Draw")

if __name__ == '__main__':
    s = input()
    minion_game(s)