class Category:
    category_id: int
    category_name: str


class SecondaryCategory(Category):
    parent_category_id: int
