# Return if number is a valid knooppunt number
def is_number_valid(number):
    if number == "?" or number == "0" or number == "":
        return False

    if isinstance(number, str) and len(number) == 3 and 'A' <= number[0] <= 'Z':
        number = number[1:3]

    try:
        if int(number) < 1:
            return False
    except ValueError:
        # It's not a number
        return False

    return True
