import difflib

# Return if number is a valid knooppunt number
def is_number_valid(number):
    if not number or number == "?" or number == "0" or number == "":
        return False

    return True

def is_small_rename(a, b):
    for i, s in enumerate(difflib.ndiff(a, b)):
        if s[0] == ' ':
            continue
        elif s[0] == '+' or s[0] == '-':
            if not s[-1].isalpha():
                return False

    return True
