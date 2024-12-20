from .order import Order
from typing import List

class OrderListResponse:
    total_record_count: int
    current_record_count: int
    total_page_no: int
    current_page_no: int
    orders: List[Order]