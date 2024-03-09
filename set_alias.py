def set_alias(filename):
    with open(filename) as f:
        lines = [line for line in f]

    line = lines[-1].split(";")
    count = int(line[0].strip())
    line[1] = line[1].strip()
    index = 2
    aliases = {}

    while count:
        ct = 1
        ind = ""
        alias_name = ""

        while True:
            if line[1][index] == ",":
                index+=2
                break
            
            ind+=line[1][index]
            index+=1
        
        while ct:
            
            if line[1][index] == "]":
                ct -= 1
            
            if line[1][index] == "[":
                ct += 1
            
            if ct == 0:
                index+=4
                break

            alias_name += line[1][index]
            index += 1

        alias_value = input(f"Enter value of '{alias_name}': ")
        aliases[ind] = [alias_name, alias_value]
        count -= 1

    return aliases
