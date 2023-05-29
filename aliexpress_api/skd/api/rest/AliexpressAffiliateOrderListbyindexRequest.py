"""
Created by auto_sdk on 2021.05.10
"""
from ..base import RestApi


class AliexpressAffiliateOrderListbyindexRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.end_time = None
        self.fields = None
        self.page_size = None
        self.start_query_index_id = None
        self.start_time = None
        self.status = None

    def getapiname(self):
        return "aliexpress.affiliate.order.listbyindex"
