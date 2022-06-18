with open('../ads.csv') as f:
    while True:
        try:
            line=next(f)
        except StopIteration:
            break
        print(line)