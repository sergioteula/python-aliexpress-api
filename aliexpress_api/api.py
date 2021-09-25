"""AliExpress API wrapper for Python

A simple Python wrapper for the AliExpress Open Platform API. This module allows
to get product information and affiliate links from AliExpress using the official
API in an easier way.
"""

from .skd import setDefaultAppInfo
from .skd import api as aliapi
from .tools import get_product_id
from .errors import AliexpressException
from .models import Language, Currency

from types import SimpleNamespace
import json


class AliexpressApi:
    """Provides methods to get information from AliExpress using your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        language (str): Language code. Defaults to EN.
        currency (str): Currency code. Defaults to USD.
        tracking_id (str): The tracking id for link generator. Defaults to None.
    """

    def __init__(self, key: str, secret: str, language: Language, currency: Currency, tracking_id: str = None, **kwargs):
        self._key = key
        self._secret = secret
        self._tracking_id = tracking_id
        self._language = language
        self._currency = currency
        setDefaultAppInfo(self._key, self._secret)


    def product_info(self, product_id: str):
        """Find product information for a specific product on AliExpress.

        Args:
            product_id (str): One item ID or product URL.
        """
        product_id = get_product_id(str(product_id))
        if product_id:
            product = aliapi.rest.AliexpressAffiliateProductdetailGetRequest()
            product.app_signature = None
            product.fields = None
            product.product_ids = product_id
            product.target_currency = self._currency
            product.target_language = self._language
            product.tracking_id = self._tracking_id
            try:
                response = product.getResponse()
                response = json.dumps(response)
                response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
                response = response.aliexpress_affiliate_productdetail_get_response.resp_result
                if response.resp_code == 200:
                    response = response.result
                    if response.current_record_count > 0:
                        response = response.products.product[0]
                        return response
                    else:
                        raise AliexpressException('Product not available')
                else:
                    raise AliexpressException('Server not reached')
            except Exception as e:
                raise AliexpressException(e)
        else:
            raise AliexpressException('Product ID not found')

    def affiliate_link(self, link: str):
        """Creates affiliate link for a specific product.

        Args:
            link (str): The URL that needs to be converted.
        """
        if self._tracking_id:
            affiliate = aliapi.rest.AliexpressAffiliateLinkGenerateRequest()
            affiliate.source_values = link
            affiliate.promotion_link_type = "0"
            affiliate.tracking_id = self._tracking_id
            try:
                response = affiliate.getResponse()
                response = json.dumps(response)
                response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
                response = response.aliexpress_affiliate_link_generate_response.resp_result
                if response.resp_code == 200:
                    response = response.result
                    if response.total_result_count > 0:
                        response = response.promotion_links.promotion_link[0].promotion_link
                        return response
                    else:
                        raise AliexpressException('Affiliate link not available')
                else:
                    raise AliexpressException('Server not reached')
            except Exception as e:
                raise AliexpressException(e)
        else:
            raise AliexpressException('Tracking ID not specified')


    def featured_promos(self):
        """Find product information for a specific product on AliExpress.

        Args:
            product_id (str): One item ID or product URL.
        """
        promo = aliapi.rest.AliexpressAffiliateHotproductQueryRequest()
        promo.app_signature = None
        # promo.fields = None
        # promo.category_id = '204000021'
        promo.target_currency = self._currency
        promo.target_language = self._language
        promo.tracking_id = self._tracking_id
        # promo.fields="commission_rate,sale_price"
        promo.page_no=1
        promo.page_size=50
        # promo.promotion_end_time="2021-12-12 00:00:00"
        # promo.promotion_name="singles' day big sale"
        # promo.promotion_start_time="2021-09-25 00:00:00"
        promo.sort="commissionAsc"
        # promo.target_currency="USD"
        # promo.target_language="EN"
        # promo.country="US"
        promo.keywords="tablet"
        try:
            response = promo.getResponse()
            response = json.dumps(response)
            response = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
            response = response.aliexpress_affiliate_hotproduct_query_response.resp_result
            if response.resp_code == 200:
                response = response.result
                if response.current_record_count > 0:
                    response = response.products.product
                    return response
                else:
                    raise AliexpressException('Product not available')
            else:
                raise AliexpressException('Server not reached')
        except Exception as e:
            raise AliexpressException(e)
