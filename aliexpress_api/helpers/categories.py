from typing import List, Union
from .. import models


def filter_parent_categories(categories: List[Union[models.Category, models.ChildCategory]]) -> List[models.Category]:
    filtered_categories = []

    for category in categories:
        if not hasattr(category, 'parent_category_id'):
            filtered_categories.append(category)

    return filtered_categories


def filter_child_categories(categories: List[Union[models.Category, models.ChildCategory]],
                            parent_category_id: int) -> List[models.ChildCategory]:
    filtered_categories = []

    for category in categories:
        if hasattr(category, 'parent_category_id') and category.parent_category_id == parent_category_id:
            filtered_categories.append(category)

    return filtered_categories
