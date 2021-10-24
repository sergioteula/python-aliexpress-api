"""Some useful tools."""

from ..errors import ProductIdNotFoundException
import re


def get_product_id(text: str) -> str:
    """Returns the product ID from a given text. Raises ProductIdNotFoundException on fail."""
    # Return if text is a product ID
    if re.search(r'^[0-9]*$', text):
        return text

    # Extract product ID from URL
    asin = re.search(r'(\/)([0-9]*)(\.)', text)
    if asin:
        return asin.group(2)
    else:
        raise ProductIdNotFoundException('Product id not found: ' + text)
