def strip_characters(string: str):
    result = ""
    for char in string:
        if char.isdigit():
            result += char
    return int(result) if result != '' else 0
