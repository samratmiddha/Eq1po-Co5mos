def alias(filename):
    with open(filename, "r") as f:
        lines = [line for line in f]

    count = 0
    ind = 0
    variables = []

    for line in lines:
        line = line.split(";")
        line = line[1].strip()
        
        if line:
            user_res = input(f"Do you want to keep '{line}' as a variable? (Y/N) ")
            if user_res == "Y":
                count+=1
                alias_name = input(f"What do you want to name the alias? ")
                variables.append([ind, alias_name])

        ind+=1

    with open(filename, "a") as f:
        f.write(f"{count} ; {variables}")
