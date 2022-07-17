def format_pretty(text):
    indent_level = 0
    indent_size = 4
    for c in text:
        print(c, end="")
        padding = " " * (indent_level * indent_size)
        match c:
            case '{':
                indent_level += 1
                print(f'\n{padding}', end="")
            case '}':
                indent_level -= 1
                print(f'\n{padding}', end="")
            case ',':
                print(f'\n{padding}', end="")
