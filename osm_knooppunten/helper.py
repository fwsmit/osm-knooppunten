# Return if number is a valid knooppunt number
def is_number_valid(number):
    if number == "?" or number == "0" or number == "":
        return False

    try:
        if int(number) < 1:
            return False
    except ValueError:
        # It's not a number
        return False

    return True
