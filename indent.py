def indent(string):
    level = 0
    ind = ' ' * 4
    it = iter(string)
    for char in it:
        print(end=char)
        if char == '(':
            level += 1
            print()
            print(end=ind*level)
        elif char == ',':
            print()
            print(end=ind*level)
        elif char == ')':
            level -= 1
            print()
            print(end=ind*level)

    
