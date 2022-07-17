import io
import sys


def next_line_with_padding(indent_level, indent_size, output=sys.stdout):
    print(f'\n{" " * (indent_level * indent_size)}', end="", file=output)


def format_pretty_string(text):
    output = io.StringIO()
    format_pretty(text, output)
    return output.getvalue()


def format_pretty(text, output=sys.stdout):
    indent_level = 0
    indent_size = 4
    newline_needed = False
    is_during_leading_whitespace = True
    for c in text:
        if newline_needed and c != ',':
            next_line_with_padding(indent_level, indent_size, output)
            is_during_leading_whitespace = True
            newline_needed = False
        if c == ' ' and is_during_leading_whitespace:
            continue  # suppress space char during leading whitespace
        print(c, end="", file=output)
        is_during_leading_whitespace = False

        match c:
            case '{':
                indent_level += 1
                next_line_with_padding(indent_level, indent_size, output)
                is_during_leading_whitespace = True
            case '}':
                indent_level -= 1
                newline_needed = True
            case ',':
                next_line_with_padding(indent_level, indent_size, output)
                is_during_leading_whitespace = True
