if __name__ == '__main__':
    scores_students = dict()
    scores = []
    
    for _ in range(int(input())):
        name = input()
        score = float(input())
        if score not in scores_students.keys():
            scores_students[score] = []
        scores_students[score].append(name)
        if score not in scores:
            scores.append(score)
    
    scores.sort()
    result = scores_students[scores[1]]
    result.sort()
    print(*result, sep="\n")
    
