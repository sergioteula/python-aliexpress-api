"""
Created by auto_sdk on 2021.05.12
"""
from ..base import RestApi


class AliexpressAffiliateHotproductDownloadRequest(RestApi):
    def __init__(self, domain="api-sg.aliexpress.com", port=80):
        RestApi.__init__(self, domain, port)
        self.app_signature = None
        self.category_id = None
        self.country = None
        self.fields = None
        self.locale_site = None
        self.page_no = None
        self.page_size = None
        self.target_currency = None
        self.target_language = None
        self.tracking_id = None

    def getapiname(self):
        return "aliexpress.affiliate.hotproduct.download"
