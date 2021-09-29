from ..errors.exceptions import InvalidArgumentException


def get_list_as_string(value):
    if isinstance(value, str):
        return value

    elif isinstance(value, list):
        return ','.join(value)

    else:
        raise InvalidArgumentException('Argument should be a list or string: ' + str(value))
