from ..errors.exceptions import InvalidArgumentException


def get_links_string(links):
    if isinstance(links, str):
        return links

    elif isinstance(links, list):
        return ','.join(links)

    else:
        raise InvalidArgumentException('Links argument should be a list or string')
