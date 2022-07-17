
def padding(indent_level, indent_size):
    print(f'\n{" " * (indent_level * indent_size)}', end="")


def format_pretty(text):
    indent_level = 0
    indent_size = 4
    newline_needed = False
    is_during_leading_whitespace = True
    for c in text:
        if newline_needed and c != ',':
            padding(indent_level, indent_size)
            is_during_leading_whitespace = True
            newline_needed = False
        if c == ' ' and is_during_leading_whitespace:
            continue  # suppress space char during leading whitespace
        print(c, end="")
        is_during_leading_whitespace = False

        match c:
            case '{':
                indent_level += 1
                padding(indent_level, indent_size)
                is_during_leading_whitespace = True
            case '}':
                indent_level -= 1
                newline_needed = True
            case ',':
                padding(indent_level, indent_size)
                is_during_leading_whitespace = True
