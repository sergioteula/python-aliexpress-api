from typing import List, Union
from .. import models

def filter_main_categories(categories: List[Union[models.Category, models.SecondaryCategory]]) -> List[models.Category]:
    filtered_categories = []

    for category in categories:
        if not hasattr(category, 'parent_category_id'):
            filtered_categories.append(category)

    return filtered_categories
